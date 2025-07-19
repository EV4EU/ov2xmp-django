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
def ocpp16_reset_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/reset/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_remote_start_transaction(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/remotestarttransaction/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_remote_stop_transaction(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/remotestoptransaction/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_reserve_now(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/reservenow/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_cancel_reservation(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/cancelreservation/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_change_availability(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/changeavailability/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_change_configuration(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/changeconfiguration/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_clear_cache(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/clearcache/" + data['chargepoint_id']).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_unlock_connector(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/unlockconnector/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_configuration(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getconfiguration/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_composite_schedule_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getcompositeschedule/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_clear_charging_profile_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/clearchargingprofile/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_set_charging_profile_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/setchargingprofile/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_diagnostics_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getdiagnostics/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_update_firmware_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/updatefirmware/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_trigger_message_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/triggermessage/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_get_local_list_version_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/getlocallistversion/" + data['chargepoint_id']).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp16_send_local_list_task(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp16/sendlocallist/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


###################################################################################################################################

@shared_task()
def ocpp201_reset(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/reset/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_change_availability(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/changeavailability/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_clear_cache(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/clearcache/" + data['chargepoint_id']).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_clear_charging_profile(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/clearchargingprofile/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_clear_display_message(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/cleardisplaymessage/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_get_charging_profile(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/getchargingprofiles/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_get_display_messages(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/getdisplaymessages/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_request_start_transaction(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/requeststarttransaction/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_request_stop_transaction(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/requeststoptransaction/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_set_charging_profile(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/setchargingprofile/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_set_display_message(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/setdisplaymessage/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message


@shared_task()
def ocpp201_unlock_connector(data):
    message = requests.post("http://" + csms_hostname + ":9000/ocpp201/unlockconnector/" + data['chargepoint_id'], json=data).json()
    send_task_update(message)
    return message
