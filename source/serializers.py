from django.db import transaction
from .question_serializers import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        fields = (
            'id',
        )


class AnonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Anonym

        fields = (
            'id',
        )


class SecureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Anonym

        fields = (
            'id',
        )


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager

        fields = (
            'id',
        )


class PhysicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Anonym

        fields = (
            'id',
        )


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Anonym

        fields = (
            'id',
        )


class TranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager

        fields = (
            'id',
        )


