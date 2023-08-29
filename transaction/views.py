from django.shortcuts import render
from rest_framework.generics import RetrieveDestroyAPIView, ListAPIView
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from django_filters.rest_framework import FilterSet, CharFilter


class TransactionFilter(FilterSet):
    chargepoint_id = CharFilter(field_name='connector__chargepoint__chargepoint_id')
    username = CharFilter(field_name='id_tag__user__username')
    id_token = CharFilter(field_name='id_tag__idToken')

    class Meta:
        model = Transaction
        fields = []



class TransactionApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filterset_class = TransactionFilter


class TransactionDetailApiView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_url_kwarg = 'transaction_id'