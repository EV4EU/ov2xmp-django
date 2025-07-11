from django.db import models
from idtag.models import IdTag
from uuid import uuid4
from connector.models import Connector
from django.contrib.postgres.fields import ArrayField


class TransactionStatus(models.TextChoices):
    started = "Started"
    finished = "Finished"
    unauthorized = "Unauthorized"

    
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=None, null=True, unique=True)
    connector = models.ForeignKey(Connector, on_delete=models.SET_NULL, default=None, null=True)
    start_transaction_timestamp = models.DateTimeField()
    stop_transaction_timestamp = models.DateTimeField(null=True)
    wh_meter_start = models.FloatField()
    wh_meter_stop = models.FloatField(null=True)
    wh_meter_last = models.FloatField()
    wh_meter_last_timestamp = models.DateTimeField()
    id_tag = models.ForeignKey(IdTag, on_delete=models.SET_NULL, null=True, default=None)
    reason_stopped = models.CharField(max_length=50, null=True)
    transaction_status = models.CharField(max_length=15, choices=TransactionStatus.choices, default=TransactionStatus.started)
    chargingprofile_applied = models.JSONField(null=True, default=None, blank=True)
    tariffs = ArrayField(base_field=models.JSONField(), null=True, default=None, blank=True)