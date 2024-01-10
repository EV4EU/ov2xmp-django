from rest_framework import serializers
from .models import Location
from django_countries.serializers import CountryFieldMixin
from zoneinfo import available_timezones


class LocationSerializer(CountryFieldMixin, serializers.ModelSerializer):
    timezone = serializers.ChoiceField(choices=available_timezones())
    class Meta:
        model = Location
        fields = "__all__"
