from rest_framework.generics import ListAPIView
from statusnotification.models import Statusnotification, Statusnotification201
from statusnotification.serializers import StatusnotificationSerializer, Statusnotification201Serializer
from rest_framework_simplejwt.authentication import JWTAuthentication  


class StatusnotificationDetailApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = StatusnotificationSerializer
    lookup_url_kwarg = 'chargepoint_id'

    def get_queryset(self):
        try:
            chargepoint_id = self.kwargs["chargepoint_id"]   
            return Statusnotification.objects.filter(chargepoint__chargepoint_id=chargepoint_id)
        except:
            return Statusnotification.objects.none()
        

class Statusnotification201DetailApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = Statusnotification201Serializer
    lookup_url_kwarg = 'chargepoint_id'

    def get_queryset(self):
        try:
            chargepoint_id = self.kwargs["chargepoint_id"]   
            return Statusnotification201.objects.filter(chargepoint__chargepoint_id=chargepoint_id)
        except:
            return Statusnotification201.objects.none()
