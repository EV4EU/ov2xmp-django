from django.core.mail import send_mail
from django.conf import settings
from rest_framework.generics import CreateAPIView 
from rest_framework.response import Response
from rest_framework import status
from mailsending.serializers import EmailSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  


class SendEmailView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.data['subject']
            message = serializer.data['message']
            recipient_email = serializer.data['recipient_email']
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [recipient_email],
                    fail_silently=False,       # Set to True if you want to silently handle errors
                )
                return Response({"status": "Email sent successfully!"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
