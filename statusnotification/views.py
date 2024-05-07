from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from statusnotification.models import Statusnotification
from statusnotification.serializers import StatusnotificationSerializer
from chargepoint.models import Chargepoint
from rest_framework_simplejwt.authentication import JWTAuthentication  
from .serializers import StatusnotificationSerializer


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