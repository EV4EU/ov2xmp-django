from rest_framework import serializers
from .models import Chargingprofile
from chargingprofile.classes import ChargingSchedulePeriodSerializerField
from rest_framework.serializers import ListField


class ChargingprofileSerializer(serializers.ModelSerializer):
    chargingschedule_period = ListField(child=ChargingSchedulePeriodSerializerField())
    class Meta:
        model = Chargingprofile
        fields = "__all__"
