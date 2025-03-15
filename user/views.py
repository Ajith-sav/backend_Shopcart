import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *


class CustomUserRegisterView(generics.CreateAPIView):
    serializer_class = CustomUserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "User  registration successful."},
            status=status.HTTP_201_CREATED,
        )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserRegisterSerializer(user)
        return Response(serializer.data)


class CustomUserLoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            User = get_user_model()
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request,
            email=email,
            password=password,
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Incorrect Password."}, status=status.HTTP_400_BAD_REQUEST
        )


logger = logging.getLogger(__name__)


class CustomUserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"success": False, "detail": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token, True)
            token.blacklist()
            logger.info(f"User {request.user.id} logout successful")
            return Response(
                {"success": True, "detail": "Logout successful"},
                status=status.HTTP_200_OK,
            )
        except TokenError:
            logger.warning(f"Invalid token attempt by user {request.user.id}")
            return Response(
                {"success": False, "detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
