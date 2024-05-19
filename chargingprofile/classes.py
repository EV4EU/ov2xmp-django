from pydantic.main import BaseModel as PydanticBaseModel
from rest_framework.fields import JSONField


class ChargingSchedulePeriod(PydanticBaseModel):
    startPeriod: int
    limit: float
    number_phases: int


class ChargingSchedulePeriodSerializerField(JSONField):
    pass