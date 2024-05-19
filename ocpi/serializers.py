from rest_framework import serializers
from .models import TariffElement, Tariff, Cdr, ChargingPeriod
from rest_framework.fields import ListField
from ocpi.classes import PriceComponentSerializerField, PriceSerializerField, TariffRestrictionsSerializerField, DisplayTextSerializerField, ManyToManyFieldWriteOnlySerializerField
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST


class TariffElementSerializer(serializers.ModelSerializer):
    price_components = ListField(child=PriceComponentSerializerField())
    restrictions = TariffRestrictionsSerializerField(required=False)
    class Meta:
        model = TariffElement
        fields = "__all__"


class TariffSerializerReadOnly(serializers.ModelSerializer):
    tariff_alt_text = ListField(child=DisplayTextSerializerField())
    min_price = PriceSerializerField(required=False)
    max_price = PriceSerializerField(required=False)

    elements = TariffElementSerializer(read_only=True, many=True)

    class Meta:
        model = Tariff
        fields = "__all__"
        

class TariffSerializerWriteOnly(TariffSerializerReadOnly):

    elements = ListField(write_only=True, child=ManyToManyFieldWriteOnlySerializerField())
        
    def create(self, validated_data):
        tariffElement_ids = validated_data.pop('elements') # type: ignore
        tariffElement_instances = []
        try:
            for tariffElement in tariffElement_ids: # type: ignore
                tariffElement_instances.append(TariffElement.objects.get(pk=tariffElement['id']))
        except TariffElement.DoesNotExist:
            raise ValidationError(detail='Specified TariffElement ID does not exist.', code=HTTP_400_BAD_REQUEST)

        new_tariff = Tariff.objects.create(**validated_data)
        new_tariff.save()
        new_tariff.elements.set(tariffElement_instances)
        new_tariff.save()
        return new_tariff


class ChargingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingPeriod
        fields = ['start_date_time', 'dimensions', 'tariff_id']


class CdrSerializer(serializers.ModelSerializer):
    
    session_id = serializers.SlugRelatedField(slug_field='uuid', read_only=True)
    tariffs = TariffSerializerReadOnly(read_only=True, many=True)
    charging_periods = ChargingPeriodSerializer(read_only=True, many=True)
    total_cost = PriceSerializerField(required=False)
    total_fixed_cost = PriceSerializerField(required=False)
    total_energy_cost = PriceSerializerField(required=False)
    total_time_cost = PriceSerializerField(required=False)
    total_parking_cost = PriceSerializerField(required=False)
    total_reservation_cost = PriceSerializerField(required=False)
    
    class Meta:
        model = Cdr
        fields = "__all__"
