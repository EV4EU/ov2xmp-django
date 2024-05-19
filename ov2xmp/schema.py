from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import follow_field_source, build_basic_type
from drf_spectacular.types import OpenApiTypes
from pydantic.main import BaseModel
from ocpi.classes import PriceComponent, TariffRestrictions, Price, DisplayText, ManyToManyWriteOnlyField
from chargingprofile.classes import ChargingSchedulePeriod
from rest_framework.fields import JSONField
from location.classes import GeoLocation


class PriceComponentFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "ocpi.classes.PriceComponentSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return PriceComponent.schema(ref_template='#/components/schemas/PatchedTariffElement/properties/price_components/items/definitions/{model}')
    

class TariffRestrictionsFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "ocpi.classes.TariffRestrictionsSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return TariffRestrictions.schema(ref_template='#/components/schemas/PatchedTariffElement/properties/restrictions/definitions/{model}')


class PriceFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "ocpi.classes.PriceSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return Price.schema()
    

class DisplayTextFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "ocpi.classes.DisplayTextSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return DisplayText.schema()


class ManyToManyFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "ocpi.classes.ManyToManyFieldWriteOnlySerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return ManyToManyWriteOnlyField.schema()


class ChargingSchedulePeriodFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "chargingprofile.classes.ChargingSchedulePeriodSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return ChargingSchedulePeriod.schema()
    

class GeoLocationFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "location.classes.GeoLocationSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return GeoLocation.schema()
