from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  


class ReservationApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class ReservationDetailApiView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ReservationSerializer
    lookup_url_kwarg = 'chargepoint_id'

    def get_queryset(self):
        try:
            chargepoint_id = self.kwargs["chargepoint_id"]   
            return Reservation.objects.filter(connector__chargepoint__chargepoint_id=chargepoint_id)
        except:
            return Reservation.objects.none()