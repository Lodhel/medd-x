from django.db import transaction
from rest_framework import serializers
from . import models, services


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        fields = (
            'id', 'language', 'country', 'city'
        )