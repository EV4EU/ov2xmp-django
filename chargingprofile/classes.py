from pydantic.main import BaseModel as PydanticBaseModel
from pydantic import Json
from pydantic import PositiveInt
from rest_framework.fields import JSONField
from typing import Optional
from datetime import datetime
from ocpp.v201 import enums as ocpp201_enums


class ChargingSchedulePeriod16SerializerField(JSONField):
    pass


class ChargingSchedulePeriod16(PydanticBaseModel):
    startPeriod: PositiveInt
    limit: float
    number_phases: PositiveInt
