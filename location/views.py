from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Location
from .serializers import LocationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from ov2xmp.helpers import CustomListCreateApiView


class LocationApiView(CustomListCreateApiView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class LocationDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = LocationSerializer
    lookup_url_kwarg = 'location_uuid'
    queryset = Location.objects.all()
