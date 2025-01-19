from rest_framework import serializers

from .models import Category, Products


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=False)

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
        ]

    def create(self, validated_data):
        categories_data = validated_data.pop("categories")
        print(categories_data, "categories_data")
        vendor = self.context["request"].user
        product = Products.objects.create(vendor=vendor, **validated_data)
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data["name"], defaults=category_data
            )
            product.categories.add(category)

        return product

    def update(self, instance, validated_data):
        if instance.vendor_id != self.context["request"].user.id:
            raise serializers.ValidationError(
                "You do not have permission to update this product."
            )
        categories_data = validated_data.pop("categories", None)
        if categories_data is not None:
            instance.categories.clear()
            for category_data in categories_data:
                category, created = Category.objects.get_or_create(
                    slug=category_data["slug"], defaults=category_data
                )
            instance.categories.add(category)

            instance.name = validated_data.get("name", instance.name)
            instance.brand_name = validated_data.get("brand_name", instance.brand_name)
            instance.slug = validated_data.get("slug", instance.slug)
            instance.description = validated_data.get(
                "description", instance.description
            )
            instance.image = validated_data.get("image", instance.image)
            instance.price = validated_data.get("price", instance.price)
            instance.stock = validated_data.get("stock", instance.stock)
            instance.available = validated_data.get("available", instance.available)
            instance.save()
        return instance

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive number")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be positive number")
        return value
