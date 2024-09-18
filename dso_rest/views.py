from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from dso_rest.serializers import *
from dso_rest.tasks import *
from rest_framework_simplejwt.authentication import JWTAuthentication  
from enum import Enum


class MESSAGE_CODE(Enum):
    RESPONSE_RECEIVED = 200
    TASK_SUBMITTED = "Task has been submitted successfully"


class DSOSignalApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = DSOSignalSerializer

    def post(self, request, *args, **kwargs):
        '''
        Send a signal to the CPO
        '''

        serializer = DSOSignalSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = process_dso_signal(serializer.data) # type: ignore
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = process_dso_signal(serializer.data) # type: ignore
                return Response({"message_code": MESSAGE_CODE.TASK_SUBMITTED.name, "message": MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
