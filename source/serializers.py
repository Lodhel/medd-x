from django.db import transaction
from rest_framework import serializers
from . import models, services


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User

        fields = (
            'id', 'first_name', 'last_name', 'cover_name',
            'middle_name', 'phone', 'language', 'country', 'city'
        )

        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'cover_name': {'write_only': True},
            'phone': {'write_only': True},
            'sms_code': {'write_only': True}
        }

    @transaction.atomic()
    def create(self, validated_data):
        return validated_data