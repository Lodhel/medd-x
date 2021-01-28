from django.db import transaction
from rest_framework import serializers
from . import models, services


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient

        fields = (
            'id', 'first_name', 'last_name', 'cover_name',
            'secure', 'phone', 'language', 'country', 'city'
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