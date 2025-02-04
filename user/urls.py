from django.urls import path

from .views import (
    CustomUserLoginView,
    CustomUserLogout,
    CustomUserRegisterView,
    UserDetailView,
)

urlpatterns = [
    path("signup/", CustomUserRegisterView.as_view(), name="signup"),
    path("signin/", CustomUserLoginView.as_view(), name="signin"),
    path("signout/", CustomUserLogout.as_view(), name="signout"),
    path("user/", UserDetailView.as_view(), name="user"),
]
