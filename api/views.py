from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication  

