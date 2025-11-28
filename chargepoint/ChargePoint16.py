from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result, call
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, ReservationStatus
from ocpp.v16 import datatypes as ocpp_datatypes
from ocpp.v16 import enums as ocpp_enums

from chargepoint.models import Chargepoint as ChargepointModel
from idtag.models import IdTag as idTagModel
from transaction.models import Transaction as TransactionModel
from transaction.models import TransactionStatus
from connector.models import Connector as ConnectorModel
from reservation.models import Reservation as ReservationModel
from statusnotification.models import Statusnotification as StatusnotificationModel
from sampledvalue.models import Sampledvalue as SampledvalueModel
from chargingprofile.models import Chargingprofile16 as ChargingprofileModel
from chargingprofile.serializers import Chargingprofile16Serializer
from ocpi.tasks import create_cdr, apply_cdr
from ov2xmp.helpers import serialize_special_types

from uuid import uuid4
from datetime import datetime, timezone
import json
from channels.layers import get_channel_layer
from django.db import DatabaseError
import logging
from django.db.models import Max

channel_layer = get_channel_layer()

ov2xmp_logger = logging.getLogger('ov2xmp')
ov2xmp_logger.setLevel(logging.DEBUG)


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
                        return {"status": AuthorizationStatus.accepted.value}
                    else:
                        return {"status": AuthorizationStatus.expired.value}
                else:
                    return {"status": AuthorizationStatus.accepted.value}
            else:
                return {"status": AuthorizationStatus.blocked.value}
        except idTagModel.DoesNotExist:
            return {"status": AuthorizationStatus.invalid.value}
    else:
        return {"status": None}


def chargingprofile16model_to_chargingprofile16type(chargingprofile_object: ChargingprofileModel) -> ocpp_datatypes.ChargingProfile:
    """
    Function that converts the ChargingProfile Django model to a ChargingProfile object of the OCPP library, so that it can be sent to a charging station.
    """
    chargingscheduleperiods_list_ocppType = list()
    for chargingscheduleperiod in chargingprofile_object.chargingschedule_period:
        chargingscheduleperiods_list_ocppType.append(
            ocpp_datatypes.ChargingSchedulePeriod(
                start_period=chargingscheduleperiod['startPeriod'],
                limit=chargingscheduleperiod['limit'],
                number_phases=chargingscheduleperiod.get('number_phases', None)
            )
        )

    chargingschedule_ocppType = ocpp_datatypes.ChargingSchedule(
        charging_rate_unit= ocpp_enums.ChargingRateUnitType(value=chargingprofile_object.charging_rate_unit),
        duration = chargingprofile_object.duration,
        charging_schedule_period=chargingscheduleperiods_list_ocppType
    )

    if chargingprofile_object.min_charging_rate:
        chargingschedule_ocppType.min_charging_rate = float(chargingprofile_object.min_charging_rate)

    if chargingprofile_object.start_schedule:
        chargingschedule_ocppType.start_schedule = chargingprofile_object.start_schedule.isoformat()

    cp = ocpp_datatypes.ChargingProfile(
        charging_profile_id = chargingprofile_object.chargingprofile_id,
        stack_level = chargingprofile_object.stack_level,
        charging_profile_purpose = ocpp_enums.ChargingProfilePurposeType(value=chargingprofile_object.chargingprofile_purpose),
        charging_profile_kind = ocpp_enums.ChargingProfileKindType(value=chargingprofile_object.chargingprofile_kind),
        charging_schedule = chargingschedule_ocppType,
    )

    if chargingprofile_object.transaction_id:
        cp.transaction_id = chargingprofile_object.transaction_id.transaction_id
    
    if chargingprofile_object.recurrency_kind:
        cp.recurrency_kind = ocpp_enums.RecurrencyKind(value=chargingprofile_object.recurrency_kind)

    if chargingprofile_object.valid_from:
        cp.valid_from = chargingprofile_object.valid_from.isoformat()
    
    if chargingprofile_object.valid_to:
        cp.valid_to = chargingprofile_object.valid_to.isoformat()

    return cp


