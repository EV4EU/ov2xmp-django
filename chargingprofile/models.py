from django.db import models
from ocpp.v16 import enums as enums_v16
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4
from ov2xmp.validators import JSONSchemaValidator
from chargingprofile.classes import ChargingSchedulePeriod
from transaction.models import Transaction


class Chargingprofile(models.Model):
    #uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chargingprofile_id = models.AutoField(primary_key=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    stack_level = models.IntegerField()
    chargingprofile_purpose = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargingProfilePurposeType], default=enums_v16.ChargingProfilePurposeType.charge_point_max_profile.value, max_length=21)
    chargingprofile_kind = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargingProfileKindType], default=enums_v16.ChargingProfileKindType.absolute.value, max_length=10)
    recurrency_kind = models.CharField(choices=[(i.value, i.value) for i in enums_v16.RecurrencyKind], default=None, null=True, max_length=10)
    valid_from = models.DateTimeField(default=None, null=True, blank=True)
    valid_to = models.DateTimeField(default=None, null=True, blank=True)
    ## ChargingSchedule attributes
    duration = models.IntegerField(default=None, null=True, blank=True)
    start_schedule = models.DateTimeField(default=None, null=True, blank=True)
    charging_rate_unit = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargingRateUnitType], default=enums_v16.ChargingRateUnitType.watts.value, max_length=1)
    chargingschedule_period = ArrayField(models.JSONField(validators=[JSONSchemaValidator(limit_value=ChargingSchedulePeriod.schema())]))
    min_charging_rate = models.DecimalField(default=None, null=True, max_digits=5, decimal_places=1, blank=True)
