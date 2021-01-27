from django.db import transaction
from rest_framework import serializers
from . import models


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient

        fields = (
            'id', 'first_name', 'last_name', 'cover_name',
            'secure', 'email', 'password', 'phone', 'language', 'country', 'city'
        )

        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'cover_name': {'write_only': True},
            'email': {'write_only': True},
            'phone': {'write_only': True},
            'sms_code': {'write_only': True}
        }

    @transaction.atomic()
    def create_profile(self, data):
        instance = models.Profile(**data)
        instance.save()

        return instance

    @transaction.atomic()
    def create(self, validated_data):
        profile = self.create_profile(validated_data)

        validated_data["profile"] = profile
        instance = models.Patient(**validated_data)
        instance.save()

        return instance