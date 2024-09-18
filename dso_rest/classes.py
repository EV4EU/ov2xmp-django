from pydantic.main import BaseModel as PydanticBaseModel
from rest_framework.fields import JSONField
from datetime import datetime

class Period(PydanticBaseModel):
    timeslot_start: int
    timeslot_end: int
    value: float


class PeriodSerializerField(JSONField):
    pass
