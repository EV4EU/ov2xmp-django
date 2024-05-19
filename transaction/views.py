from django.shortcuts import render
from rest_framework.generics import RetrieveDestroyAPIView, ListAPIView
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class TransactionFilter(FilterSet):
    chargepoint_id = CharFilter(field_name='connector__chargepoint__chargepoint_id')
    username = CharFilter(field_name='id_tag__user__username')
    id_token = CharFilter(field_name='id_tag__idToken')
    transaction_status = CharFilter(field_name='transaction_status')

    class Meta:
        model = Transaction
        fields = []
        

@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class TransactionApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filterset_class = TransactionFilter

    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )


class TransactionDetailApiView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_url_kwarg = 'transaction_id'
