from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django_celery_results.models import TaskResult
from .serializers import TaskResultSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  


class TasksApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskResultSerializer
    queryset = TaskResult.objects.all()


class TasksDetailApiView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskResultSerializer
    queryset = TaskResult.objects.all()
    lookup_url_kwarg = 'task_id'
