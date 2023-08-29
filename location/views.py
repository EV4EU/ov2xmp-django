from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Location
from .serializers import LocationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class LocationApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class LocationDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = LocationSerializer
    lookup_url_kwarg = 'location_uuid'
    queryset = Location.objects.all()
