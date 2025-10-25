from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Chargingprofile16, Chargingprofile201
from .serializers import Chargingprofile16Serializer, Chargingprofile201Serializer
from ov2xmp.helpers import CustomListCreateApiView

class Chargingprofile16ApiView(CustomListCreateApiView):
    serializer_class = Chargingprofile16Serializer
    queryset = Chargingprofile16.objects.all()


class Chargingprofile16DetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Chargingprofile16Serializer
    lookup_url_kwarg = 'chargingprofile_id'
    queryset = Chargingprofile16.objects.all()


###########################################################################################################################
###########################################################################################################################
class Chargingprofile201ApiView(CustomListCreateApiView):
    serializer_class = Chargingprofile201Serializer
    queryset = Chargingprofile201.objects.all()


class Chargingprofile201DetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Chargingprofile201Serializer
    lookup_url_kwarg = 'chargingprofile_id'
    queryset = Chargingprofile201.objects.all()
