from django.db import models
from chargepoint.models import Chargepoint
from uuid import uuid4
from ocpi.models import Tariff
from django.contrib.postgres.fields import ArrayField  # Import ArrayField


# This Function generates default time slots with values. For Tariff
def default_tariff_history():
    time_ranges = {}
    for h in range(24):
        for m in [0, 30]:
            start_time = f"{h:02}:{m:02}"
            end_hour = h if m == 0 else h + 1  # If 30, move to the next hour
            end_minute = 30 if m == 0 else 0   # If 30, reset to 0
            
            # Fix the "24:00" issue
            if end_hour == 24:
                end_hour = 0  # Convert to "00"
            
            end_time = f"{end_hour:02}:{end_minute:02}"
            time_ranges[f"{start_time}-{end_time}"] = 0.09
    return time_ranges

# This Function generates default time slots with values. For Capacity
def default_capacity_history():
    time_ranges = {}
    for h in range(24):
        for m in [0, 30]:
            start_time = f"{h:02}:{m:02}"
            end_hour = h if m == 0 else h + 1
            end_minute = 30 if m == 0 else 0

            # Fix the "24:00" issue
            if end_hour == 24:
                end_hour = 0  # Convert to "00"
            
            end_time = f"{end_hour:02}:{end_minute:02}"
            time_ranges[f"{start_time}-{end_time}"] = 11
    return time_ranges

# this needs to be extended, according to OCPI
class ConnectorType(models.TextChoices):
    CHADEMO = "CHADEMO"
    DOMESTIC_A = "DOMESTIC_A"
    IEC_60309_2_single_16 = "IEC_60309_2_single_16"
    IEC_62196_T1_COMBO = "IEC_62196_T1_COMBO"


class ConnectorFormat(models.TextChoices):
    SOCKET = "SOCKET"
    CABLE = "CABLE"


class PowerType(models.TextChoices):
    AC_1_PHASE = "AC_1_PHASE"
    AC_3_PHASE = "AC_3_PHASE"
    DC = "DC"


class Connector(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    connectorid = models.IntegerField()
    availability_status = models.CharField(default=None, null=True, blank=True, max_length=13)
    connector_status = models.CharField(default=None, null=True, blank=True, max_length=13)
    chargepoint = models.ForeignKey(Chargepoint, on_delete=models.CASCADE)

    standard = models.CharField(max_length=255, choices=ConnectorType.choices, null=True, default=None, blank=True)
    format = models.CharField(max_length=10, choices=ConnectorFormat.choices, null=True, default=None, blank=True)
    power_type = models.CharField(max_length=20, choices=PowerType.choices, null=True, default=None, blank=True)

    # max_voltage, max_amperage, max_electric_power are ommited

    tariff_ids = models.ManyToManyField(Tariff, default=None)
    
    # TODO: This should be ManyToMany field
    charging_profile = ArrayField(
        base_field=models.IntegerField(),  
        null=True, 
        blank=True,  
        default=list,  
    )

    tariff_history = models.JSONField(default=default_tariff_history, blank=True)
    capacity_history = models.JSONField(default=default_capacity_history, blank=True)
    evse_id = models.IntegerField(default=0)
    
    def __str__(self):
        return "Connector " + str(self.connectorid) + " of " + self.chargepoint.chargepoint_id