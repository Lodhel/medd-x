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
    def create_profile(self, data):
        instance = models.Profile(**data)
        instance.save()

        return instance

    @transaction.atomic()
    def create(self, validated_data):
        try:
            email = validated_data["email"]
        except KeyError:
            email = None

        try:
            phone = validated_data["phone"]
        except KeyError:
            phone = None

        if not phone and not email:
            validated_data["error"]: True
            return validated_data

        profile = self.create_profile(
            {
                "is_active": False
            }
        )

        validated_data["profile"] = profile
        sms_code = services.General().generate_code()
        validated_data["sms_code"] = sms_code
        instance = models.Patient(**validated_data)
        if phone:
            pass
            #services.Twillio().send(validated_data["phone"], sms_code)
        if email:
            pass
        instance.save()
        return instance