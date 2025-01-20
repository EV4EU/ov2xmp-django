from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny

# Define a serializer to validate email parameters
class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=100)
    message = serializers.CharField(max_length=500)
    recipient_email = serializers.EmailField()

# Create the API View to handle sending the email
@extend_schema(
    request=EmailSerializer,  # Define the request schema here
    responses={200: OpenApiTypes.STR},  # Define a response type
)
class SendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Validate incoming data with serializer
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            recipient_email = serializer.validated_data['recipient_email']
            
            try:
                # Send the email using Django's send_mail function
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # From address (your Gmail)
                    [recipient_email],         # To address
                    fail_silently=False,       # Set to True if you want to silently handle errors
                )
                return Response({"status": "Email sent successfully!"}, status=status.HTTP_200_OK)
            except Exception as e:
                # Detailed error message to handle failures in sending email
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # If serializer is invalid, return the validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
