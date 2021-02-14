from django.db import transaction
from rest_framework import serializers
from . import models, services


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


class ChoiceSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField()

    class Meta:
        model = models.ChoiceMeasurment
        fields = ['pk', 'title', ]

    def get_percent(self, obj):
        total = models.Answer.objects.filter(question=obj.question).count()
        current = models.Answer.objects.filter(question=obj.question, choice=obj).count()
        if total != 0:
            return float(current * 100 / total)
        else:
            return float(0)


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set', )

    class Meta:
        model = models.Question
        fields = ['id', ]

