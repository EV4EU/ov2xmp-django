import os, re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ov2xmp.settings")
import django
django.setup()
from django.conf import settings
from chargepoint.models import Chargepoint as ChargepointModel
from chargingprofile.models import Chargingprofile as ChargingprofileModel
from chargepoint.models import OcppProtocols
from ocpp.v16.enums import ChargePointStatus
from chargepoint.ChargePoint16 import ChargePoint16
from api.serializers import CSMS_MESSAGE_CODE
from chargepoint.ChargePoint201 import ChargePoint201

import asyncio
from asgiref.sync import sync_to_async

from sanic import Sanic, Request, Websocket
from sanic.log import logger
from sanic import json
from sanic.response import json as json_resp
from dataclasses import asdict, is_dataclass
import logging
logging.basicConfig(level=logging.INFO)
app = Sanic(__name__)

app.ctx.CHARGEPOINTS_V16 = {}
app.ctx.CHARGEPOINTS_V201 = {}
app.config.FALLBACK_ERROR_FORMAT = "json"
app.config.WEBSOCKET_PING_INTERVAL = 0  # Disable Websocket ping/pong, since some EV chargers do not respond to pings.

from logstash_async.handler import AsynchronousLogstashHandler

if int(os.environ["OV2XMP_LOGSTASH_ENABLE"]):
    handler = AsynchronousLogstashHandler(
        host=os.environ["OV2XMP_LOGSTASH_HOST"],
        port=int(os.environ["OV2XMP_LOGSTASH_PORT"]),
        database_path='logstash_test.db'
    )
    ocpp_logger = logging.getLogger("ocpp")
    ocpp_logger.addHandler(handler)

OV2XMP_OCPP_TIMEOUT = int(os.environ.get("OV2XMP_OCPP_TIMEOUT", 30))
OV2XMP_OCPP_PREREGISTRATION_EVCS = bool(int(os.environ.get("OV2XMP_OCPP_PREREGISTRATION_EVCS", 0)))


# json() function of Sanic compatible with dataclasses returned by the ocpp library
def json_ocpp(input):
    if type(input) is not CSMS_MESSAGE_CODE:
        if is_dataclass(input):
            return json({"message_code": CSMS_MESSAGE_CODE.RESPONSE_RECEIVED.name, "message": asdict(input)})
        else:
            return json({"message_code": CSMS_MESSAGE_CODE.RESPONSE_RECEIVED.name, "message": input})
    else:
        if input == CSMS_MESSAGE_CODE.CHARGING_PROFILE_DOES_NOT_EXIST:
            return json({"message_code": CSMS_MESSAGE_CODE.CHARGING_PROFILE_DOES_NOT_EXIST.name, "message": CSMS_MESSAGE_CODE.CHARGING_PROFILE_DOES_NOT_EXIST.value})
        elif input == CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST:
            return json({"message_code": CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST.name, "message": CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST.value})


###################################################################################################
############################# CSMS REST API - OCPP 1.6 ############################################
###################################################################################################

# Reset (hard or soft)
@app.route("/ocpp16/reset/<chargepoint_id:str>", methods=["POST"])
async def reset(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        resetType = request.json["reset_type"]
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].reset(resetType)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# RemoteStartTransaction  
@app.route("/ocpp16/remotestarttransaction/<chargepoint_id:str>", methods=["POST"])
async def remote_start_transaction(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        connector_id = request.json['connector_id']
        connector_id = int(connector_id)
        id_tag = request.json['id_tag']
        charging_profile = request.json['charging_profile']
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].remote_start_transaction(id_tag, connector_id, charging_profile)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# RemoteStopTransaction  
@app.route("/ocpp16/remotestoptransaction/<chargepoint_id:str>", methods=["POST"])
async def remote_stop_transaction(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        transaction_id = request.json['transaction_id']
        transaction_id = int(transaction_id)
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].remote_stop_transaction(transaction_id)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# ReserveNow
@app.route("/ocpp16/reservenow/<chargepoint_id:str>", methods=["POST"])
async def reserve_now(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        connector_id = request.json['connector_id']
        id_tag = request.json['id_tag']
        expiry_date = request.json['expiry_date']
        reservation_id = request.json['reservation_id']
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].reserve_now(connector_id, id_tag, expiry_date, reservation_id)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# CancelReservation
@app.route("/ocpp16/cancelreservation/<chargepoint_id:str>", methods=["POST"])
async def cancel_reservation(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        reservation_id = request.json['reservation_id']
        reservation_id = int(reservation_id)
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].cancel_reservation(reservation_id)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# ChangeAvailability
@app.route("/ocpp16/changeavailability/<chargepoint_id:str>", methods=["POST"])
async def change_availability(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        connector_id = request.json['connector_id']
        connector_id = int(connector_id)
        availability_type = request.json['type']
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].change_availability(connector_id, availability_type)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)

