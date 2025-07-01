from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from ocpi.classes import PriceComponent, TariffRestrictions, Price, DisplayText, ManyToManyWriteOnlyField
from chargingprofile.classes import ChargingSchedulePeriod16
from location.classes import GeoLocation
from dso_rest.classes import Period


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


class ChargingSchedulePeriod16FieldExtension(OpenApiSerializerFieldExtension):
    target_class = "chargingprofile.classes.ChargingSchedulePeriod16SerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return ChargingSchedulePeriod16.schema()


class GeoLocationFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "location.classes.GeoLocationSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return GeoLocation.schema()


class DSOPeriodFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "dso_rest.classes.PeriodSerializerField"
    def map_serializer_field(self, auto_schema, direction):
        return Period.schema()
