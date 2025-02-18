from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):
    chargepoint_name = serializers.CharField()
    sync = serializers.BooleanField(default=True, required=False)
