from django.db import models
from django_countries.fields import CountryField
from uuid import uuid4
from timezone_field import TimeZoneField
from ov2xmp.validators import JSONSchemaValidator
from .classes import GeoLocation
import os


OV2XMP_OCPI_COUNTRYCODE = os.environ.get("OV2XMP_OCPI_COUNTRYCODE", "GR")
OV2XMP_OCPI_PARTYID = os.environ.get("OV2XMP_OCPI_PARTYID", "DEF")
OV2XMP_OCPI_CURRENCY = os.environ.get("OV2XMP_OCPI_CURRENCY", "EUR")


class ParkingType(models.TextChoices):
    ALONG_MOTORWAY = "ALONG_MOTORWAY"
    PARKING_GARAGE = "PARKING_GARAGE"
    PARKING_LOT = "PARKING_LOT"
    ON_DRIVEWAY = "ON_DRIVEWAY"
    ON_STREET = "ON_STREET"
    UNDERGROUND_GARAGE = "UNDERGROUND_GARAGE"


# Create your models here.
class Location(models.Model):
    country_code = models.CharField(max_length=2, default=OV2XMP_OCPI_COUNTRYCODE)
    party_id = models.CharField(max_length=3, default=OV2XMP_OCPI_PARTYID)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField()
    coordinates = models.JSONField(validators=[JSONSchemaValidator(limit_value=GeoLocation.schema())])
    parking_type = models.CharField(choices=ParkingType.choices, max_length=20)
    last_updated = models.DateTimeField(auto_now=True)
    time_zone = TimeZoneField(default='Europe/Athens')
    substation_id = models.CharField(max_length=100, null=True, blank=True)
