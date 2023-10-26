from .models import User
from CORE.serializer import ModelSerializer
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "role", "password")

    def create(self, validated_data):
        user = User(
            email=validated_data.get("email"),
            username=validated_data.get("username"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        self.context.update({"user": user})

        return user

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
