from rest_framework import serializers
from .models import Location
from django_countries.serializers import CountryFieldMixin
from zoneinfo import available_timezones
from .classes import GeoLocationSerializerField

class LocationSerializer(CountryFieldMixin, serializers.ModelSerializer):
    time_zone = serializers.ChoiceField(choices=available_timezones())
    coordinates = GeoLocationSerializerField()
    
    class Meta:
        model = Location
        fields = "__all__"
