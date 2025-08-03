from rest_framework import serializers

from modules.products.models import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "brand_name",
            "slug",
            "description",
            "image",
            "price",
            "stock",
            "available",
            "categories",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "vendor_id",
            "slug",
        ]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be a non-negative number.")
        return value

    def create(self, validated_data):
        try:
            vendor = self.context["request"].user
            categories = validated_data.pop("categories", [])
            product = Products.objects.create(vendor=vendor, **validated_data)
            product.categories.set(categories)
            return product
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["categories"] = CategorySerializer(
            instance.categories.all(), many=True
        ).data
        return representation
