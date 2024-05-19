from rest_framework import serializers
from .models import IdTag
from django.contrib.auth.models import User


class IdTagSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, queryset=User.objects.all(), read_only=False, allow_null=True, slug_field="username")
    class Meta:
        model = IdTag
        fields = "__all__"
