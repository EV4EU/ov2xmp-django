from .models import Chargingprofile
from .serializers import ChargingprofileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ChargingprofileApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChargingprofileSerializer
    queryset = Chargingprofile.objects.all()


class ChargingprofileDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChargingprofileSerializer
    lookup_url_kwarg = 'chargingprofile_id'
    queryset = Chargingprofile.objects.all()