# ChangeConfiguration
@app.route("/ocpp16/changeconfiguration/<chargepoint_id:str>", methods=["POST"])
async def change_configuration(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        key = request.json['key']
        value = request.json['value']
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].change_configuration(key, value)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# ClearCache
@app.route("/ocpp16/clearcache/<chargepoint_id:str>", methods=["POST"])
async def clear_cache(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16:
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].clear_cache()
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# UnlockConnector
@app.route("/ocpp16/unlockconnector/<chargepoint_id:str>", methods=["POST"])
async def unlock_connector(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        connector_id = request.json['connector_id']
        connector_id = int(connector_id)
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].unlock_connector(connector_id)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# GetConfiguration
@app.route("/ocpp16/getconfiguration/<chargepoint_id:str>", methods=["POST"])
async def get_configuration(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        keys = request.json['keys']
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].get_configuration(keys)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# GetCompositeSchedule
@app.route("/ocpp16/getcompositeschedule/<chargepoint_id:str>", methods=["POST"])
async def get_composite_schedule(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        connector_id = request.json["connector_id"]
        duration = request.json["duration"]
        charging_rate_unit_type= request.json["charging_rate_unit"]
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].get_composite_schedule(connector_id, duration, charging_rate_unit_type)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# ClearChargingProfile
@app.route("/ocpp16/clearchargingprofile/<chargepoint_id:str>", methods=["POST"])
async def clear_charging_profile(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        charging_profile_id=request.json["charging_profile_id"]
        connector_id = request.json["connector_id"]
        charging_profile_purpose_type= request.json["charging_profile_purpose"]
        stack_level= request.json["stack_level"]
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].clear_charging_profile(charging_profile_id, connector_id, charging_profile_purpose_type, stack_level)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# SetChargingProfile
@app.route("/ocpp16/setchargingprofile/<chargepoint_id:str>", methods=["POST"])
async def set_charging_profile(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        connector_id = request.json["connector_id"]
        charging_profile_id = request.json["charging_profile_id"]
        try:
            chargingprofile_object = ChargingprofileModel.objects.get(pk=charging_profile_id)
            chargingprofile = {
                "chargingProfileId": chargingprofile_object.chargingprofile_id,
                "stackLevel": chargingprofile_object.stack_level,
                "chargingProfilePurpose": chargingprofile_object.chargingprofile_purpose,
                "chargingProfileKind": chargingprofile_object.chargingprofile_kind,
                "chargingSchedule": {
                    "chargingSchedulePeriod": chargingprofile_object.chargingschedule_period,
                    "chargingRateUnit": chargingprofile_object.charging_rate_unit
                }
            }

            if hasattr(chargingprofile_object, 'transaction_id'):
                if chargingprofile_object.transaction_id is not None:
                    chargingprofile["transactionId"] = chargingprofile_object.transaction_id
            
            if chargingprofile_object.recurrency_kind is not None:
                chargingprofile["recurrencyKind"] = chargingprofile_object.recurrency_kind

            if chargingprofile_object.valid_from is not None:
                chargingprofile["validFrom"] = chargingprofile_object.valid_from.now().isoformat()

            if chargingprofile_object.valid_to is not None:
                chargingprofile["validTo"] = chargingprofile_object.valid_to.now().isoformat()
            
            if chargingprofile_object.duration is not None:
                chargingprofile["chargingSchedule"]["duration"] = chargingprofile_object.duration

            if chargingprofile_object.start_schedule is not None:
                chargingprofile["chargingSchedule"]["startSchedule"] = chargingprofile_object.start_schedule.now().isoformat()
            
            if chargingprofile_object.min_charging_rate is not None:
                chargingprofile["chargingSchedule"]["minChargingRate"] = float(chargingprofile_object.min_charging_rate)

            result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].set_charging_profile(connector_id, chargingprofile)
            return json_ocpp(result)
        except ChargingprofileModel.DoesNotExist:
            return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_PROFILE_DOES_NOT_EXIST)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# GetDiagnostics
