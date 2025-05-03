from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from dso_rest.serializers import DsoSignalSerializer
from dso_rest.tasks import *
from rest_framework_simplejwt.authentication import JWTAuthentication  
from enum import Enum
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class MESSAGE_CODE(Enum):
    RESPONSE_RECEIVED = 200
    TASK_SUBMITTED = "Task has been submitted successfully"


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class DsoSignalApiView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = DsoSignalSerializer
    queryset = DsoSignal.objects.all()

    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )


    def post(self, request, *args, **kwargs):
        '''
        Send a signal to the CPO
        '''

        serializer = DsoSignalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data["sync"]:
                task = process_dso_signal(serializer.data) 
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = process_dso_signal.delay(serializer.data) # type: ignore
                return Response({"message_code": MESSAGE_CODE.TASK_SUBMITTED.name, "message": MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DsoSignalDetailApiView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = DsoSignalSerializer
    lookup_url_kwarg = 'id'
    queryset = DsoSignal.objects.all()
