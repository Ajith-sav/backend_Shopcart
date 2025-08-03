from django.urls import path, include
from rest_framework.routers import DefaultRouter

from modules.banners.views import ImageViewSet


router = DefaultRouter()
router.register(r"images", ImageViewSet, basename="images")

urlpatterns = [
    path("", include(router.urls)),
]
