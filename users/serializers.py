from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User
from zoneinfo import available_timezones
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_field


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError("Email has already been used.")
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email", "is_superuser", "is_active"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    timezone = serializers.ChoiceField(choices=available_timezones())

    class Meta:
        model = Profile
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token
