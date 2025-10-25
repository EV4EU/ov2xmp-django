from idtag.models import IdTag
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import IdTag
from .serializers import IdTagSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from django_filters.rest_framework import FilterSet, CharFilter
from ov2xmp.helpers import CustomListCreateApiView

class IdtagFilter(FilterSet):
    username = CharFilter(field_name='user__username')
    friendly_name = CharFilter(field_name='friendly_name')

    class Meta:
        model = IdTag
        fields = []


class IdtagApiView(CustomListCreateApiView):
    serializer_class = IdTagSerializer
    queryset = IdTag.objects.all()
    filterset_class = IdtagFilter


class IdtagDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = IdTagSerializer
    lookup_url_kwarg = 'id_token'
    queryset = IdTag.objects.all()
