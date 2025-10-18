from datetime import datetime
from connector.models import Connector
import logging

logger = logging.getLogger('ov2xmp')

def update_history(history, time_range, new_value):
    """
    Update history with the new value for the given time range.
    Handles time ranges that span across midnight.
    """
    logger.info(f"[UPDATE_HISTORY] Called with time_range: {time_range}, new_value: {new_value}")
    logger.info(f"[UPDATE_HISTORY] Input history type: {type(history)}")
    
    # Ensure history is a valid dictionary
    if history is None:
        logger.warning("[UPDATE_HISTORY] History is None, initializing with defaults")
        history = default_capacity_history() if isinstance(new_value, (int, float)) and new_value > 1 else default_tariff_history()
    elif not isinstance(history, dict):
        logger.warning(f"[UPDATE_HISTORY] History is not a dict (type: {type(history)}), initializing")
        history = default_capacity_history() if isinstance(new_value, (int, float)) and new_value > 1 else default_tariff_history()
    
    start_time, end_time = time_range.split("-")
    start_dt = datetime.strptime(start_time, "%H:%M").time()
    end_dt = datetime.strptime(end_time, "%H:%M").time()

    if end_dt < start_dt:
        logger.info("[UPDATE_HISTORY] Time range spans midnight - splitting")
        history = update_history_for_range(history, f"{start_time}-23:59", new_value)
        history = update_history_for_range(history, f"00:00-{end_time}", new_value)
    else:
        history = update_history_for_range(history, time_range, new_value)

    updated_count = len([k for k, v in history.items() if v == new_value])
    logger.info(f"[UPDATE_HISTORY] Final result: {updated_count} slots updated to value {new_value}")
    return history


def update_history_for_range(history, time_range, new_value):
    """
    FIXED: Helper function to update history for a given time range.
    Updates all slots that OVERLAP with the given time range.
    """
    logger.info(f"[UPDATE_RANGE] Processing range: {time_range} with value: {new_value}")
    
    start_time, end_time = time_range.split("-")
    start_dt = datetime.strptime(start_time, "%H:%M").time()
    end_dt = datetime.strptime(end_time, "%H:%M").time()
    
    updated_slots = []
    total_slots = len(history)
    
    for key in list(history.keys()):
        key_start, key_end = key.split("-")
        key_start_dt = datetime.strptime(key_start, "%H:%M").time()
        
        # Handle midnight boundary (00:00 represents end of day)
        if key_end == "00:00":
            key_end_dt = datetime.strptime("23:59", "%H:%M").time()
        else:
            key_end_dt = datetime.strptime(key_end, "%H:%M").time()

        # FIXED OVERLAP LOGIC: Check if ranges overlap
        # Two ranges overlap if: start1 < end2 AND start2 < end1
        overlaps = False
        
        # Primary overlap check
        if start_dt < key_end_dt and key_start_dt < end_dt:
            overlaps = True
            
        # Handle exact boundary matches
        if start_dt == key_start_dt or end_dt == key_end_dt:
            overlaps = True
        
        # Special case for slots ending at midnight
        if key_end == "00:00" and end_dt >= datetime.strptime("23:55", "%H:%M").time():
            overlaps = True

        if overlaps:
            old_value = history[key]
            history[key] = new_value
            updated_slots.append(key)
            logger.info(f"[UPDATE_RANGE] ✓ Updated {key}: {old_value} -> {new_value}")
    
    logger.info(f"[UPDATE_RANGE] Updated {len(updated_slots)}/{total_slots} slots: {updated_slots}")
    
    if len(updated_slots) == 0:
        logger.warning(f"[UPDATE_RANGE] WARNING: No slots updated for range {time_range}")
        logger.warning(f"[UPDATE_RANGE] Available slots sample: {list(history.keys())[:10]}")  # Show more samples
    
    return history


def default_tariff_history():
    """Generate default tariff history with 5-minute slots for 24 hours (288 slots)"""
    time_ranges = {}
    for h in range(24):
        for m in range(0, 60, 5):  # Every 5 minutes: 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55
            start_time = f"{h:02d}:{m:02d}"
            
            # Calculate end time
            end_minute = m + 5
            end_hour = h
            
            if end_minute >= 60:
                end_minute = 0
                end_hour = h + 1
            
            # Fix the "24:00" issue
            if end_hour == 24:
                end_hour = 0  # Convert to "00"
            
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            time_ranges[f"{start_time}-{end_time}"] = 0.09
    return time_ranges


