from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Chargepoint
from .serializers import ChargepointSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django_filters.rest_framework import FilterSet, CharFilter


class ChargepointFilter(FilterSet):
    chargepoint_status = CharFilter(field_name='chargepoint_status')

    class Meta:
        model = Chargepoint
        fields = []


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class ChargepointApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChargepointSerializer
    queryset = Chargepoint.objects.all()
    filterset_class = ChargepointFilter

    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )


class ChargepointDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChargepointSerializer
    lookup_url_kwarg = 'chargepoint_id'
    queryset = Chargepoint.objects.all()

