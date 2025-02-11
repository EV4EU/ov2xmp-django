from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result, call
import ocpp.v16.enums as ocpp_v16_enums
from ocpp.v16 import datatypes as ocpp_v16_datatypes

from chargepoint.models import Chargepoint as ChargepointModel
from idtag.models import IdTag as idTagModel
from transaction.models import Transaction as TransactionModel
from transaction.models import TransactionStatus
from connector.models import Connector as ConnectorModel
from reservation.models import Reservation as ReservationModel
from statusnotification.models import Statusnotification as StatusnotificationModel
from sampledvalue.models import Sampledvalue as SampledvalueModel

from uuid import uuid4
from uuid import UUID
from decimal import Decimal
from chargingprofile.models import Chargingprofile as ChargingprofileModel
from django.utils import timezone
from datetime import datetime, timezone
import json
from channels.layers import get_channel_layer
from django.db import DatabaseError
import logging
from django.db.models import Max

channel_layer = get_channel_layer()


def convert_special_types(obj):
    """
    Helper function that recursively traverses through a dictionary or list, and converts
    datetime to string via isoformat(), UUID to string, and Decimal to float.
    """
    if isinstance(obj, dict):
        return {key: convert_special_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_special_types(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


async def broadcast_metervalues(message):
    message = json.dumps(message)
    if channel_layer is not None:
        await channel_layer.group_send("metervalues_updates", {"type": "websocket.send", "text": message})


def authorize_idTag(id_token):
    if id_token is not None: 
        try:
            idTag_object = idTagModel.objects.get(idToken=id_token)
            if not idTag_object.revoked:
                if idTag_object.expiry_date is not None:
                    if idTag_object.expiry_date.timestamp() > datetime.now(timezone.utc).timestamp():
                        return {"status": ocpp_v16_enums.AuthorizationStatus.accepted.value}
                    else:
                        return {"status": ocpp_v16_enums.AuthorizationStatus.expired.value}
                else:
                    return {"status": ocpp_v16_enums.AuthorizationStatus.accepted.value}
            else:
                return {"status": ocpp_v16_enums.AuthorizationStatus.blocked.value}
        except idTagModel.DoesNotExist:
            return {"status": ocpp_v16_enums.AuthorizationStatus.invalid.value}
    else:
        return {"status": None}


class ChargePoint16(cp):
    ##########################################################################################################################
    ###################  HANDLE INCOMING OCPP MESSAGES #######################################################################
    ##########################################################################################################################
    @on(ocpp_v16_enums.Action.BootNotification)
    def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):

        charge_box_serial_number = kwargs.get('charge_box_serial_number', None) 
        charge_point_serial_number = kwargs.get('charge_point_serial_number', None)
        firmware_version = kwargs.get('firmware_version', None)

        ChargepointModel.objects.filter(pk=self.id).update(
            chargepoint_model = charge_point_model, 
            chargepoint_vendor = charge_point_vendor,
            chargebox_serial_number = charge_box_serial_number,
            chargepoint_serial_number = charge_point_serial_number,
            firmware_version = firmware_version
        ) 

        return call_result.BootNotification(
            current_time=datetime.now(timezone.utc).isoformat(),
            interval=10,
            status=ocpp_v16_enums.RegistrationStatus.accepted,
        )
    

    @on(ocpp_v16_enums.Action.Heartbeat)
    def on_heartbeat(self):
        current_cp = ChargepointModel.objects.filter(pk=self.id).get()
        current_cp.last_heartbeat = datetime.now(timezone.utc)
        current_cp.save()

        return call_result.Heartbeat(
            current_time=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )


    @on(ocpp_v16_enums.Action.StatusNotification)
    def on_status_notification(self, connector_id, error_code, status, **kwargs):
        current_cp = ChargepointModel.objects.filter(pk=self.id).get()
        if connector_id != 0:
            try:
                connector_to_update = ConnectorModel.objects.filter(chargepoint=current_cp, connectorid=connector_id).get()
                connector_to_update.connector_status = status
                connector_to_update.save()
            except ConnectorModel.DoesNotExist:     
                connector_to_update = None
                ConnectorModel.objects.create(
                    uuid = uuid4(),
                    connectorid = connector_id,
                    connector_status = status,
                    chargepoint = current_cp
                )
        else:
            connector_to_update = None
            current_cp.chargepoint_status = status
            current_cp.save()
        
        StatusnotificationModel.objects.create(
            connector = connector_to_update,
            chargepoint = current_cp,
            error_code = error_code,
            info = kwargs.get('info', None),
            status_reported = status,
            timestamp = kwargs.get('timestamp', datetime.now(timezone.utc)),
            vendor_id = kwargs.get('vendor_id', None),
            vendor_error_code = kwargs.get('vendor_error_code', None)
        )

        return call_result.StatusNotification()


    @on(ocpp_v16_enums.Action.Authorize)
    def on_authorize(self, id_tag):
        result = authorize_idTag(id_tag)
        return call_result.Authorize(id_tag_info=result) # type: ignore


    @on(ocpp_v16_enums.Action.StartTransaction)
    def on_startTransaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):

        current_cp = ChargepointModel.objects.filter(pk=self.id).get()

        new_transaction = TransactionModel.objects.create(
            start_transaction_timestamp = timestamp,
            wh_meter_start = meter_start,
            wh_meter_last = meter_start,
            wh_meter_last_timestamp = timestamp
        )
        new_transaction.save()

        result = authorize_idTag(id_tag)
        
        if result["status"] == ocpp_v16_enums.AuthorizationStatus.accepted:
            new_transaction.id_tag = idTagModel.objects.get(idToken=id_tag)
            try:
                new_transaction.connector = ConnectorModel.objects.filter(connectorid=connector_id, chargepoint=current_cp).get()

                # Retrieve the charging profile currently associated with the connector
                # chargingprofile_queryset = ChargingprofileModel.objects.filter(chargingprofile_id=new_transaction.connector.charging_profile)
                # Dump the charging profile and save it as attribute of the transaction
                # TODO: This code always takes the first chargingprofile, however the connector may have multiple charging profiles. To do this correctly, get the charging profile with the greatest stack level.
                #chargingprofile = list(chargingprofile_queryset.values())
                #if len(chargingprofile) > 0:
                #    chargingprofile = chargingprofile[0]
                #    new_transaction.chargingprofile = convert_special_types(chargingprofile)
                #else:
                new_transaction.chargingprofile = None

                # Retrieve all the tariffs currently associated with the connector
                tariff_queryset = new_transaction.connector.tariff_ids.all()
                # Dump the tariff objects and save them as attribute of the transaction
                tariff_list = list(tariff_queryset.values())
                new_transaction.tariffs = convert_special_types(tariff_list)

            except ConnectorModel.DoesNotExist:
                pass
            reservation_id = kwargs.get('reservation_id', None)
            if reservation_id is not None:
                ReservationModel.objects.filter(connector__chargepoint__chargepoint_id = self.id, reservation_id=reservation_id).delete()
            new_transaction.transaction_status = TransactionStatus.started
        else:
            new_transaction.stop_transaction_timestamp = datetime.now(timezone.utc)
            new_transaction.wh_meter_stop = meter_start
            new_transaction.reason_stopped = TransactionStatus.unauthorized
            new_transaction.transaction_status = TransactionStatus.unauthorized
        
        new_transaction.save()
        
        return call_result.StartTransaction(
            transaction_id = new_transaction.transaction_id,
            id_tag_info = ocpp_v16_datatypes.IdTagInfo(status=result["status"])
        )


    @on(ocpp_v16_enums.Action.MeterValues)
    async def on_meterValues(self, connector_id, meter_value, **kwargs):
        transaction_id = kwargs.get('transaction_id', None)
        
        # Check if the transaction_id is valid, otherwise return MeterValues.conf
        if transaction_id is not None and transaction_id > 0:
            try:
                # Check if the transaction_id corresponds to a transaction that exists in the database
                transaction = TransactionModel.objects.get(transaction_id=transaction_id)
                wh_meter_last = None
                wh_meter_last_timestamp = None
                for _metervalue in meter_value:
                    wh_meter_last_timestamp = _metervalue["timestamp"]
                    for _sampledvalue in _metervalue["sampled_value"]:
                        SampledvalueModel.objects.create(
                            transaction = transaction,
                            timestamp = wh_meter_last_timestamp,
                            value = _sampledvalue["value"],
                            context = _sampledvalue.get('context', None),
                            format = _sampledvalue.get("format", None),
                            measurand = _sampledvalue.get("measurand", None),
                            phase = _sampledvalue.get('phase', None),
                            location = _sampledvalue.get('location', None),
                            unit = _sampledvalue.get('unit', None)
                        ).save()
        
                        if 'unit' in _sampledvalue:
                            if _sampledvalue['unit'] == "Wh":
                                wh_meter_last = _sampledvalue['value']
                        
                        if wh_meter_last is not None:
                            TransactionModel.objects.filter(transaction_id=transaction_id).update(wh_meter_last = wh_meter_last, 
                                                                                                  wh_meter_last_timestamp = wh_meter_last_timestamp)
                        
                    # if everything is sucessful, broadcast the metervalues message to the django channel
                    message = {
                        "transaction_id": transaction_id,
                        "connector_id": connector_id, 
                        "meterValue": meter_value
                    }
                    await broadcast_metervalues(message)
                return call_result.MeterValues()

            except TransactionModel.DoesNotExist:
                # Return MeterValues.conf if the transaction_id is not found in the database
                return call_result.MeterValues()
        else:
            # If transaction_id is invalid, just return a MeterValues.conf
            return call_result.MeterValues()


    @on(ocpp_v16_enums.Action.StopTransaction)
    def on_stopTransaction(self, meter_stop, timestamp, transaction_id, **kwargs): #reason, id_tag, transaction_data):
        
        try:
            current_transaction = TransactionModel.objects.get(transaction_id=transaction_id)

            current_transaction.stop_transaction_timestamp = timestamp
            current_transaction.wh_meter_stop = meter_stop
            current_transaction.transaction_status = TransactionStatus.finished
            reason = kwargs.get('reason', None)
            if reason is not None:
                current_transaction.reason_stopped = reason

            current_transaction.save()

            return call_result.StopTransaction()
        
        except DatabaseError as e:
            logging.error("Connection error with Django DB. The transaction details for # " + str(transaction_id) + " have not been saved.")
            return call_result.StopTransaction()


    @on(ocpp_v16_enums.Action.DiagnosticsStatusNotification)
    def on_DiagnosticsStatusNotification(self, status):
        return call_result.DiagnosticsStatusNotification()
    
    
    @on(ocpp_v16_enums.Action.FirmwareStatusNotification)
    def on_FirmwareNotification(self):
        return call_result.FirmwareStatusNotification()

    ##########################################################################################################################
    #################### ACTIONS INITIATED BY THE CSMS #######################################################################
    ##########################################################################################################################

    # Reset
    async def reset(self, reset_type):
        request = call.Reset(type = reset_type)
        return await self.call(request)

    # RemoteStartTransaction
    async def remote_start_transaction(self, id_tag, connector_id, charging_profile):
        request = call.RemoteStartTransaction(
            connector_id=connector_id,
            id_tag=id_tag,
            charging_profile=charging_profile
        )
        return await self.call(request)

    # RemoteStopTransaction
    async def remote_stop_transaction(self, transaction_id):
        request = call.RemoteStopTransaction(
            transaction_id=transaction_id
        )
        return await self.call(request)
    
    # ReserveNow
    async def reserve_now(self, connector_id, id_tag, expiry_date, reservation_id):

        if reservation_id is None:
            # If reservation_id is not provided, we need to find the maximum reservation_id that exists for the particular EVCS
            # Get all reservations of the specific EVCS and find the max reservation_id value. then, add +1 (so we do not replace any existing reservation_id on the particular EVCS)
            reservation_id = ReservationModel.objects.filter(connector__chargepoint__chargepoint_id=self.id).aggregate(Max('reservation_id'))["reservation_id__max"] + 1
            
        request = call.ReserveNow(
            connector_id=connector_id,
            id_tag=id_tag,
            expiry_date=expiry_date,
            reservation_id=reservation_id
        )

        response = await self.call(request)
        if response is not None:
            # Create the reservation instance, if status accepted
            if response.status == ocpp_v16_enums.ReservationStatus.accepted:
                connector = ConnectorModel.objects.filter(chargepoint__chargepoint_id=self.id, connectorid=connector_id)
                ReservationModel.objects.create(
                    connector=connector,
                    reservation_id=reservation_id,
                    expiry_date=expiry_date
                ).save()
            return response
        else:
            return None

    # CancelReservation
    async def cancel_reservation(self, reservation_id):
        request = call.CancelReservation(
            reservation_id=reservation_id
        )
        response = await self.call(request)
        if response is not None:
            if response.status == ocpp_v16_enums.ReservationStatus.accepted:
                reservation_to_delete = ReservationModel.objects.filter(connector__chargepoint__chargepoint_id=self.id, reservation_id=reservation_id)
                reservation_to_delete.delete()
            return response
        else:
            return None
        
    # ChangeAvailability
    async def change_availability(self, connector_id, availability_type):
        request = call.ChangeAvailability(
            connector_id=connector_id,
            type=availability_type
        )
        return await self.call(request)

    # ChangeConfiguration
    async def change_configuration(self, key, value):
        request = call.ChangeConfiguration(
            key=key,
            value=value
        )
        return await self.call(request)
    
    # ClearCache
    async def clear_cache(self):
        request = call.ClearCache()
        return await self.call(request)
    
    # UnlockConnector
    async def unlock_connector(self, connector_id):
        request = call.UnlockConnector(
            connector_id=connector_id
        )
        return await self.call(request)

    # GetConfiguration
    async def get_configuration(self, keys):
        request = call.GetConfiguration(
            key=keys
        )
        return await self.call(request)

    # GetCompositeSchedule
    async def get_composite_schedule(self, connector_id, duration, charging_rate_unit_type):
        request = call.GetCompositeSchedule(
            connector_id= connector_id,
            duration= duration,
            charging_rate_unit= charging_rate_unit_type)
        return await self.call(request)
        
    # ClearChargingProfile
    async def clear_charging_profile(self, charging_profile_id, connector_id, charging_profile_purpose_type, stack_level):
        request = call.ClearChargingProfile(
            id = charging_profile_id,
            connector_id = connector_id,
            charging_profile_purpose = charging_profile_purpose_type,
            stack_level = stack_level)
        return await self.call(request)
        
    #SetChargingProfile
    async def set_charging_profile(self, connector_id, charging_profile):
        request = call.SetChargingProfile(
            connector_id=connector_id,
            cs_charging_profiles = charging_profile)
        return await self.call(request)

    #GetDiagnostics
    async def get_diagnostics(self, location, retries, retry_interval, start_time, stop_time):
        request = call.GetDiagnostics(
            location=location,
            retries=retries,
            retry_interval=retry_interval,
            start_time=start_time,
            stop_time=stop_time)
        return await self.call(request)

    #UpdateFirmware
    async def update_firmware(self, location, retries, retrieve_date, retry_interval):
        request = call.UpdateFirmware(
            location=location,
            retries=retries,
            retrieve_date=retrieve_date,
            retry_interval=retry_interval
        )
        return await self.call(request)

    #TriggerMessage
    async def trigger_message(self, requested_message, connector_id):
        request = call.TriggerMessage(
            requested_message=requested_message,
            connector_id=connector_id
        )
        return await self.call(request)

    #GetLocalListVersion
    async def get_local_list_version(self):
        request = call.GetLocalListVersion()
        return await self.call(request)

    #SendLocalList
    async def send_local_list(self, list_version, update_type, local_authorization_list=list()):
        request = call.SendLocalList(
            list_version=list_version,
            update_type=update_type,
            local_authorization_list=local_authorization_list
        )
        return await self.call(request)