from django.db import models
from connector.models import Connector
from chargepoint.models import Chargepoint
from ocpp.v16 import enums as enums_v16 #ChargePointErrorCode
from ocpp.v201 import enums as enums_v201
from uuid import uuid4
from django.utils.timezone import now


# Create your models here.
class Statusnotification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE, null=True, default=None)
    chargepoint = models.ForeignKey(Chargepoint, on_delete=models.CASCADE)
    error_code = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargePointErrorCode], max_length=50)
    info = models.CharField(max_length=50, blank=True, null=True, default='')
    status_reported = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargePointStatus], max_length=50)
    timestamp = models.DateTimeField(default=now)
    vendor_id = models.CharField(max_length=255, blank=True, null=True, default='')
    vendor_error_code = models.CharField(max_length=50, blank=True, null=True, default='')


class Statusnotification201(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE, null=True, default=None)
    timestamp = models.DateTimeField()
    connector_status = models.CharField(choices=[(i.value, i.value) for i in enums_v201.ConnectorStatusEnumType], max_length=50)