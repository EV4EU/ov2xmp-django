from rest_framework.generics import ListAPIView
from .models import Connector
from .serializers import ConnectorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  


class ConnectorApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ConnectorSerializer
    queryset = Connector.objects.all()


class ConnectorDetailApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ConnectorSerializer
    lookup_url_kwarg = 'chargepoint_id'

    def get_queryset(self):
        chargepoint_id = self.kwargs["chargepoint_id"]   
        return Connector.objects.filter(chargepoint__chargepoint_id=chargepoint_id)
