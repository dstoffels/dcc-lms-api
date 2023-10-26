from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):
    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
