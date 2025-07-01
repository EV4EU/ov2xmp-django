from rest_framework import serializers
from statusnotification.models import Statusnotification, Statusnotification201


class StatusnotificationSerializer(serializers.ModelSerializer):
    connector = serializers.SlugRelatedField(many=False, read_only=True, slug_field="uuid")
    class Meta:
        model = Statusnotification
        fields = "__all__"


class Statusnotification201Serializer(serializers.ModelSerializer):
    connector = serializers.SlugRelatedField(many=False, read_only=True, slug_field="uuid")
    class Meta:
        model = Statusnotification201
        fields = "__all__"
