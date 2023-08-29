from rest_framework import serializers
from .models import Sampledvalue


class SampledvalueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sampledvalue
        fields = "__all__"
