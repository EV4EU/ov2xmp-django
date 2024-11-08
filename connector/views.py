from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from .models import Connector
from .serializers import ConnectorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django_filters.rest_framework import FilterSet, CharFilter


class ConnectorFilter(FilterSet):
    chargepoint_id = CharFilter(field_name='chargepoint__chargepoint_id')
    availability_status = CharFilter(field_name='availability_status')
    connector_status = CharFilter(field_name='connector_status')
    connector_id = CharFilter(field_name='connectorid')

    class Meta:
        model = Connector
        fields = []


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class ConnectorApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ConnectorSerializer
    queryset = Connector.objects.all()
    filterset_class = ConnectorFilter
    
    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class ConnectorDetailApiView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ConnectorSerializer
    lookup_url_kwarg = 'uuid'
    queryset = Connector.objects.all()

    def get(self, request, uuid):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        filtered_queryset = filtered_queryset.filter(uuid=uuid)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )
