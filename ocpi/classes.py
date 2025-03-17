from django.db import models
from pydantic.main import BaseModel as PydanticBaseModel
from typing import Optional
from rest_framework.fields import JSONField

class TariffType(models.TextChoices):
    AD_HOC_PAYMENT = "AD_HOC_PAYMENT"
    PROFILE_CHEAP = "PROFILE_CHEAP"
    PROFILE_FAST = "PROFILE_FAST"
    PROFILE_GREEN = "PROFILE_GREEN"
    REGULAR = "REGULAR"

class TariffDimensionType(models.TextChoices):
    ENERGY = "ENERGY"
    FLAT = "FLAT"
    PARKING_TIME = "PARKING_TIME"
    TIME = "TIME"

class DayOfWeek(models.TextChoices):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class ReservationRestrictionType(models.TextChoices):
    RESERVATION = "RESERVATION"
    RESERVATION_EXPIRES = "RESERVATION_EXPIRES"

class AuthMethod(models.TextChoices):
    AUTH_REQUEST = "AUTH_REQUEST"
    COMMAND = "COMMAND"
    WHITELIST = "WHITELIST"

class CdrDimensionType(models.TextChoices):
    CURRENT = "CURRENT"
    ENERGY = "ENERGY"
    ENERGY_EXPORT = "ENERGY_EXPORT"
    ENERGY_IMPORT = "ENERGY_IMPORT"
    MAX_CURRENT = "MAX_CURRENT"
    MIN_CURRENT = "MIN_CURRENT"
    MAX_POWER = "MAX_POWER"
    MIN_POWER = "MIN_POWER"
    PARKING_TIME = "PARKING_TIME"
    POWER = "POWER"
    RESERVATION_TIME = "RESERVATION_TIME"
    STATE_OF_CHARGE = "STATE_OF_CHARGE"
    TIME = "TIME"

class PriceComponent(PydanticBaseModel):
    type: TariffDimensionType
    price: float
    vat: Optional[float] = 0.0
    step_size: int    

class Price(PydanticBaseModel):
    excl_vat: float
    incl_vat: float

class DisplayText(PydanticBaseModel):
    language: str
    text: str

class TariffRestrictions(PydanticBaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    min_kwh: Optional[int] = None
    max_kwh: Optional[int] = None
    min_current: Optional[int] = None
    max_current: Optional[int] = None
    min_power: Optional[int] = None
    max_power: Optional[int] = None
    min_duration: Optional[int] = None
    max_duration: Optional[int] = None
    day_of_week: Optional[DayOfWeek] = None
    reservation: Optional[ReservationRestrictionType] = None

class ManyToManyWriteOnlyField(PydanticBaseModel):
    id: int

class CdrDimension(PydanticBaseModel):
    type: CdrDimensionType
    volume: float

class ChargingPeriod(PydanticBaseModel):
    start_date_time: str
    dimensions: CdrDimension
    tariff_id: Optional[str]

class ChargingPeriodSerializerField(JSONField):
    pass

class PriceComponentSerializerField(JSONField):
    pass

class TariffRestrictionsSerializerField(JSONField):
    pass

class PriceSerializerField(JSONField):
    pass

class DisplayTextSerializerField(JSONField):
    pass

class ManyToManyFieldWriteOnlySerializerField(JSONField):
    pass

##################################################################################
##################################################################################

