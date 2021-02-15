from . import models, serializers
from rest_framework import viewsets


class ChoiceAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceAttachmentSerializer
    queryset = models.ChoiceAttachment.objects.all()


class ChoiceGenderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceGenderSerializer
    queryset = models.ChoiceGender.objects.all()


class ChoiceAgeGroupsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceAgeGroupsSerializer
    queryset = models.ChoiceAgeGroups.objects.all()


class ChoiceDestinationBlockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceDestinationBlockSerializer
    queryset = models.ChoiceDestinationBlock.objects.all()


class ChoiceDestinationChapterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceDestinationChapterSerializer
    queryset = models.ChoiceDestinationChapter.objects.all()


class ChoiceDefaultBlockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceDefaultBlockSerializer
    queryset = models.ChoiceDefaultBlock.objects.all()


class ChoiceDefaultChapterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceDefaultChapterSerializer
    queryset = models.ChoiceDefaultChapter.objects.all()


class ChoiceHealthStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceHealthStatusSerializer
    queryset = models.ChoiceHealthStatus.objects.all()


class ChoiceBioMarketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceBioMarketSerializer
    queryset = models.ChoiceBioMarket.objects.all()


class ChoiceMeddataTypeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceMeddataTypeSerializer
    queryset = models.ChoiceMeddataType.objects.all()


class ChoiceMeasurmentDefaultViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceMeasurmentDefaultSerializer
    queryset = models.ChoiceMeasurmentDefault.objects.all()


class ChoiceMeasurmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChoiceMeasurmentSerializer
    queryset = models.ChoiceMeasurment.objects.all()