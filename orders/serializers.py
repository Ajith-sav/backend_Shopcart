from rest_framework import serializers

from products.models import *

from .models import *


class OrderItemSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "total_amount"]
        read_only_fields = ["price", "total_amount"]

    def validate(self, data):
        product = data["product"]
        quantity = data["quantity"]
        if quantity > product.stock:
            if product.stock == 0:
                raise serializers.ValidationError(f"Stock is not available")
            raise serializers.ValidationError(
                f"Only {product.stock} stock is available"
            )
        return data

    def create(self, validated_data):
        product = validated_data["product"]
        validated_data["price"] = product.price
        validated_data["total_amount"] = product.price * validated_data["quantity"]
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "placed_at", "payment_status", "owner", "items"]
