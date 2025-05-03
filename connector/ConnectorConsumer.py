from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Connector
from channels.layers import get_channel_layer

class ConnectorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Called when a WebSocket connection is established
        """
        # Join the connector updates group
        await self.channel_layer.group_add(
            "connector_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed
        """
        await self.channel_layer.group_discard(
            "connector_updates",
            self.channel_name
        )

    async def connector_update(self, event):
        """
        Handler for connector update events
        """
        # Send the update to the WebSocket
        await self.send(text_data=json.dumps(event['data']))

@receiver(post_save, sender=Connector)
def connector_changed(sender, instance, created, **kwargs):
    print("Signal handler triggered")
    
    connector_data = {
        'uuid': str(instance.uuid),
        'connectorid': instance.connectorid,
        'availability_status': instance.availability_status,
        'connector_status': instance.connector_status,
        'chargepoint_id': instance.chargepoint.chargepoint_id,
        'tariff_history': instance.tariff_history,
        'capacity_history': instance.capacity_history
    }

    # WebSocket update
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "connector_updates",
        {
            "type": "connector_update",
            "data": {
                "type": "connector_update",
                "connector": connector_data
            }
        }
    )
    
    # Task call with error handling
    try:
        from dso_rest.tasks import process_connector_status_change
        print(f"Calling task with data: {connector_data}")
        task = process_connector_status_change.delay(connector_data)
        print(f"Task called with ID: {task.id}")
    except Exception as e:
        print(f"Error calling task: {str(e)}")

   