@app.route("/ocpp16/getdiagnostics/<chargepoint_id:str>", methods=["POST"])
async def get_diagnostics(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        location = request.json["location"]
        retries = request.json["retries"]
        retry_interval = request.json["retry_interval"]
        start_time = request.json["start_time"]
        stop_time = request.json["stop_time"]
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].get_diagnostics(location, retries, retry_interval, start_time, stop_time)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# UpdateFirmware
@app.route("/ocpp16/updatefirmware/<chargepoint_id:str>", methods=["POST"])
async def update_firmware(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        location = request.json["location"]
        retries = request.json["retries"]
        retrieve_date = request.json["retrieve_date"]
        retry_interval = request.json["retry_interval"]
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].update_firmware(location, retries, retrieve_date, retry_interval)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


# TriggerMessage
@app.route("/ocpp16/triggermessage/<chargepoint_id:str>", methods=["POST"])
async def trigger_message(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        requested_message = request.json["requested_message"]
        connector_id = request.json["connector_id"]
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].trigger_message(requested_message, connector_id)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


#GetLocalListVersion
@app.route("/ocpp16/getlocallistversion/<chargepoint_id:str>", methods=["POST"])
async def get_local_list_version(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 is not None:
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].get_local_list_version()
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)


#SendLocalList
@app.route("/ocpp16/sendlocallist/<chargepoint_id:str>", methods=["POST"])
async def send_local_list(request: Request, chargepoint_id: str):
    if chargepoint_id in app.ctx.CHARGEPOINTS_V16 and request.json is not None:
        list_version = request.json["list_version"]
        local_authorization_list = request.json["local_authorization_list"]
        update_type = request.json["update_type"]
        result = await app.ctx.CHARGEPOINTS_V16[chargepoint_id].send_local_list(list_version, local_authorization_list, update_type)
        return json_ocpp(result)
    else:
        return json_ocpp(CSMS_MESSAGE_CODE.CHARGING_STATION_DOES_NOT_EXIST)

###################################################################################################
############################ CSMS REST API - OCPP 2.0.1 ###########################################
###################################################################################################

#ReserveNow - OCPP 2.0.1
@app.route("/ocpp201/reservenow/<chargepoint_id:str>", methods=["POST"])
async def ocpp201_reserve_now(request: Request, chargepoint_id: str):
    pass


#CancelReservation - OCPP 2.0.1
@app.route("/ocpp201/cancelreservation/<chargepoint_id:str>", methods=["POST"])
async def ocpp201_cancel_reservation(request: Request, chargepoint_id: str):
    pass


#GetCompositeSchedule - OCPP 2.0.1
@app.route("/ocpp201/getcompositeschedule/<chargepoint_id:str>", methods=["POST"])
async def ocpp201_get_composite_schedule(request: Request, chargepoint_id: str):
    pass


#SetChargingProfile - OCPP 2.0.1
@app.route("/ocpp201/setchargingprofile/<chargepoint_id:str>", methods=["POST"])
async def ocpp201_set_charging_profile(request: Request, chargepoint_id: str):
    pass

