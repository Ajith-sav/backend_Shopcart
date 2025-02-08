from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Banner
from .permissions import IsStaffAndSelf
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffAndSelf]
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Banner.objects.all()

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        image = request.FILES.get("image")

        if not image:
            return Response({"error": "No image provided"}, status=400)

        image_blob = image.read()
        instance = Banner.objects.create(
            staff=request.user, name=name, image_blob=image_blob
        )

        return Response({"id": instance.id, "message": "Image stored successfully"})

    def destroy(self, request, pk=None):
        image = get_object_or_404(Banner, id=pk)
        image.delete()
        return Response({"message": "Image deleted successfully"}, status=200)
