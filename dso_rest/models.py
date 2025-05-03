from django.db import models
from django.contrib.postgres.fields import ArrayField
from dso_rest.classes import Period
from ov2xmp.validators import JSONSchemaValidator


class uuName(models.TextChoices):
    event_DUoSTarrif = "event_DUoSTarrif"
    event_CapacityLimit = "event_CapacityLimit"


# Create your models here.
class DsoSignal(models.Model):
    id = models.IntegerField(primary_key=True)
    uuId = models.UUIDField()
    uuName = models.CharField(choices=uuName)
    event_timestamp = models.IntegerField()
    locationCoords = ArrayField(base_field=models.CharField(max_length=10))
    locationName = models.CharField(max_length=30)
    transformerID = models.CharField(max_length=255)
    duration = models.IntegerField()
    period = ArrayField(base_field=models.JSONField(validators=[JSONSchemaValidator(limit_value=Period.schema())]))

