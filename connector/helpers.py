from datetime import datetime
from connector.models import Connector


def update_history(history, time_range, new_value):
    """
    Update history with the new value for the given time range.
    Handles time ranges that span across midnight.
    """
    start_time, end_time = time_range.split("-")
    start_dt = datetime.strptime(start_time, "%H:%M").time()
    end_dt = datetime.strptime(end_time, "%H:%M").time()

    if end_dt < start_dt:
        print("Use case ")
        # Time range spans midnight: split into two parts
        history = update_history_for_range(history, f"{start_time}-23:30", new_value)
        history = update_history_for_range(history, f"23:30-00:00", new_value)  # Handle last 30 min before midnight
        history = update_history_for_range(history, f"00:00-{end_time}", new_value)
    else:
        history = update_history_for_range(history, time_range, new_value)

    return history


def update_history_for_range(history, time_range, new_value):
    """
    Helper function to update the history for a given time range.
    Ensures proper handling of time slots.
    """
    start_time, end_time = time_range.split("-")
    start_dt = datetime.strptime(start_time, "%H:%M").time()
    end_dt = datetime.strptime(end_time, "%H:%M").time()

    for key in list(history.keys()):
        key_start, key_end = key.split("-")
        key_start_dt = datetime.strptime(key_start, "%H:%M").time()
        key_end_dt = datetime.strptime(key_end, "%H:%M").time()

        # If the key represents the special 23:30-00:00 slot, handle it explicitly
        if key == "23:30-00:00":
            #print(" The Key",{key})
            #print("the start time",{start_time},"The end time ",{end_time})
            if (end_time == "23:59"):
                end_time = "00:00"
            if start_time == "23:30" and end_time == "00:00":
                #print(" success Key",{key})
                history[key] = new_value  # Directly set value for this special case
        else:
            #print("start_dt->",{start_dt},"key_start_dt->",{key_start_dt},"end_dt->",{end_dt},"key_end_dt->",{key_end_dt},"start_dt->",{start_dt})
            # Ensure the entire slot is within the time range
            if start_dt <= key_start_dt < end_dt and start_dt < key_end_dt <= end_dt:
                history[key] = new_value  # Update matching slots

    return history


# Function to generate default tariff history
def default_tariff_history():
    time_ranges = {}
    for h in range(24):
        for m in [0, 30]:
            start_time = f"{h:02}:{m:02}"
            end_hour = h if m == 0 else h + 1  # If 30, move to the next hour
            end_minute = 30 if m == 0 else 0   # If 30, reset to 0
            
            # Fix the "24:00" issue
            if end_hour == 24:
                end_hour = 0  # Convert to "00" for midnight
            
            end_time = f"{end_hour:02}:{end_minute:02}"
            time_ranges[f"{start_time}-{end_time}"] = 0.09
    return time_ranges


# Function to generate default capacity history
def default_capacity_history():
    time_ranges = {}
    for h in range(24):
        for m in [0, 30]:
            start_time = f"{h:02}:{m:02}"
            end_hour = h if m == 0 else h + 1
            end_minute = 30 if m == 0 else 0

            # Fix the "24:00" issue
            if end_hour == 24:
                end_hour = 0  # Convert to "00" for midnight
            
            end_time = f"{end_hour:02}:{end_minute:02}"
            time_ranges[f"{start_time}-{end_time}"] = 11
    return time_ranges


def update_connectors():
    # Ensure existing connectors are updated correctly
    for connector in Connector.objects.all():
        if not connector.tariff_history or "23:30-24:00" in connector.tariff_history:
            connector.tariff_history = default_tariff_history()
            connector.save(update_fields=["tariff_history"])

        if not connector.capacity_history or "23:30-24:00" in connector.capacity_history:
            connector.capacity_history = default_capacity_history()
            connector.save(update_fields=["capacity_history"])

    print("Updated all existing connectors with corrected tariff and capacity history.")
