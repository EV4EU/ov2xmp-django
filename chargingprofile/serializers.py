from rest_framework import serializers
from chargingprofile.classes import ChargingSchedulePeriod16SerializerField
from rest_framework.serializers import ListField
from .models import Chargingprofile16, Chargingprofile201
from ocpp.v201 import enums as ocpp201_enums


class Chargingprofile16Serializer(serializers.ModelSerializer):
    chargingschedule_period = ListField(child=ChargingSchedulePeriod16SerializerField())
    class Meta:
        model = Chargingprofile16
        fields = "__all__"

##################################################################################################

class ChargingSchedulePeriod201SerializerField(serializers.Serializer):
    start_period = serializers.IntegerField()
    limit = serializers.FloatField()
    number_phases = serializers.IntegerField(required=False)
    phase_to_use = serializers.IntegerField(required=False)


class ChargingSchedule201SerializerField(serializers.Serializer):
    id = serializers.IntegerField()
    start_schedule = serializers.CharField(required=False)  #TODO: This should be DateTimeField, but the serializer converts it to Datetime object, which causes error when saving the model, because the charging_schedule is a JSON string in the db.
    duration = serializers.IntegerField()
    charging_rate_unit = serializers.ChoiceField(choices=ocpp201_enums.ChargingRateUnitEnumType) 
    min_charging_rate = serializers.FloatField()
    charging_schedule_period = serializers.ListField(child=ChargingSchedulePeriod201SerializerField())
    

class Chargingprofile201Serializer(serializers.ModelSerializer):
    charging_schedule = ListField(child=ChargingSchedule201SerializerField())
    class Meta:
        model = Chargingprofile201
        fields = "__all__"
