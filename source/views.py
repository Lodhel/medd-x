from django.http import JsonResponse
from rest_framework import viewsets
from . import models, serializers


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PatientSerializer
    queryset = models.Patient.objects.all()

    def list(self, request, *args, **kwargs):
        token = request._request.GET['token']
        try:
            user = models.Profile.objects.get(token=token)
            user.is_active = True
            user.save()
            return JsonResponse({"request": True})
        except:
            return JsonResponse({'response': False})