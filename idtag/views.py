from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import IdTagForm
from django.contrib.auth.decorators import login_required
from idtag.models import IdTag
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import IdTag
from .serializers import IdTagSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class IdtagFilter(FilterSet):
    username = CharFilter(field_name='user__username')
    friendly_name = CharFilter(field_name='friendly_name')

    class Meta:
        model = IdTag
        fields = []


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class IdtagApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = IdTagSerializer
    queryset = IdTag.objects.all()
    filterset_class = IdtagFilter

    
    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )
    


class IdtagDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = IdTagSerializer
    lookup_url_kwarg = 'id_token'
    queryset = IdTag.objects.all()
