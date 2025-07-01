from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Chargingprofile16, Chargingprofile201
from .serializers import Chargingprofile16Serializer, Chargingprofile201Serializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class Chargingprofile16ApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Chargingprofile16Serializer
    queryset = Chargingprofile16.objects.all()

    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )


class Chargingprofile16DetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Chargingprofile16Serializer
    lookup_url_kwarg = 'chargingprofile_id'
    queryset = Chargingprofile16.objects.all()


###########################################################################################################################
###########################################################################################################################
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ],
    )
)
class Chargingprofile201ApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Chargingprofile201Serializer
    queryset = Chargingprofile201.objects.all()

    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )


class Chargingprofile201DetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Chargingprofile201Serializer
    lookup_url_kwarg = 'chargingprofile_id'
    queryset = Chargingprofile201.objects.all()
