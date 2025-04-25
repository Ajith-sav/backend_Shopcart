from django.urls import path

from .views import *

urlpatterns = [
    path("signup/", CustomUserRegisterView.as_view(), name="signup"),
    path("signin/", CustomUserLoginView.as_view(), name="signin"),
    path("signout/", CustomUserLogout.as_view(), name="signout"),
    path("user/", UserDetailView.as_view(), name="user"),
    path("change-password/", AccountPasswordChange.as_view(), name="change-password"),
    path("send_otp/", SendOTPView.as_view(), name="send_otp"),
    path("verify_otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("reset_password/", PasswordResetView.as_view(), name="reset-password"),
]
