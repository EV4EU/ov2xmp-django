from django.db import models
import json
import os
from django.contrib.postgres.fields import ArrayField
from ov2xmp.validators import JSONSchemaValidator
from ocpi.classes import PriceComponent, TariffType, TariffRestrictions, Price, AuthMethod, ChargingPeriod
from uuid import uuid4
from idtag.models import IdTag
from location.models import Location


OV2XMP_OCPI_COUNTRYCODE = os.environ.get("OV2XMP_OCPI_COUNTRYCODE", "GR")
OV2XMP_OCPI_PARTYID = os.environ.get("OV2XMP_OCPI_PARTYID", "DEF")
OV2XMP_OCPI_CURRENCY = os.environ.get("OV2XMP_OCPI_CURRENCY", "EUR")


class TariffElement(models.Model):
    price_components = ArrayField(
        base_field=models.JSONField(
            default=dict,
            validators=[JSONSchemaValidator(limit_value=PriceComponent.schema())]
            ))
    
    restrictions = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=TariffRestrictions.schema())]
    )


# Create your models here.
class Tariff(models.Model):
    country_code = models.CharField(max_length=2, default=OV2XMP_OCPI_COUNTRYCODE)
    party_id = models.CharField(max_length=3, default=OV2XMP_OCPI_PARTYID)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    currency = models.CharField(max_length=3, default=OV2XMP_OCPI_CURRENCY)
    type = models.CharField(max_length=15, choices=TariffType.choices, default=TariffType.REGULAR)
    tariff_alt_text = ArrayField(base_field=models.JSONField())
    min_price = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())],
        blank=True, null=True)
    max_price = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())],
        blank=True, null=True)
    start_date_time = models.DateTimeField(null=True, blank=True)
    end_date_time = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    elements = models.ManyToManyField(TariffElement)


class Cdr(models.Model):
    country_code = models.CharField(max_length=2, default=OV2XMP_OCPI_COUNTRYCODE)
    party_id = models.CharField(max_length=3, default=OV2XMP_OCPI_PARTYID)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    session_id = models.ForeignKey(to='transaction.Transaction', on_delete=models.SET_NULL, null=True)
    cdr_token = models.ForeignKey(IdTag, on_delete=models.SET_NULL, null=True)   # The cdr_token must be filled by traversing through session_id__id_tag__idToken
    auth_method = models.CharField(max_length=15, choices=AuthMethod.choices)
    authorization_reference = models.CharField(max_length=36, null=True, blank=True)
    cdr_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True) # The cdr_location must be filled by traversing through session_id__connector__chargepoint__location
    meter_id = models.CharField(max_length=3, null=True, blank=True)
    tariffs = ArrayField(base_field=models.JSONField())
    charging_periods = ArrayField(base_field=models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=ChargingPeriod.schema())]))
    # signed_data is ommitted
    total_cost = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())])
    total_fixed_cost = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())])
    total_energy = models.FloatField()
    total_energy_cost = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())])
    total_time = models.FloatField() # in hours
    total_time_cost = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())])
    total_parking_time = models.FloatField(null=True, blank=True)
    total_parking_cost = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())])
    total_reservation_cost = models.JSONField(
        default=dict,
        validators=[JSONSchemaValidator(limit_value=Price.schema())])
    remark = models.CharField(max_length=255, null=True, blank=True)
    credit = models.BooleanField(default=False)
    credit_reference_id = models.CharField(max_length=39, null=True, blank=True)
    home_charging_compensation = models.BooleanField()
    last_updated = models.DateTimeField(auto_now=True)
