from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result, call
import ocpp.v201.enums as ocpp_enums
import ocpp.v201.datatypes as ocpp_datatypes
from ocpp.v201.enums import Action

from chargepoint.models import Chargepoint as ChargepointModel
from idtag.models import IdTag as idTagModel
from users.models import Profile as ProfileModel
from transaction.models import Transaction as TransactionModel
from transaction.models import TransactionStatus
from connector.models import Connector as ConnectorModel
from reservation.models import Reservation as ReservationModel
from statusnotification.models import Statusnotification201 as StatusnotificationModel
from sampledvalue.models import Sampledvalue as SampledvalueModel
from chargingprofile.models import Chargingprofile201 as Chargingprofile201Model
from chargingprofile.serializers import Chargingprofile201Serializer


import uuid
from datetime import datetime, timezone
import json
from channels.layers import get_channel_layer
import logging
from django.core.exceptions import ObjectDoesNotExist
from ocpi.tasks import create_cdr, apply_cdr
from ov2xmp.helpers import get_current_utc_string_without_timezone_offset
from dateutil import parser

channel_layer = get_channel_layer()

ov2xmp_logger = logging.getLogger('ov2xmp')
ov2xmp_logger.setLevel(logging.DEBUG)

async def broadcast_metervalues(message):
    message = json.dumps(message)
    if channel_layer is not None:
        await channel_layer.group_send("metervalues_updates", {"type": "websocket.send", "text": message})

######################################################################################
### Helper functions to proccess meter_value #########################################
def save_metervalues_to_db(meter_value, timestamp, current_transaction):
    for mv in meter_value:
        mv_timestamp = mv.get('timestamp', timestamp)
        sampled_values = mv.get('sampled_value', [])
        
        for sampled_value in sampled_values:
            SampledvalueModel.objects.create(
                transaction=current_transaction,
                timestamp=mv_timestamp,
                value=sampled_value.get("value"),
                context=sampled_value.get('context', None),
                measurand=sampled_value.get("measurand", None),
                phase=sampled_value.get('phase', None),
                location=sampled_value.get('location', None),
                unit=sampled_value.get('unit_of_measure', {}).get('unit', None) if sampled_value.get('unit_of_measure') else None
            )

def get_meter_value_start(meter_value):
    if meter_value and len(meter_value) > 0:
        for mv in meter_value:
            sampled_values = mv.get('sampled_value', [])
            for sv in sampled_values:
                if sv.get('measurand') == 'Energy.Active.Import.Register':
                    meter_start = float(sv.get('value', 0))
                    return meter_start
    return 0

def get_meter_value_last(meter_value):
    for mv in meter_value:
        sampled_values = mv.get('sampled_value', [])
        for sv in sampled_values:
            if sv.get('measurand') == 'Energy.Active.Import.Register':
                wh_meter_last = float(sv.get('value', 0))
                wh_meter_last_timestamp = mv.get('timestamp')
                return wh_meter_last, wh_meter_last_timestamp
    return 0,"0"
###########################################################################################


def authorize_idToken(id_token):
    try:
        idTag_object = idTagModel.objects.get(idToken=id_token)
        user_profile = ProfileModel.objects.get(user=idTag_object.user)
        if not idTag_object.revoked:
            if idTag_object.expiry_date is not None:                    
                if idTag_object.expiry_date.timestamp() > datetime.now(timezone.utc).timestamp():
                    # Check if user has credit
                    if user_profile.credit_balance > 0:
                        return ocpp_enums.AuthorizationStatusEnumType.accepted
                    else:
                        return ocpp_enums.AuthorizationStatusEnumType.no_credit
                else:
                    return ocpp_enums.AuthorizationStatusEnumType.expired
            else:
                return ocpp_enums.AuthorizationStatusEnumType.accepted
        else:
            return ocpp_enums.AuthorizationStatusEnumType.blocked
    except idTagModel.DoesNotExist:
        return ocpp_enums.AuthorizationStatusEnumType.invalid
    

