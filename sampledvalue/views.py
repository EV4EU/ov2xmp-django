from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.generics import ListAPIView
from .serializers import SampledvalueSerializer
from .models import Sampledvalue


class SampledvalueDetailApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SampledvalueSerializer
    lookup_url_kwarg = 'transaction_id'

    def get_queryset(self):
        try:
            transaction_id = self.kwargs["transaction_id"]   
            return Sampledvalue.objects.filter(transaction__transaction_id=transaction_id)
        except:
            return Sampledvalue.objects.none()