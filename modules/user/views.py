import logging
from datetime import timedelta

import pyotp
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *
from .service import *

User = get_user_model()


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


class AccountPasswordChange(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(serializer.data.get("new_password"))
                user.save()
                update_session_auth_hash(request, user)
                return Response(
                    {"message": "Password changed successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    """View to send OTP to user's email"""

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]

        try:
            user = CustomUser.objects.get(email=email)
            otp_record = OTPService.create_or_update_otp(user)
            otp_code = OTPManager.generate_otp_code(otp_record.otp_secret)

            # Send email with OTP code (implement your email service)
            send_to_email(email, user, otp_code)

            logger.info(f"OTP sent to {email}")
            return Response(
                {"detail": "OTP sent successfully"}, status=status.HTTP_200_OK
            )

        except CustomUser.DoesNotExist:
            logger.warning(f"Attempt to send OTP to non-existent email: {email}")
            return Response(
                {"detail": "User with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error sending OTP to {email}: {str(e)}")
            return Response(
                {"detail": "Failed to send OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyOTPView(APIView):
    """View to verify OTP code"""

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp"]

        try:
            user = CustomUser.objects.get(email=email)
            otp_record = OTPService.get_valid_otp_record(user)

            if not otp_record:
                return Response(
                    {"detail": "No active OTP found or OTP expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not OTPManager.verify_otp(otp_record.otp_secret, otp_code):
                return Response(
                    {"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Mark OTP as verified
            otp_record.is_verified = True
            otp_record.save()

            logger.info(f"OTP verified for user {email}")
            return Response(
                {"detail": "OTP verified successfully"}, status=status.HTTP_200_OK
            )

        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error verifying OTP for {email}: {str(e)}")
            return Response(
                {"detail": "Error verifying OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            new_password = serializer.validated_data["new_password"]
            try:
                user = User.objects.get(email=email)

                if user:
                    user.set_password(new_password)
                    user.save()
                    return Response(
                        {"message": "Password reset successfully"},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"error": "OTP not verified"}, status=status.HTTP_400_BAD_REQUEST
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
