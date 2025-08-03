import base64

from rest_framework import serializers

from modules.banners.models import Banner


class ImageSerializer(serializers.ModelSerializer):
    image_blob = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ["id", "name", "image_blob", "staff", "created_at"]
        extra_kwargs = {"staff": {"read_only": True}}

    def get_image_blob(self, obj):
        if obj.image_blob:
            return base64.b64encode(obj.image_blob).decode("utf-8")
        return None
