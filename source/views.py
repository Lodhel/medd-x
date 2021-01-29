from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets
from . import models, serializers, services


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

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

    def create_user(self, profile, sms_code=None, email=None, phone=None):
        instance = models.User(**{
            "profile": profile,
            "sms_code": sms_code,
            "email": email,
            "phone": phone,
            "step": 1
        })
        instance.save()

        return instance

    def identification(self, role):
        roles = {
            1: "company",
            2: "secure",
            3: "anonym",
            4: "other"
        }

        return roles[role]

    def is_step(self, data):
        pass

    def one_step(self, role, phone=None, email=None, password=None):
        if role == "secure" or role == "other":
            sms_code = services.General().generate_code()
            if not phone:
                return JsonResponse({"error": "argument not found"})
            profile = self.create_profile(
                {
                    role: True
                }
            )

            if not profile:
                JsonResponse({"error": "create error"})

            user = self.create_user(profile, sms_code, phone=phone)
            if not user:
                JsonResponse({"error": "create error"})
            #services.Twillio().send(phone, sms_code)

            return JsonResponse(
                {
                    "id": profile.pk
                }
            )
        else:
            token = services.General().generate_token()
            if not email:
                return JsonResponse({"error": "argument not found"})
            profile = self.create_profile(
                {
                    role: True,
                    "password": services.General().crypt(password),
                    "token": token,
                }
            )

            user = self.create_user(profile, email=email)
            if not user:
                JsonResponse({"error": "create error"})

            return JsonResponse(
                {
                    "id": profile.pk
                }
            )

    def step_two(self, profile_id, auth):
        try:
            user = models.User.objects.get(profile=profile_id)
            profile = models.Profile.objects.get(pk=profile_id)
        except:
            return JsonResponse({"error": "not found"})

        if user.phone:
            if user.sms_code == auth:
                profile.is_active = True
                profile.save()
                user.step = 2
                user.save()

                return JsonResponse({"id": profile_id})
            else:
                return JsonResponse({"error": "not valid"})
        else:
            if profile.token == auth:
                profile.is_active = True
                profile.save()
                user.step = 2
                user.save()

                return JsonResponse({"id": profile_id})
            else:
                return JsonResponse({"error": "not valid"})

    def step_three(self, profile_id, first_name=None, last_name=None, cover_name=None, password=None):
        try:
            user = models.User.objects.get(profile=profile_id)
            profile = models.Profile.objects.get(pk=profile_id)
        except:
            return JsonResponse({"error": "not found"})

        if user.role == "other" or user.role == "secure":
            if not password:
                return JsonResponse({"error": "field not filled"})
            profile.password = services.General().crypt(password)
            profile.save()
            user.step = 3
            user.save()
            return JsonResponse({"id": profile_id})

        if user.role == "anonym":
            if not cover_name:
                return JsonResponse({"error": "field not filled"})
            user.cover_name = cover_name
            user.step = 3
            user.save()
            return JsonResponse({"id": profile_id})

        if not first_name and not last_name:
            return JsonResponse({"error": "field not filled"})
        user.first_name = first_name
        user.last_name = last_name
        user.step = 3
        user.save()
        return JsonResponse({"id": profile_id})

    def four_step(self, profile_id, phone=None, names=None, country=None, city=None, language=None):
        try:
            user = models.User.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found"})

        if user.role == "company":
            if not phone:
                return JsonResponse({"error": "field not filled"})
            user.phone = phone
            user.step = 4
            user.save()
            return JsonResponse({"id": profile_id})

        if user.role == "anonym":
            if not language:
                return JsonResponse({"error": "field not filled"})
            user.language = language
            user.country = country
            user.city = city
            user.step = 4
            user.save()
            return JsonResponse({"id": profile_id})

        user.first_name = names["first_name"]
        user.middle_name = names["middle_name"]
        user.last_name = names["last_name"]
        user.step = 4
        user.save()
        return JsonResponse({"id": profile_id})

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
        user = self.make_struct(profile, sms_code)

        for key, value in data.items():
            user[key] = value

        if not user["email"] and not user["phone"]:
            return JsonResponse({
                "error": "attribute not found"
            })

        del user["password"]
        instance = models.User(**user)
        instance.save()
        del user["sms_code"]
        user["profile"] = profile.id

        self.send(user["phone"], user["email"])

        return JsonResponse(user)