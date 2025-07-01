from pydantic.main import BaseModel as PydanticBaseModel
from rest_framework.fields import JSONField
from datetime import datetime
from typing import Union


class Period(PydanticBaseModel):
    timeslot_start: int
    timeslot_end: int
    value: Union[float, list]


class PeriodSerializerField(JSONField):
    pass
