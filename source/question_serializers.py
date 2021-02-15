from . import models
from rest_framework import serializers


class ChoiceAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceAttachment

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceAttachment(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceGender

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceGender(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceAgeGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceAgeGroups

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceAgeGroups(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceDestinationBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceDestinationBlock

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceDestinationBlock(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceDestinationChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceDestinationChapter

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceDestinationChapter(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceDefaultBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceDefaultBlock

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceDefaultBlock(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceDefaultChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceDefaultChapter

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceDefaultChapter(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceHealthStatus

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceHealthStatus(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceBioMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceBioMarket

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceBioMarket(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceMeddataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceMeddataType

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceMeddataType(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceMeasurmentDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceMeasurmentDefault

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceMeasurmentDefault(
            title=validated_data['title']
        )

        request.save()
        return request


class ChoiceMeasurmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceMeasurment

        fields = (
            'id', 'title'
        )

    def create(self, validated_data):
        request = models.ChoiceMeasurment(
            title=validated_data['title']
        )

        request.save()
        return request