def default_capacity_history():
    """Generate default capacity history with 5-minute slots for 24 hours (288 slots)"""
    time_ranges = {}
    for h in range(24):
        for m in range(0, 60, 5):  # Every 5 minutes: 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55
            start_time = f"{h:02d}:{m:02d}"
            
            # Calculate end time
            end_minute = m + 5
            end_hour = h
            
            if end_minute >= 60:
                end_minute = 0
                end_hour = h + 1

            # Fix the "24:00" issue
            if end_hour == 24:
                end_hour = 0  # Convert to "00"
            
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            time_ranges[f"{start_time}-{end_time}"] = 11
    return time_ranges


def update_connectors():
    """Ensure existing connectors have proper history with 5-minute intervals"""
    updated_count = 0
    for connector in Connector.objects.all():
        needs_update = False
        
        # Check if connector has old 30-minute format or incorrect format
        if (not connector.tariff_history or 
            len(connector.tariff_history) != 288 or  # Should have 288 slots now
            "23:30-24:00" in connector.tariff_history or  # Old format indicator
            any("30-" in k or "-30" in k for k in connector.tariff_history.keys() if ":" in k)):  # Old 30-minute slots
            connector.tariff_history = default_tariff_history()
            needs_update = True
            logger.info(f"Updated tariff history for connector {connector.uuid}")

        if (not connector.capacity_history or 
            len(connector.capacity_history) != 288 or  # Should have 288 slots now
            "23:30-24:00" in connector.capacity_history or  # Old format indicator
            any("30-" in k or "-30" in k for k in connector.capacity_history.keys() if ":" in k)):  # Old 30-minute slots
            connector.capacity_history = default_capacity_history()
            needs_update = True
            logger.info(f"Updated capacity history for connector {connector.uuid}")
        
        if needs_update:
            connector.save(update_fields=["tariff_history", "capacity_history"])
            updated_count += 1

    logger.info(f"Updated {updated_count} connectors with corrected 5-minute interval history.")
    return updated_count


def test_update_logic():
    """Test the update logic with 5-minute intervals"""
    logger.info("=== TESTING UPDATE LOGIC WITH 5-MINUTE INTERVALS ===")
    
    # Test with actual time range
    test_history = default_capacity_history()
    test_range = "16:05-16:10"  # Your actual DSO signal time
    test_value = 15.0  # Your actual DSO signal value
    
    logger.info(f"Testing range: {test_range} with value: {test_value}")
    logger.info(f"Total slots in history: {len(test_history)}")
    logger.info("Before update - slots around 16:xx:")
    count_16 = 0
    for k, v in test_history.items():
        if "16:" in k:
            logger.info(f"  {k}: {v}")
            count_16 += 1
    logger.info(f"Found {count_16} slots for hour 16")
    
    # Apply the update
    updated_history = update_history(test_history, test_range, test_value)
    
    logger.info("After update - slots around 16:xx:")
    updated_count = 0
    for k, v in updated_history.items():
        if "16:" in k:
            logger.info(f"  {k}: {v}")
            if v == test_value:
                updated_count += 1
    
    logger.info(f"Test Result: {updated_count} slots updated")
    logger.info("=== TEST COMPLETE ===")
    return updated_count > 0


def reinitialize_all_connectors():
    """
    Force reinitialize all connectors with new 5-minute interval structure.
    This function should be called as a one-time migration after code deployment.
    """
    logger.info("=== STARTING CONNECTOR REINITIALIZATION ===")
    
    total_connectors = Connector.objects.count()
    logger.info(f"Found {total_connectors} connectors to update")
    
    updated_count = 0
    
    for connector in Connector.objects.all():
        try:
            # Always update to new 5-minute format
            old_tariff_count = len(connector.tariff_history) if connector.tariff_history else 0
            old_capacity_count = len(connector.capacity_history) if connector.capacity_history else 0
            
            connector.tariff_history = default_tariff_history()
            connector.capacity_history = default_capacity_history()
            
            connector.save(update_fields=["tariff_history", "capacity_history"])
            updated_count += 1
            
            logger.info(f"✓ Updated connector {connector.uuid}")
            logger.info(f"  - Tariff slots: {old_tariff_count} → {len(connector.tariff_history)}")
            logger.info(f"  - Capacity slots: {old_capacity_count} → {len(connector.capacity_history)}")
            
        except Exception as e:
            logger.error(f"✗ Failed to update connector {connector.uuid}: {str(e)}")
    
    logger.info(f"=== REINITIALIZATION COMPLETE: {updated_count}/{total_connectors} connectors updated ===")
    return updated_count