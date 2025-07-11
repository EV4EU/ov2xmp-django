from celery import shared_task
from celery import current_task
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import os
import logging
logging.basicConfig(level=logging.INFO)


channel_layer = get_channel_layer()
csms_hostname = os.environ["OV2XMP_CSMS_HOSTNAME"]


def send_task_update(message):
    message["task_id"] = current_task.request.id  # type: ignore
    message = json.dumps(message)
    if channel_layer is not None:
        async_to_sync(channel_layer.group_send)\
            ("tasks_updates", {"type": "websocket.send", "text": message})


@shared_task()
def ocpp16_reset_task(chargepoint_id, reset_type):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/reset/" + chargepoint_id, json={"reset_type": reset_type}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_remote_start_transaction(chargepoint_id, connector_id, id_tag, charging_profile):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/remotestarttransaction/" + chargepoint_id, json={"connector_id": connector_id, "id_tag": id_tag, "charging_profile": charging_profile}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_remote_stop_transaction(chargepoint_id, transaction_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/remotestoptransaction/" + chargepoint_id, json={"transaction_id": transaction_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_reserve_now(chargepoint_id, connector_id, id_tag, expiry_date, reservation_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/reservenow/" + chargepoint_id, json={"connector_id": connector_id, "id_tag": id_tag, "expiry_date": expiry_date, "reservation_id": reservation_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_cancel_reservation(chargepoint_id, reservation_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/cancelreservation/" + chargepoint_id, json={"reservation_id": reservation_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_change_availability(chargepoint_id, connector_id, availability_type):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/changeavailability/" + chargepoint_id, json={"connector_id": connector_id, "type": availability_type}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_change_configuration(chargepoint_id, key, value):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/changeconfiguration/" + chargepoint_id, json={"key": key, "value": value}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_clear_cache(chargepoint_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/clearcache/" + chargepoint_id).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_unlock_connector(chargepoint_id, connector_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/unlockconnector/" + chargepoint_id, json={"connector_id": connector_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_configuration(chargepoint_id, keys):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getconfiguration/" + chargepoint_id, json={"keys": keys}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_composite_schedule_task(chargepoint_id, connector_id, duration, charging_rate_unit_type):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getcompositeschedule/" + chargepoint_id, json={"connector_id": connector_id, "duration": duration, "charging_rate_unit": charging_rate_unit_type}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_clear_charging_profile_task(chargepoint_id, charging_profile_id, connector_id, charging_profile_purpose_type, stack_level):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/clearchargingprofile/" + chargepoint_id, json={"charging_profile_id": charging_profile_id,"connector_id": connector_id, "charging_profile_purpose":charging_profile_purpose_type, "stack_level": stack_level}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_set_charging_profile_task(chargepoint_id, connector_id, charging_profile_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/setchargingprofile/" + chargepoint_id, json={"connector_id": connector_id, "charging_profile_id": charging_profile_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_diagnostics_task(chargepoint_id, location, retries, retry_interval, start_time, stop_time):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getdiagnostics/" + chargepoint_id, json={"location": location, "retries": retries, "retry_interval": retry_interval, "start_time": start_time, "stop_time": stop_time}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_update_firmware_task(chargepoint_id, location, retries, retrieve_date, retry_interval):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/updatefirmware/" + chargepoint_id, json={"location": location, "retries": retries, "retrieve_date": retrieve_date, "retry_interval": retry_interval}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_trigger_message_task(chargepoint_id, requested_message, connector_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/triggermessage/" + chargepoint_id, json={"requested_message": requested_message, "connector_id": connector_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_local_list_version_task(chargepoint_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getlocallistversion/" + chargepoint_id).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_send_local_list_task(chargepoint_id, list_version, local_authorization_list, update_type):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/sendlocallist/" + chargepoint_id, json={"list_version": list_version, "local_authorization_list": local_authorization_list, "update_type": update_type}).json()
    send_task_update(message)
    return message


###################################################################################################################################

@shared_task()
def ocpp201_reset(chargepoint_id, reset_type, evse_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/reset/" + chargepoint_id, json={"reset_type": reset_type, "evse_id": evse_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_change_availability(chargepoint_id, operational_status, evse_id, connector_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/changeavailability/" + chargepoint_id, json={"operational_status": operational_status, "evse_id": evse_id, "connector_id": connector_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_clear_cache(chargepoint_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/clearcache/" + chargepoint_id).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_clear_charging_profile(chargepoint_id, charging_profile_id, charging_profile_criteria):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/clearchargingprofile/" + chargepoint_id, json={"charging_profile_id": charging_profile_id, "charging_profile_criteria": charging_profile_criteria}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_clear_display_message(chargepoint_id, id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/cleardisplaymessage/" + chargepoint_id, json={"id": id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_get_charging_profile(chargepoint_id, request_id, evse_id, charging_profile):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/getchargingprofiles/" + chargepoint_id, json={"request_id": request_id, "evse_id": evse_id, "charging_profile": charging_profile}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_get_display_messages(chargepoint_id, request_id, id, priority, state):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/getdisplaymessages/" + chargepoint_id, json={"request_id": request_id, "id": id, "priority": priority, "state": state}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_request_start_transaction(chargepoint_id, id_token, evse_id, remote_start_id, charging_profile_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/requeststarttransaction/" + chargepoint_id, json={"id_token": id_token, "evse_id": evse_id, "remote_start_id": remote_start_id, "charging_profile_id": charging_profile_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_request_stop_transaction(chargepoint_id, transaction_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/requeststoptransaction/" + chargepoint_id, json={"transaction_id": transaction_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_set_charging_profile(chargepoint_id, evse_id, charging_profile_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/setchargingprofile/" + chargepoint_id, json={"evse_id": evse_id, "charging_profile_id": charging_profile_id}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_set_display_message(chargepoint_id, message):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/setdisplaymessage/" + chargepoint_id, json={"message": message}).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_unlock_connector(chargepoint_id, evse_id, connector_id):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/unlockconnector/" + chargepoint_id, json={"evse_id": evse_id, "connector_id": connector_id}).json()
    send_task_update(message)
    return message