###################################################################################################
################################## Websocket Handler ##############################################
###################################################################################################

@app.middleware('request')
async def evcs_validation_middleware(request: Request):
    """
    This middleware contains code that activates first when we receive a WebSocket request from an EV Charger.
    Purpose of this middleware is to check whether the EVCS with the given ID, already exists in the Django DB.
    This security check is performed if OV2XMP_OCPP_PREREGISTRATION_EVCS is 1. If OV2XMP_OCPP_PREREGISTRATION_EVCS is 0,
    then the registration status is ignored, and the handshake continues.
    """
    request_url = request.raw_url.decode()

    result = re.search(r'\/ws\/ocpp\/(.*)', request_url)
    if result:
        charge_point_id = result.group(1)
        new_chargepoint = await sync_to_async(ChargepointModel.objects.filter, thread_sensitive=True)(pk=charge_point_id)

        if OV2XMP_OCPP_PREREGISTRATION_EVCS and not (await sync_to_async(new_chargepoint.exists, thread_sensitive=True)()):
            logger.error("EV Charging Station not found: %s, from: %s", charge_point_id, request.ip)
            return json('EV Charging Station not found', status=404)


@app.websocket("/ws/ocpp/<charge_point_id:str>", subprotocols=['ocpp1.6', 'ocpp2.0.1'])
async def on_connect(request: Request, websocket: Websocket, charge_point_id: str):
    # For every new charge point that connects, create a ChargePoint instance and start listening for messages.
     
    logger.info("Protocols Matched: %s", websocket.subprotocol)
    logger.info("Charge Point connected: %s, from: %s", charge_point_id, request.ip)

    if websocket.subprotocol == 'ocpp1.6':
        cp = ChargePoint16(charge_point_id, websocket, response_timeout=OV2XMP_OCPP_TIMEOUT)
        app.ctx.CHARGEPOINTS_V16.update({charge_point_id: cp})
        ocpp_version = OcppProtocols.ocpp16
    elif websocket.subprotocol == 'ocpp2.0.1':
        cp = ChargePoint201(charge_point_id, websocket, response_timeout=OV2XMP_OCPP_TIMEOUT)
        app.ctx.CHARGEPOINTS_V201.update({charge_point_id: cp})
        ocpp_version = OcppProtocols.ocpp201
    else:
        logger.error("No subprotocol defined - Aborting connection.")
        return json_resp({"error": "Unauthorized"}, status=400)
    
    new_chargepoint = await sync_to_async(ChargepointModel.objects.filter, thread_sensitive=True)(pk=charge_point_id)
    
    if not (await sync_to_async(new_chargepoint.exists, thread_sensitive=True)()):
        await ChargepointModel.objects.acreate(chargepoint_id = charge_point_id, 
                                                ocpp_version=ocpp_version,
                                                chargepoint_status=ChargePointStatus.available.value,  # type: ignore
                                                ip_address=request.ip,
                                                websocket_port=request.port)
    else:
        await new_chargepoint.aupdate(connected=True, chargepoint_status=ChargePointStatus.available.value) # type: ignore
    try:
        await cp.start()

    except asyncio.exceptions.CancelledError:
        logger.error("Disconnected from CP: %s", charge_point_id)        
        if isinstance(cp, ChargePoint16):
            ChargepointModel.objects.filter(pk=charge_point_id).update(connected=False, chargepoint_status=ChargePointStatus.unavailable.value) # type: ignore
            app.ctx.CHARGEPOINTS_V16[charge_point_id]._connection.fail_connection()  # Ungracefully close the Websocket connection so that the CP tries to reconnect
        elif isinstance(cp, ChargePoint201):
            ChargepointModel.objects.filter(pk=charge_point_id).update(connected=False, chargepoint_status=ChargePointStatus.unavailable.value) # type: ignore
            app.ctx.CHARGEPOINTS_V201[charge_point_id]._connection.fail_connection()  # Ungracefully close the Websocket connection so that the CP tries to reconnect
