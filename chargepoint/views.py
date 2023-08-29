from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Chargepoint
from .serializers import ChargepointSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  


class ChargepointApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChargepointSerializer
    queryset = Chargepoint.objects.all()


class ChargepointDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChargepointSerializer
    lookup_url_kwarg = 'chargepoint_id'
    queryset = Chargepoint.objects.all()

