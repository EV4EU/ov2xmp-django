from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django_filters.rest_framework import FilterSet, CharFilter
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import MyTokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import User, Profile, PasswordReset
from users.serializers import ResetPasswordRequestSerializer, ResetPasswordSerializer
from users.serializers import UserProfileSerializer, UserSerializer, UserSignupSerializer
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_message_to_users(data):
    # Get the channel layer
    channel_layer = get_channel_layer()
    
    # Send the data to the 'users_updates' group
    if channel_layer is not None:
        async_to_sync(channel_layer.group_send)(
            "users_updates",  # The group name your consumers are listening to
            {
                "type": "websocket_send",  # Method in your consumer
                "text": data,  # Send the full data (as JSON)
            }
        )


class ProfileFilter(FilterSet):
    username = CharFilter(field_name='user__username')

    class Meta:
        model = Profile
        fields = []


class UserCreateApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user=serializer.save()

            # Trigger WebSocket message for user creation
            #message = f"User {user.username} has been created."
            #send_message_to_users(message)  # Send message to WebSocket consumers

            # Send the serialized data as a JSON object through WebSocket
            serialized_user = UserSerializer(user)  # Serialize the user object
            user_data = serialized_user.data  # Get the data as a dictionary
            
            # Trigger WebSocket message for user creation with full user data
            send_message_to_users(user_data)  # Send complete user data to WebSocket consumers

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='fields', type=OpenApiTypes.STR)
        ]
    )
)
class UserApiView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    filterset_class = ProfileFilter

    def get(self, request):
        fields = request.GET.get('fields', None)
        filtered_queryset = self.filter_queryset(self.queryset)
        if fields is not None:
            fields = fields.split(',')
            data = list(filtered_queryset.values(*fields))
            return Response(data)
        else:
            return Response(data= self.serializer_class(filtered_queryset.all(), many=True).data )


class UserDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'username'
    lookup_field = "user__username"

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the user profile instance
        data = request.data

        # Perform the update
        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            updated_instance = serializer.save()

            # Trigger WebSocket message for user update
            #message = f"User {updated_instance.user.username} has been updated."
            #send_message_to_users(message)  # Send message to WebSocket consumers

            # Send the updated user data as a JSON object through WebSocket
            serialized_user = UserProfileSerializer(updated_instance)  # Serialize the updated user profile
            updated_user_data = serialized_user.data  # Get the data as a dictionary

            # Trigger WebSocket message for user update with full updated data
            send_message_to_users(updated_user_data)  # Send updated data to WebSocket consumers

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        user = self.get_object()  # Get the user profile instance
        username = user.user.username

        # Serialize user data to send it after deletion
        serialized_user = UserProfileSerializer(user)  # Serialize the user profile data
        user_data = serialized_user.data  # Get the data as a dictionary

        # Delete the user
        user.delete()

        # Trigger WebSocket message for user deletion with the deleted user data
        send_message_to_users(user_data)  # Send deleted user data to WebSocket consumers

        # Trigger WebSocket message for user deletion
        #message = f"User {username} has been deleted."
        #send_message_to_users(message)  # Send message to WebSocket consumers

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RequestPasswordReset(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.filter(email__iexact=email).first()

            if user:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user) 
                reset = PasswordReset(email=email, token=token)
                reset.save()

                reset_url = "https://ev4eu.rid-ppcinspectra.com/password-reset/?" + token

                send_mail(
                    "[O-V2X-MP] Password Reset Instructions",
                    "Please use the following URL to reset your password: " + reset_url,
                    settings.EMAIL_HOST_USER,   # From address (your Gmail)
                    [user.email],               # To address
                    fail_silently=False,        # Set to True if you want to silently handle errors
                )

                return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        token = data['token']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=400)
        
        user = User.objects.filter(email=reset_obj.email).first()
        
        if user:
            user.set_password(request.data['new_password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=404)
