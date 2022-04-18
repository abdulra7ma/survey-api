from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (LogInSerializer, RegisterationSerializer,
                          RegisterionAdministratorSerializer, UserSerializer)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterationSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Create user account, activate it directly and returns related
        tokens
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=data["email"])

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        return Response(
            data={
                "tokens": {
                    "access": str(access_token),
                    "refresh": str(access_token),
                },
                "user": UserSerializer(instance=user).data,
            }
        )


class AdministoratorRegisterView(RegisterView):
    """
    Inherits RegisterView class and overwrites
    """

    serializer_class = RegisterionAdministratorSerializer

    def post(self, request, *args, **kwargs):
        """
        Create Administorator user account
        """
        return super().post(request, *args, **kwargs)


class LogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Login a user by sending related token
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=data["email"])

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        return Response(
            data={
                "tokens": {
                    "access": str(access_token),
                    "refresh": str(access_token),
                },
                "user": UserSerializer(instance=user).data,
            }
        )