class ChargePoint201(cp):
    ##########################################################################################################################
    ###################  HANDLE INCOMING OCPP MESSAGES #######################################################################
    ##########################################################################################################################

    @on(Action.boot_notification)
    def on_boot_notification(self, charging_station, reason, **kwargs):

        charge_point_serial_number = charging_station.get("serial_number", None)
        chargepoint_model = charging_station["model"]
        firmware_version = charging_station.get("firmware_version", None)
        chargepoint_vendor = charging_station["vendor_name"]

        cp_to_update = ChargepointModel.objects.filter(pk=self.id)
        if cp_to_update:
            cp_to_update.update(
                chargepoint_model = chargepoint_model, 
                chargepoint_vendor = chargepoint_vendor,
                chargepoint_serial_number = charge_point_serial_number,
                firmware_version = firmware_version
            )
            return call_result.BootNotification(
                current_time=get_current_utc_string_without_timezone_offset(),
                interval=10,
                status=ocpp_enums.RegistrationStatusEnumType.accepted,
            )
        else:
            return call_result.BootNotification(
                current_time=get_current_utc_string_without_timezone_offset(),
                interval=10,
                status=ocpp_enums.RegistrationStatusEnumType.rejected,
                status_info=ocpp_datatypes.StatusInfoType(reason_code='-1', additional_info="Rejected because CS is not registered."),
            )
    

    @on(Action.heartbeat)
    def on_heartbeat(self):
        current_cp = ChargepointModel.objects.filter(pk=self.id).get()
        current_cp.last_heartbeat = datetime.now(timezone.utc)
        current_cp.save()

        return call_result.Heartbeat(
            current_time=get_current_utc_string_without_timezone_offset()
        )


    @on(Action.status_notification)
    def on_status_notification(self, timestamp, connector_status, evse_id, connector_id):
        try:
            connector_to_update = ConnectorModel.objects.get(connectorid=connector_id, evse_id=evse_id)
            connector_to_update.connector_status = connector_status
            connector_to_update.save()
        
        except ConnectorModel.DoesNotExist:
            connector_to_update = ConnectorModel.objects.create(
                uuid=uuid.uuid4(),
                connectorid=connector_id,
                connector_status=connector_status,
                evse_id=evse_id
            )
        
        StatusnotificationModel.objects.create(
            connector=connector_to_update,
            connector_status=connector_status,
            timestamp=parser.parse(timestamp),
        )
        
        return call_result.StatusNotification()
    
    # Authorize
    @on(Action.authorize)
    def on_authorize(self, id_token, **kwargs):
        # Extract the actual token value
        if isinstance(id_token, dict):
            token_value = id_token.get('id_token', str(id_token))
        else:
            token_value = str(id_token)
            
        AuthorizationStatus = authorize_idToken(token_value)
        return call_result.Authorize(
            id_token_info=ocpp_datatypes.IdTokenInfoType(
                status=AuthorizationStatus
            )
        )


    # ReportChargingProfiles
    @on(Action.report_charging_profiles)
    async def on_report_charging_profiles(self, request_id, charging_limit_source, tbc, evse_id, charging_profile):
        ov2xmp_logger.info("Received ReportChargingProfiles: " + "Request ID: " + str(request_id) + " | Charging Limit Source: " + charging_limit_source + " | TBC: " + str(tbc) + " | EVSE ID: " + str(evse_id) + " | Charging Profile: " + str(charging_profile))
        return call_result.ReportChargingProfiles()


    # TransactionEvent
    @on(Action.transaction_event)
    async def on_transaction_event(self, event_type, timestamp, trigger_reason, seq_no, transaction_info, evse=None, id_token=None, meter_value=None, id_token_info=None, offline=None, number_of_phases_in_use=None, cable_max_current=None, reservation_id=None):
        
        transaction_id = transaction_info.get('transaction_id') # Note that in OCPP 2.0.1, the transaction ID is provided by the Charging Station. This is required according to the standard, so there is no reason to check whether it has been provided or not.
        if id_token:
            AuthorizationStatus = authorize_idToken(id_token.get('id_token'))
        else:
            AuthorizationStatus = None
        
        ######################################################################################################################################################
        ################################################ S T A R T E D #######################################################################################
        ######################################################################################################################################################
        if event_type == ocpp_enums.TransactionEventEnumType.started:
            
            meter_start = get_meter_value_start(meter_value)
            id_token_object = None
            current_connector = None

            if id_token is not None:
                if AuthorizationStatus != ocpp_enums.AuthorizationStatusEnumType.invalid:  # This means that the id token existed in the database during the authorization, so the get() will not fail. 
                    id_token_object = idTagModel.objects.get(idToken=id_token.get("id_token"))
            
            if evse:
                current_connector = ConnectorModel.objects.get(evse_id=evse["id"], connectorid=evse["connector_id"])
            
            new_transaction = TransactionModel.objects.create(
                uuid=transaction_id,
                start_transaction_timestamp = timestamp,
                wh_meter_start = meter_start,
                wh_meter_last = meter_start,
                wh_meter_last_timestamp = timestamp,
                id_tag = id_token_object,
                connector = current_connector
            )

            save_metervalues_to_db(meter_value, timestamp, new_transaction)

            if AuthorizationStatus:
                return call_result.TransactionEvent(id_token_info=ocpp_datatypes.IdTokenInfoType(status=AuthorizationStatus))
            else:
                return call_result.TransactionEvent()

        ######################################################################################################################################################
        ################################################ U P D A T E D #######################################################################################
        ######################################################################################################################################################

        elif event_type == ocpp_enums.TransactionEventEnumType.updated:
            
            try:
                current_transaction = TransactionModel.objects.get(uuid=transaction_id)
                if AuthorizationStatus == ocpp_enums.AuthorizationStatusEnumType.accepted and id_token is not None:
                    id_token_object = idTagModel.objects.get(idToken=id_token.get("id_token"))
                    current_transaction.id_tag = id_token_object
                    current_transaction.save()
                
                if meter_value is not None:   
                    save_metervalues_to_db(meter_value, timestamp, current_transaction)
                    wh_meter_last, wh_meter_last_timestamp = get_meter_value_last(meter_value)
                    current_transaction.wh_meter_last = wh_meter_last
                    current_transaction.wh_meter_last_timestamp = parser.parse(wh_meter_last_timestamp)
                    current_transaction.save()
                                    
                if AuthorizationStatus:
                    return call_result.TransactionEvent(id_token_info=ocpp_datatypes.IdTokenInfoType(status=AuthorizationStatus))
                else:
                    return call_result.TransactionEvent()

            except ObjectDoesNotExist:
                ov2xmp_logger.error("[!!] Received update for a transaction that does not exist!")
                return call_result.TransactionEvent()

        ######################################################################################################################################################
        ################################################ E N D E D ###########################################################################################
        ######################################################################################################################################################

        elif event_type == ocpp_enums.TransactionEventEnumType.ended:
            
            current_transaction = TransactionModel.objects.get(uuid=transaction_id)
            current_transaction.transaction_status = TransactionStatus.finished
            current_transaction.stop_transaction_timestamp = parser.parse(timestamp)

            save_metervalues_to_db(meter_value, timestamp, current_transaction)

            if meter_value:
                # TODO: Parse signedMeterValue to extract the wh stop value and timestamp
                pass

            result, cdr = create_cdr(transaction_id)  # type: ignore
            ov2xmp_logger.info(result)
            
            if result["success"] and current_transaction.id_tag is not None and cdr is not None:
                apply_cdr(cdr=cdr, user=current_transaction.id_tag.user)
                return call_result.TransactionEvent(
                    total_cost=cdr.total_cost["incl_vat"],
                    id_token_info=id_token_info,
                    updated_personal_message=ocpp_datatypes.MessageContentType(
                        format=ocpp_enums.MessageFormatEnumType.utf8, 
                        content="EV4EU transaction ended"
                    )
                )
            
            if AuthorizationStatus:
                return call_result.TransactionEvent(id_token_info=ocpp_datatypes.IdTokenInfoType(status=AuthorizationStatus))
            else:
                return call_result.TransactionEvent()
    

    ##########################################################################################################################
    #################### ACTIONS INITIATED BY THE CSMS #######################################################################
    ##########################################################################################################################

    # Reset
    async def reset(self, reset_type, evse_id):
        request = call.Reset(type = reset_type, evse_id=evse_id)
        return await self.call(request)


    # ChangeAvailability
    async def change_availability(self, operational_status, evse_id, connector_id):
        request = call.ChangeAvailability(
            operational_status=operational_status,
            evse=ocpp_datatypes.EVSEType(
                id=evse_id,
                connector_id=connector_id
            )
        )
        return await self.call(request)
    
    # ClearCache
    async def clear_cache(self):
        request = call.ClearCache()
        return await self.call(request)

    # ClearChargingProfile
    async def clear_charging_profile(self, chargingprofileid, chargingprofilecriteria):
        request = call.ClearChargingProfile(
            charging_profile_id=chargingprofileid, 
            charging_profile_criteria=chargingprofilecriteria
        )
        return await self.call(request)
    
    # ClearDisplayMessage
    async def clear_display_message(self, id):
        request = call.ClearDisplayMessage(
            id=id
        )
        return await self.call(request)

    # GetChargingProfiles
    async def get_charging_profiles(self, request_id, evse_id, charging_profile):
        request = call.GetChargingProfiles(
            request_id=request_id,
            evse_id=evse_id,
            charging_profile=charging_profile
        )
        return await self.call(request)

    # GetDisplayMessages
    async def get_display_messages(self, id, request_id, priority, state):
        request = call.GetDisplayMessages(
            id=id,
            request_id=request_id,
            priority=priority,
            state=state
        )
        return await self.call(request)

    # RequestStartTransaction
    async def request_start_transaction(self, id_token, evse_id, remote_start_id, charging_profile_id):
        
        try:
            charging_profile = Chargingprofile201Model.objects.get(chargingprofile_id=charging_profile_id)
            charging_profile = None   # TODO: We need a function that receives a charging profile object and returns a ChargingProfileType.
        except ObjectDoesNotExist:
            charging_profile = None
        
        request = call.RequestStartTransaction(
            evse_id=evse_id,
            remote_start_id=remote_start_id,
            id_token=id_token,
            charging_profile=charging_profile,
            group_id_token=None
        )
        return await self.call(request)


    # RequestStopTransaction
    async def request_stop_transaction(self, transaction_id):

        request = call.RequestStopTransaction(
            transaction_id=transaction_id
        )
        return await self.call(request)


    # SetChargingProfile
    async def set_charging_profile(self, evse_id, charging_profile):
        request = call.SetChargingProfile(
            evse_id=evse_id,
            charging_profile=charging_profile
        )
        return await self.call(request)
    

    # SetDisplayMessage
    async def set_display_message(self, message):
        request = call.SetDisplayMessage(
            message=message
        )
        return await self.call(request)
    
    
    # UnlockConnector
    async def unlock_connector(self, evse_id, connector_id):
        request = call.UnlockConnector(
            evse_id=evse_id,
            connector_id=connector_id
        )
        return await self.call(request)
