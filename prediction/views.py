from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from prediction.serializers import *
from prediction.tasks import *
from rest_framework_simplejwt.authentication import JWTAuthentication  
from enum import Enum


class MESSAGE_CODE(Enum):
    RESPONSE_RECEIVED = 200
    TASK_SUBMITTED = "Task has been submitted successfully"


class PredictionApiView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = PredictionSerializer

    def post(self, request, *args, **kwargs):
        '''
        Receive a request to generate AI predictions
        '''

        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["sync"]:
                task = generate_prediction(serializer.data) # type: ignore
                return Response(task, status=status.HTTP_200_OK)
            else:
                task = generate_prediction(serializer.data) # type: ignore
                return Response({"message_code": MESSAGE_CODE.TASK_SUBMITTED.name, "message": MESSAGE_CODE.TASK_SUBMITTED.value, "task_id": task.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
