# mailsending/serializers.py
from rest_framework import serializers

class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=255, required=True)
    message = serializers.CharField(required=True)
