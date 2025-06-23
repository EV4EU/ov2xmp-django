from rest_framework.generics import ListAPIView
from .models import Sampledvalue
from .serializers import SampledvalueSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django_filters.rest_framework import FilterSet, CharFilter


class SampledvalueFilter(FilterSet):
    unit = CharFilter(field_name='unit')

    class Meta:
        model = Sampledvalue
        fields = []


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class SampledvalueDetailApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SampledvalueSerializer
    queryset = Sampledvalue.objects.all()
    lookup_url_kwarg = 'transaction_id'
    filterset_class = SampledvalueFilter

    def get(self, request, transaction_id):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        filtered_queryset = filtered_queryset.filter(transaction_id=transaction_id)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )
