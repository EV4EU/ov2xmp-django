from django.shortcuts import render
from ocpi.serializers import TariffSerializerReadOnly, TariffSerializerWriteOnly, TariffElementSerializer, CdrSerializer
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, UpdateAPIView, RetrieveDestroyAPIView
from ocpi.models import TariffElement, Tariff, Cdr


class TariffElementApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TariffElementSerializer
    queryset = TariffElement.objects.all()


class TariffElementDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TariffElementSerializer
    lookup_url_kwarg = 'id'
    queryset = TariffElement.objects.all()


class TariffApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    model = Tariff
    queryset = Tariff.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TariffSerializerWriteOnly
        return TariffSerializerReadOnly


class TariffDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TariffSerializerWriteOnly
    lookup_url_kwarg = 'id'
    queryset = Tariff.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TariffSerializerReadOnly
        return TariffSerializerWriteOnly


class CdrApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CdrSerializer
    queryset = Cdr.objects.all()


class CdrDetailApiView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CdrSerializer
    lookup_url_kwarg = 'id'
    queryset = Cdr.objects.all()
