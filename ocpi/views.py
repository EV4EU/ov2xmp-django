from django.shortcuts import render
from ocpi.serializers import TariffSerializerReadOnly, TariffSerializerWriteOnly, TariffElementSerializer, CdrSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from ocpi.models import TariffElement, Tariff, Cdr
from ov2xmp.helpers import CustomListApiView, CustomListCreateApiView
from django_filters.rest_framework import FilterSet, CharFilter, DateFilter


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class TariffElementApiView(CustomListCreateApiView):
    serializer_class = TariffElementSerializer
    queryset = TariffElement.objects.all()



@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class TariffElementDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TariffElementSerializer
    lookup_url_kwarg = 'id'
    queryset = TariffElement.objects.all()

    def get(self, request, id):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        filtered_queryset = filtered_queryset.filter(id=id)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data[0] )


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class TariffApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    model = Tariff
    queryset = Tariff.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TariffSerializerWriteOnly
        return TariffSerializerReadOnly

    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= TariffSerializerReadOnly(filtered_queryset.all(), many=True).data )


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class TariffDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TariffSerializerWriteOnly
    lookup_url_kwarg = 'id'
    queryset = Tariff.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TariffSerializerReadOnly
        return TariffSerializerWriteOnly

    def get(self, request, id):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        filtered_queryset = filtered_queryset.filter(id=id)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= TariffSerializerReadOnly(filtered_queryset.all(), many=True).data[0] )


class CdrFilter(FilterSet):
    cdr_token = CharFilter(field_name='cdr_token')
    session_id = CharFilter(field_name='session_id__transaction_id')
   
    class Meta:
        model = Cdr
        fields = []


'''
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class CdrApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CdrSerializer
    queryset = Cdr.objects.all()
    
    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )
'''
class CdrApiView(CustomListApiView):
    serializer_class = CdrSerializer
    queryset = Cdr.objects.all()
    filterset_class = CdrFilter

@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class CdrDetailApiView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CdrSerializer
    lookup_url_kwarg = 'id'
    queryset = Cdr.objects.all()

    def get(self, request, id):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        filtered_queryset = filtered_queryset.filter(id=id)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data[0] )
