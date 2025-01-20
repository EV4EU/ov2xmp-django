from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import os
import logging
logging.basicConfig(level=logging.INFO)
from ocpp_rest.tasks import send_task_update




from time import sleep
import logging
from chargepoint.models import Chargepoint
from location.models import Location
from connector.models import Connector

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()
csms_hostname = os.environ["OV2XMP_CSMS_HOSTNAME"]


#@shared_task()
#def process_dso_signal(dso_signal):
#
#    # Check if chargingprofiles already exist that satisfy the specified capacity limits
#        # If not, then create corresponding chargingprofiles
#    
#    # Based on the locations, find the corresponding charging stations
#
#    # Apply the new chargingprofiles or those that already exist
#
#    return "Test API"

#@shared_task()
#def process_dso_signal(dso_signal):
#    # Process the DSO signal
#    message = "Signal received and processed: " + str(dso_signal)
#
#    # Send message to WebSocket
#    async_to_sync(channel_layer.group_send)(
#        "dso_signal_dso_signal_room",  # WebSocket room group
#        {
#            "type": "send_message",
#            "message": message,
#        }
#    )
#
#    return message



# Apply DSO Charging Schedule
def dso_scedule_details(substation_list):

    
    print(substation_list)


# Connnector Finder
def connector_finder(chargepoint_list):

    Substation_List=[]
    chargepoint_list=sorted(chargepoint_list)
    for chargepoint_name in chargepoint_list:
        connectors = Connector.objects.filter(chargepoint=chargepoint_name)
        connectors = list(connectors.values_list('connectorid', flat=True))
        
        connectors=sorted(connectors)
        

        Substation_List.append([chargepoint_name,connectors])

    return Substation_List


# Chargepoint Finder function
def chargepoint_finder(structured_message):

    transformer_id_signal = structured_message.get("transformerID")

    # Log the received message
    #logger.info(f"Processing signal for transformer ID: {transformer_id_signal}")

    # Check if the transformer exists in the database
    try:
        #transformer = Transformer.objects.get(transformer_id=transformer_id_signal)
        
        location_transformer = Location.objects.filter(substation_id=transformer_id_signal)
        
        if location_transformer.exists():
            # Extract and convert to a list of desired values (e.g., IDs or names)
            location_ids = list(location_transformer.values_list('id', flat=True))
            #logger.info(f"Transformer associated locations (IDs): {location_ids}")

            #print(type(location_ids)) # It is a list of 3 locations
            chargepoint_list=[]
            for ii_location in location_ids:

                chargepoint_value = Chargepoint.objects.filter(location=ii_location)
                if chargepoint_value.exists():
                    chargepoint_id = list(chargepoint_value.values_list('chargepoint_id', flat=True))
                    chargepoint_list.append(chargepoint_id)
            
            # Flatten the nested list
            chargepoint_list = [item for sublist in chargepoint_list for item in sublist]
            #print(chargepoint_list) # A list with the Chargepoint names inside

            return chargepoint_list



        else:
            logger.warning(f"No locations found for transformer ID: {transformer_id_signal}.")


    except transformer_id_signal.DoesNotExist:
        logger.error(f"Transformer with ID {transformer_id_signal} does not exist.")
    except Exception as e:
        logger.exception(f"Unexpected error occurred during scheduling: {e}")


@shared_task()
def process_dso_signal(dso_signal):
    # Structure the data as a JSON object
    structured_message = {
        "message": "Signal received and processed",
        "id": dso_signal.get("id"),
        "uuId": dso_signal.get("uuId"),
        "uuName": dso_signal.get("uuName"),
        "transformerID": dso_signal.get("transformerID"),
        "event_timestamp": dso_signal.get("event_timestamp"),
        "locationCoords": dso_signal.get("locationCoords"),
        "locationName": dso_signal.get("locationName"),
        "duration": dso_signal.get("duration"),
        "period": dso_signal.get("period"),
        "sync": dso_signal.get("sync"),
    }

    
    # Calling Chargepoint Finder fro the DSS Signal
    chargepoint_list=chargepoint_finder(structured_message)
    logger.info(f'With Transformer_id: {structured_message.get("transformerID")}, we have these Chargepoints: {chargepoint_list}')


    substation_list=connector_finder(chargepoint_list)
    
    dso_scedule_details(substation_list)






    # Send structured message to WebSocket
    async_to_sync(channel_layer.group_send)(
        "dso_signal_dso_signal_room",  # WebSocket room group
        {
            "type": "send_message",
            "message": structured_message,  # Send the structured data
        }
    )
    
    return structured_message









########## Task for auto updating the charging shcedules etc.

@shared_task
def periodic_test_task():
    try:
        # Perform updates or other logic here
        logger.info(f'Updaaaa')
        # Sleep to allow system resources to be freed
       
    except Exception as e:
        logger.info(f"Error updating variables: {e}")
