from django.db import models
from chargepoint.models import Chargepoint
from ocpp.v16 import enums as enums_v16
from uuid import uuid4
from ocpi.models import Tariff


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

# Create your models here.
class Connector(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    connectorid = models.IntegerField()
    availability_status = models.CharField(choices=[(i.value, i.value) for i in enums_v16.AvailabilityType], default=enums_v16.AvailabilityType.operative.value, max_length=11)
    connector_status = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargePointStatus], default=enums_v16.ChargePointStatus.available.value, max_length=13)
    chargepoint = models.ForeignKey(Chargepoint, on_delete=models.CASCADE)

    standard = models.CharField(max_length=255, choices=ConnectorType.choices)
    format = models.CharField(max_length=10, choices=ConnectorFormat.choices)
    power_type = models.CharField(max_length=20, choices=PowerType.choices)

    # max_voltage, max_amperage, max_electric_power are ommited

    tariff_ids = models.ManyToManyField(Tariff)
    
    def __str__(self):
        return "Connector " + str(self.connectorid) + " of " + self.chargepoint.chargepoint_id