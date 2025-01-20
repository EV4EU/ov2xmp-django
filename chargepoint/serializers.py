from rest_framework import serializers
from .models import Chargepoint
from location.serializers import LocationSerializer
from location.models import Location
from rest_framework.response import Response
from rest_framework import status
from api.serializers import RelatedFieldAlternative


class ChargepointSerializer(serializers.ModelSerializer):

    location = RelatedFieldAlternative(queryset=Location.objects.all(), serializer=LocationSerializer)
    #location = LocationSerializer(allow_null=True, read_only=True)

    chargepoint_id = serializers.PrimaryKeyRelatedField(read_only=True)
    ip_address = serializers.CharField(read_only=True)
    websocket_port = serializers.IntegerField(read_only=True)
    connected = serializers.BooleanField(read_only=True)
    ocpp_version = serializers.CharField(read_only=True)
    last_heartbeat = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chargepoint
        fields = "__all__"
