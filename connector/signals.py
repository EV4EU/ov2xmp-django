from django.db.models.signals import post_save
from django.dispatch import receiver
from connector.models import Connector
from channels.layers import get_channel_layer
import asyncio
import logging
import threading

logger = logging.getLogger('ov2xmp')

# Thread-local storage to prevent recursion
_thread_local = threading.local()

def is_signal_processing():
    """Check if signal is currently being processed in this thread"""
    return getattr(_thread_local, 'signal_in_progress', False)

def set_signal_processing(value):
    """Set signal processing state for this thread"""
    _thread_local.signal_in_progress = value

async def send_websocket_update_async(channel_layer, connector_data):
    """Async function to send websocket update"""
    try:
        await channel_layer.group_send(
            "connector_updates",
            {
                "type": "connector_update",
                "data": {
                    "type": "connector_update",
                    "connector": connector_data
                }
            }
        )
        logger.info(f"[SIGNAL] Sent connector update via WebSocket: {connector_data['uuid']}")
    except Exception as e:
        logger.error(f"[SIGNAL] Error sending websocket update: {str(e)}")

def safe_websocket_send(connector_data):
    """Safe websocket message sending"""
    channel_layer = get_channel_layer()
    
    if channel_layer is None:
        logger.warning(f"[SIGNAL] Failed to send connector update - channel_layer is None")
        return
    
    try:
        # Check if there's a running event loop
        try:
            loop = asyncio.get_running_loop()
            # If we're in async context, use create_task
            if loop.is_running():
                asyncio.create_task(send_websocket_update_async(channel_layer, connector_data))
                return
        except RuntimeError:
            # No running loop - continue with sync approach
            pass
        
        # Fallback to sync approach
        from asgiref.sync import async_to_sync
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
        logger.info(f"[SIGNAL] Sent connector update via WebSocket (sync): {connector_data['uuid']}")
        
    except Exception as e:
        logger.error(f"[SIGNAL] Error in websocket update: {str(e)}")

@receiver(post_save, sender=Connector, weak=False)
def send_connector_websocket_update(sender, instance, created, **kwargs):
    # Prevent infinite recursion
    if is_signal_processing():
        logger.debug(f"[SIGNAL] Skipping signal for {instance.uuid} - recursion prevention")
        return
        
    try:
        set_signal_processing(True)
        
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

        # Send websocket update
        safe_websocket_send(connector_data)

        # Check if we should trigger the task - IMPROVED FOR MANUAL TRANSACTIONS
        update_fields = kwargs.get('update_fields', None)
        
        # Handle None update_fields
        if update_fields is None:
            update_fields = []
        else:
            # Convert frozenset to list for easier handling
            update_fields = list(update_fields) if hasattr(update_fields, '__iter__') else []
        
        # IMPROVED LOGIC: Handle manual transaction status changes
        should_trigger_task = (
            not created and  # Don't trigger on creation
            instance.connector_status in ['Charging', 'Reserved', 'Available', 'Finishing',
                                          'Faulted', 'Unavailable', 'SuspendedEVSE', 'SuspendedEV'] and
            (
                # Case 1: Explicit connector_status change
                'connector_status' in update_fields or
                # Case 2: Manual transaction (empty update_fields but status is relevant)
                (len(update_fields) == 0 and 
                 instance.connector_status in ['Charging', 'Reserved', 'Available', 'Finishing',
                                               'Faulted', 'Unavailable', 'SuspendedEVSE', 'SuspendedEV'] and
                 # Don't trigger if it's from our own tasks (they always specify update_fields)
                 not hasattr(_thread_local, 'from_dso_task'))
            ) and
            # Don't trigger if it's a bulk update from our own tasks
            'charging_profile' not in update_fields and
            'capacity_history' not in update_fields and
            'tariff_history' not in update_fields
        )
        
        if should_trigger_task:
            try:
                # Late import to avoid circular imports
                from dso_rest.tasks import process_connector_status_change
                
                logger.info(f"[SIGNAL] Scheduling status change task for {instance.uuid} (Manual transaction detected)")
                task = process_connector_status_change.delay(connector_data)
                logger.info(f"[SIGNAL] Task scheduled with ID: {task.id}")
                
            except Exception as e:
                logger.error(f"[SIGNAL] Error scheduling task: {str(e)}")
        else:
            # Log why we're not triggering
            if created:
                logger.debug(f"[SIGNAL] No task - connector created")
            elif instance.connector_status not in ['Charging', 'Reserved', 'Available', 'Finishing',
                                                    'Faulted', 'Unavailable', 'SuspendedEVSE', 'SuspendedEV']:
                logger.debug(f"[SIGNAL] No task - status not relevant: {instance.connector_status}")
            elif any(field in update_fields for field in ['charging_profile', 'capacity_history', 'tariff_history']):
                logger.debug(f"[SIGNAL] No task - programmatic update. Fields: {update_fields}")
            else:
                logger.debug(f"[SIGNAL] No task - other reason. Fields: {update_fields}, Status: {instance.connector_status}")
                
    except Exception as e:
        logger.error(f"[SIGNAL] Error in signal handler: {str(e)}")
    finally:
        set_signal_processing(False)