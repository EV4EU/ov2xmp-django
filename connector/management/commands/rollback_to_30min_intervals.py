# Save this as: rollback_connectors.py (in your project root)
# Or run directly in Django shell

from connector.models import Connector

def old_default_tariff_history():
    """Generate default tariff history with 30-minute slots for 24 hours (48 slots)"""
    time_ranges = {}
    for h in range(24):
        for m in [0, 30]:
            start_time = f"{h:02d}:{m:02d}"
            end_hour = h if m == 0 else h + 1
            end_minute = 30 if m == 0 else 0
            if end_hour == 24:
                end_hour = 0
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            time_ranges[f"{start_time}-{end_time}"] = 0.09
    return time_ranges

def old_default_capacity_history():
    """Generate default capacity history with 30-minute slots for 24 hours (48 slots)"""
    time_ranges = {}
    for h in range(24):
        for m in [0, 30]:
            start_time = f"{h:02d}:{m:02d}"
            end_hour = h if m == 0 else h + 1
            end_minute = 30 if m == 0 else 0
            if end_hour == 24:
                end_hour = 0
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            time_ranges[f"{start_time}-{end_time}"] = 11
    return time_ranges

# Apply rollback to all connectors
print("Starting rollback to 30-minute intervals...")
updated_count = 0

for connector in Connector.objects.all():
    old_tariff_slots = len(connector.tariff_history) if connector.tariff_history else 0
    old_capacity_slots = len(connector.capacity_history) if connector.capacity_history else 0
    
    connector.tariff_history = old_default_tariff_history()
    connector.capacity_history = old_default_capacity_history()
    connector.save(update_fields=["tariff_history", "capacity_history"])
    
    updated_count += 1
    print(f"✓ Connector {connector.uuid}: {old_tariff_slots}→48 tariff, {old_capacity_slots}→48 capacity")

print(f"Rollback complete: {updated_count} connectors updated to 30-minute intervals")

# Verification
print("\nVerification:")
for connector in Connector.objects.all()[:3]:  # Check first 3 connectors
    tariff_count = len(connector.tariff_history)
    capacity_count = len(connector.capacity_history)
    print(f"Connector {connector.uuid}: {tariff_count} tariff slots, {capacity_count} capacity slots")
    if tariff_count == 48 and capacity_count == 48:
        print("  ✓ Rollback successful")
    else:
        print("  ✗ Rollback failed")