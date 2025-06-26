from django.db.models.signals import post_save
from django.dispatch import receiver
from connector.models import Connector
from channels.layers import get_channel_layer
import asyncio


@receiver(post_save, sender=Connector, weak=False)
def send_connector_websocket_update(sender, instance, created, **kwargs):

    connector_data = {
        'uuid': str(instance.uuid),
        'connectorid': instance.connectorid,
        'availability_status': instance.availability_status,
        'connector_status': instance.connector_status,
        'chargepoint_id': instance.chargepoint.chargepoint_id,
        'tariff_history': instance.tariff_history,
        'capacity_history': instance.capacity_history,
        'standard': instance.standard,
        'format': instance.format,
        'power_type': instance.power_type,
        'evse_id': instance.evse_id,
        'charging_profile': instance.charging_profile,
    }

    channel_layer = get_channel_layer()

    if channel_layer is not None:
        asyncio.create_task(
            channel_layer.group_send(
                "connector_updates",
                {
                    "type": "connector_update",
                    "data": {
                        "type": "connector_update",
                        "connector": connector_data
                    }
                }
            )
        )
        print(f"Sent connector update via WebSocket: {connector_data}")
    else:
        print(f"[!!] Failed to send connector update via WebSocket, because channel_layer was None. Connector data: {connector_data}")

    #try:
    #    from dso_rest.tasks import process_connector_status_change
    #    print(f"Calling task with data: {connector_data}")
    #    task = process_connector_status_change.delay(connector_data)
    #    print(f"Task called with ID: {task.id}")
    #except Exception as e:
    #    print(f"Error calling task: {str(e)}")
