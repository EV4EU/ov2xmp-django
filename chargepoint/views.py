from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Chargepoint
from .serializers import ChargepointSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from django_filters.rest_framework import FilterSet, CharFilter
from django_filters.rest_framework import FilterSet, CharFilter
from ov2xmp.helpers import CustomListCreateApiView


class ChargepointFilter(FilterSet):
    chargepoint_status = CharFilter(field_name='chargepoint_status')

    class Meta:
        model = Chargepoint
        fields = []


class ChargepointApiView(CustomListCreateApiView):
    serializer_class = ChargepointSerializer
    queryset = Chargepoint.objects.all()
    filterset_class = ChargepointFilter


class ChargepointDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChargepointSerializer
    lookup_url_kwarg = 'chargepoint_id'
    queryset = Chargepoint.objects.all()

