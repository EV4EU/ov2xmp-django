from rest_framework import serializers
from dso_rest.classes import PeriodSerializerField
from dso_rest.models import DsoSignal


class DsoSignalSerializer(serializers.ModelSerializer):
    sync = serializers.BooleanField(required=False, default=True)

    period = serializers.ListField(
        child=PeriodSerializerField()
    )
    
    def create(self, validated_data):
        if "sync" in validated_data:
            del validated_data["sync"]
        return DsoSignal.objects.create(**validated_data)
    
    class Meta:
        model = DsoSignal
        fields = "__all__"
