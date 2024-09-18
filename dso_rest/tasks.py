from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import os
import logging
logging.basicConfig(level=logging.INFO)
from ocpp_rest.tasks import send_task_update


channel_layer = get_channel_layer()
csms_hostname = os.environ["OV2XMP_CSMS_HOSTNAME"]


@shared_task()
def process_dso_signal(dso_signal):

    # Check if chargingprofiles already exist that satisfy the specified capacity limits
        # If not, then create corresponding chargingprofiles
    
    # Based on the locations, find the corresponding charging stations

    # Apply the new chargingprofiles or those that already exist

    return "Test API"

