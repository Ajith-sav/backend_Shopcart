from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "phone_number",
            "is_vendor",
            "password",
            "password2",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "password field does not match"}
            )
        if CustomUser.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError(
                {"username": ("A user with that username already exists.")}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return {"message": "User signup successful."}