class ChargePoint16(cp):
    ##########################################################################################################################
    ###################  HANDLE INCOMING OCPP MESSAGES #######################################################################
    ##########################################################################################################################
    @on(Action.boot_notification)
    def on_boot_notification(self, charge_point_vendor:str, charge_point_model:str, **kwargs):

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
            status=RegistrationStatus.accepted,
        )
    

    @on(Action.heartbeat)
    def on_heartbeat(self):
        current_cp = ChargepointModel.objects.filter(pk=self.id).get()
        current_cp.last_heartbeat = datetime.now(timezone.utc)
        current_cp.save()

        return call_result.Heartbeat(
            current_time=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )


    @on(Action.status_notification)
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


    @on(Action.authorize)
    def on_authorize(self, id_tag):
        result = authorize_idTag(id_tag)
        return call_result.Authorize(id_tag_info=result) # type: ignore


    @on(Action.start_transaction)
    def on_startTransaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):

        # Parse timestamp if it's a string
        if isinstance(timestamp, str):
            start_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            start_timestamp = timestamp

        new_transaction = TransactionModel.objects.create(
            start_transaction_timestamp = start_timestamp,
            wh_meter_start = meter_start,
            wh_meter_last = meter_start,
            wh_meter_last_timestamp = start_timestamp
        )

        # Obtain the relevant Connector object
        try:
            connector = ConnectorModel.objects.get(
                chargepoint__chargepoint_id=self.id, 
                connectorid=connector_id
            )   
        except ConnectorModel.DoesNotExist:
            connector = None
        new_transaction.connector = connector

        new_transaction.save()

        result = authorize_idTag(id_tag)
        
        if result["status"] == AuthorizationStatus.accepted:
            new_transaction.id_tag = idTagModel.objects.get(idToken=id_tag)
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
            id_tag_info = ocpp_datatypes.IdTagInfo(status=result["status"])
        )


    @on(Action.meter_values)
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


    @on(Action.stop_transaction)
    def on_stopTransaction(self, meter_stop, timestamp, transaction_id, **kwargs):
        
        try:
            current_transaction = TransactionModel.objects.get(transaction_id=transaction_id)
            
            # Parse timestamp if it's a string
            if isinstance(timestamp, str):
                stop_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                stop_timestamp = timestamp
            
            # Update transaction with stop details
            current_transaction.stop_transaction_timestamp = stop_timestamp
            current_transaction.wh_meter_stop = meter_stop
            current_transaction.transaction_status = TransactionStatus.finished
            reason = kwargs.get('reason', None)
            if reason is not None:
                current_transaction.reason_stopped = reason

            # Get charging profiles from connector's charging_profile array
            if current_transaction.connector is not None:
                connector = current_transaction.connector
                
                # Get the charging profile IDs that are currently in the connector
                connector_charging_profile_ids = connector.charging_profile if connector.charging_profile else []
                ov2xmp_logger.info(f"Connector has {len(connector_charging_profile_ids)} charging profiles: {connector_charging_profile_ids}")
                
                if connector_charging_profile_ids and current_transaction.stop_transaction_timestamp is not None:
                    
                    # Get transaction time window
                    t_s = current_transaction.start_transaction_timestamp.replace(tzinfo=timezone.utc)
                    t_e = current_transaction.stop_transaction_timestamp.replace(tzinfo=timezone.utc)
                    
                    seen_profile_ids = set()  # Track unique profiles
                    
                    # Fetch ONLY the charging profiles that are in connector.charging_profile
                    for profile_id in connector_charging_profile_ids:
                        # Skip if we've already added this profile
                        if profile_id in seen_profile_ids:
                            continue
                        try:
                            _chargingprofile = ChargingprofileModel.objects.get(chargingprofile_id=profile_id)
                            
                            # Check if charging profile was active during transaction time
                            if _chargingprofile.valid_from is not None and _chargingprofile.valid_to is not None:
                                c_s = _chargingprofile.valid_from.replace(tzinfo=timezone.utc)
                                c_e = _chargingprofile.valid_to.replace(tzinfo=timezone.utc)
                                
                                # Check if charging profile time overlaps with transaction time
                                if (c_e >= t_s and c_s <= t_s) or (c_s >= t_s and c_e <= t_e) or (c_s <= t_s and c_e >= t_e) or (c_s <= t_e and c_e >= t_e):
                                    # Add to transaction's chargingprofile_applied
                                    current_transaction.chargingprofile_applied.append(
                                        serialize_special_types(Chargingprofile16Serializer(_chargingprofile).data)
                                    )
                                    seen_profile_ids.add(profile_id)
                                    ov2xmp_logger.info(f"Added profile {profile_id} to chargingprofile_applied (was active during transaction)")
                                else:
                                    ov2xmp_logger.info(f"Skipped profile {profile_id} - not active during transaction time window")
                            else:
                                # Profile has no validity times - add it anyway since it's in connector.charging_profile
                                current_transaction.chargingprofile_applied.append(
                                    serialize_special_types(Chargingprofile16Serializer(_chargingprofile).data)
                                )
                                seen_profile_ids.add(profile_id)
                                ov2xmp_logger.info(f"Added profile {profile_id} to chargingprofile_applied (no validity times)")
                                
                        except ChargingprofileModel.DoesNotExist:
                            ov2xmp_logger.warning(f"Charging profile {profile_id} not found in database")
                            continue
                    
                    ov2xmp_logger.info(f"Total profiles added to transaction: {len(seen_profile_ids)}")
            
            current_transaction.save()

            # Create and apply CDR
            result, cdr = create_cdr(transaction_id)  # type: ignore
            ov2xmp_logger.info(result)

            if result["success"] and current_transaction.id_tag is not None and cdr is not None:
                apply_cdr(cdr=cdr, user=current_transaction.id_tag.user)

            return call_result.StopTransaction()
        
        except TransactionModel.DoesNotExist:
            ov2xmp_logger.error(f"Transaction {transaction_id} not found")
            return call_result.StopTransaction()
        except DatabaseError as e:
            ov2xmp_logger.error("Connection error with Django DB. The transaction details for # " + str(transaction_id) + " have not been saved.")
            ov2xmp_logger.error(e)
            return call_result.StopTransaction()


    @on(Action.diagnostics_status_notification)
    def on_DiagnosticsStatusNotification(self, status):
        return call_result.DiagnosticsStatusNotification()
    
    
    @on(Action.firmware_status_notification)
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
        connector_id = int(connector_id)
        request = call.RemoteStartTransaction(
            connector_id=connector_id,
            id_tag=id_tag,
            charging_profile=charging_profile
        )
        return await self.call(request)

    # RemoteStopTransaction
    async def remote_stop_transaction(self, transaction_id):
        transaction_id = int(transaction_id)
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
            if response.status == ReservationStatus.accepted:
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
        reservation_id = int(reservation_id)
        request = call.CancelReservation(
            reservation_id=reservation_id
        )
        response = await self.call(request)
        if response is not None:
            if response.status == ReservationStatus.accepted:
                reservation_to_delete = ReservationModel.objects.filter(connector__chargepoint__chargepoint_id=self.id, reservation_id=reservation_id)
                reservation_to_delete.delete()
            return response
        else:
            return None
        
    # ChangeAvailability
    async def change_availability(self, connector_id, availability_type):
        connector_id = int(connector_id)
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
        connector_id = int(connector_id)
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
    async def clear_charging_profile(self, charging_profile_id, connector_id, charging_profile_purpose, stack_level):
        request = call.ClearChargingProfile(
            id = charging_profile_id,
            connector_id = connector_id,
            charging_profile_purpose = charging_profile_purpose,
            stack_level = stack_level)
        return await self.call(request)
        
    #SetChargingProfile
    async def set_charging_profile(self, connector_id, chargingprofile_object):
        charging_profile = chargingprofile16model_to_chargingprofile16type(chargingprofile_object)
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