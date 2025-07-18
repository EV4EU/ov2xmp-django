from django.db import models
from ocpp.v16 import enums as enums_v16
from ocpp.v201 import enums as enums_v201
from ocpp.v201 import datatypes as datatypes_v201

from django.contrib.postgres.fields import ArrayField
from uuid import uuid4
from ov2xmp.validators import JSONSchemaValidator
from chargingprofile.classes import ChargingSchedulePeriod16
from transaction.models import Transaction
from dso_rest.models import DsoSignal


class Chargingprofile16(models.Model):
    #uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chargingprofile_id = models.AutoField(primary_key=True)
    stack_level = models.IntegerField()
    chargingprofile_purpose = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargingProfilePurposeType], default=enums_v16.ChargingProfilePurposeType.charge_point_max_profile.value, max_length=21)
    chargingprofile_kind = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargingProfileKindType], default=enums_v16.ChargingProfileKindType.absolute.value, max_length=10)
    ## start ChargingSchedule attributes
    duration = models.IntegerField(default=None, null=True, blank=True)
    start_schedule = models.DateTimeField(default=None, null=True, blank=True)
    charging_rate_unit = models.CharField(choices=[(i.value, i.value) for i in enums_v16.ChargingRateUnitType], default=enums_v16.ChargingRateUnitType.watts.value, max_length=1)
    chargingschedule_period = ArrayField(models.JSONField(validators=[JSONSchemaValidator(limit_value=ChargingSchedulePeriod16.schema())]))
    min_charging_rate = models.DecimalField(default=None, null=True, max_digits=7, decimal_places=1, blank=True)
    #### end ChargingSchedule attributes
    valid_from = models.DateTimeField(default=None, null=True, blank=True)
    valid_to = models.DateTimeField(default=None, null=True, blank=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    recurrency_kind = models.CharField(choices=[(i.value, i.value) for i in enums_v16.RecurrencyKind], default=None, null=True, max_length=10)
    dsosignal = models.ForeignKey(DsoSignal, on_delete=models.SET_NULL, default=None, null=True, blank=True)


class Chargingprofile201(models.Model):
    chargingprofile_id = models.AutoField(primary_key=True)
    stack_level = models.IntegerField()
    chargingprofile_purpose = models.CharField(choices=[(i.value, i.value) for i in enums_v201.ChargingProfilePurposeEnumType], default=enums_v201.ChargingProfilePurposeEnumType.charging_station_max_profile.value, max_length=50)
    chargingprofile_kind = models.CharField(choices=[(i.value, i.value) for i in enums_v201.ChargingProfileKindEnumType], default=enums_v201.ChargingProfileKindEnumType.absolute.value, max_length=10)
    recurrency_kind = models.CharField(choices=[(i.value, i.value) for i in enums_v201.RecurrencyKindEnumType], default=None, null=True, max_length=10)
    valid_from = models.DateTimeField(default=None, null=True, blank=True)
    valid_to = models.DateTimeField(default=None, null=True, blank=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    charging_schedule = ArrayField(base_field=models.JSONField(), max_length=3)


