from pydantic.main import BaseModel as PydanticBaseModel
from rest_framework.fields import JSONField


class GeoLocation(PydanticBaseModel):
    latitude: float
    longitude: float


class GeoLocationSerializerField(JSONField):
    pass