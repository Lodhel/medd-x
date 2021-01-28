from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets
from . import models, serializers, services


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

    @transaction.atomic()
    def create_profile(self, data):
        instance = models.Profile(**data)
        instance.save()

        return instance

    def make_struct(self, profile, sms_code):
        return {
            "profile": profile,
            "sms_code": sms_code,
            "email": None,
            "phone": None,
            "secure": False
        }

    def send(self, phone, email):
        if phone:
            pass
            #services.Twillio().send(validated_data["phone"], sms_code)
        if email:
            pass

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        instance = super().create(request)
        try:
            return JsonResponse(instance)
        except TypeError:
            pass
        data = request.data
        try:
            password = services.General().crypt(data["password"])
        except KeyError:
            return JsonResponse({
                "error": "attribute not found"
            })
        profile = self.create_profile(
            {
                "is_active": False,
                "password": password
            }
        )
        sms_code = services.General().generate_code()
        patient = self.make_struct(profile, sms_code)

        for key, value in data.items():
            patient[key] = value

        if not patient["email"] and not patient["phone"]:
            return JsonResponse({
                "error": "attribute not found"
            })

        del patient["password"]
        instance = models.Patient(**patient)
        instance.save()
        del patient["sms_code"]
        patient["profile"] = profile.id

        self.send(patient["phone"], patient["email"])

        return JsonResponse(patient)