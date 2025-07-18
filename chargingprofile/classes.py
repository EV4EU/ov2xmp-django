from pydantic.main import BaseModel as PydanticBaseModel
from pydantic import PositiveInt
from rest_framework.fields import JSONField


class ChargingSchedulePeriod16SerializerField(JSONField):
    pass


class ChargingSchedulePeriod16(PydanticBaseModel):
    startPeriod: PositiveInt
    limit: float
    number_phases: PositiveInt
