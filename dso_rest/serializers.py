from rest_framework import serializers
from dso_rest.classes import PeriodSerializerField

class DSOSignalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    uuId = serializers.UUIDField()
    uuName = serializers.ChoiceField(choices=['event_DUoSTarrif', 'event_CapacityLimit'])
    transformerID = serializers.CharField()
    event_timestamp = serializers.IntegerField()
    locationCoords = serializers.ListField()
    locationName = serializers.CharField()
    duration = serializers.IntegerField()
    period = serializers.ListField(
        child=PeriodSerializerField()
    )
    sync = serializers.BooleanField(default=True, required=False)
