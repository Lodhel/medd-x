from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets
from . import models, serializers, services


class UserViewSet:

    @transaction.atomic()
    def create_profile(self, data):
        instance = models.Profile(**data)
        instance.save()

        return instance

    @transaction.atomic()
    def create_user(self, profile):
        instance = models.Company(**{
            "profile": profile,
            "step": 1
        })
        instance.save()
        return instance

"""


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

        return roles[int(role)]

    def is_step(self, data):
        step = {
            1: self.one_step(data),
            2: self.step_two(data),
            3: self.step_three(data),
            4: self.step_four(data),
            5: self.step_five(data),
            6: self.one_step(data)
        }

        return step[int(data["step"])]

    def one_step(self, data):
        try:
            role = self.identification(data["role"])
            if role == "secure" or role == "other":
                sms_code = services.General().generate_code()
                profile = self.create_profile(
                    {
                        role: True
                    }
                )

                if not profile:
                    JsonResponse({"error": "create error"})

                user = self.create_user(profile, sms_code=sms_code)
                user.phone = data["phone"]
                user.save()
                #services.Twillio().send(phone, sms_code)
                return JsonResponse(
                    {
                        "id": profile.pk
                    }
                )
        except KeyError:
            pass

        try:
            token = services.General().generate_token()
            profile = self.create_profile(
                {
                    data["role"]: True,
                    "password": services.General().crypt(data["password"]),
                    "token": token,
                }
            )

            user = self.create_user(profile, email=data["email"])
            if not user:
                JsonResponse({"error": "create error"})

            return JsonResponse(
                {
                    "id": profile.pk
                }
            )
        except KeyError:
            return JsonResponse({"error": "argument not found"})

    def step_two(self, profile_id, auth=None):
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

    def step_four(self, profile_id, phone=None, names=None, country=None, city=None, language=None):
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
            if not language and not country and not city:
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

    def step_five(self, profile_id, country=None, city=None, language=None):
        try:
            user = models.User.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found"})
        if not language and not country and not city:
            return JsonResponse({"error": "field not filled"})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        return JsonResponse({"id": profile_id})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance
"""

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all()

    def list(self, request, *args, **kwargs):
        token = request._request.GET['token']
        try:
            user = models.Profile.objects.get(token=token)
            user.is_active = True
            user.save()
            return JsonResponse({"request": True})
        except:
            return JsonResponse({'response': False})

    def is_step(self, data):

        if int(data["step"]) == 1:
            return self.one_step(data)
        elif int(data["step"]) == 2:
            return self.step_two(data)
        elif int(data["step"]) == 3:
            return self.step_three(data)
        elif int(data["step"]) == 4:
            return self.step_four(data)
        elif int(data["step"]) == 5:
            return self.step_five(data)
        elif int(data["step"]) == 6:
            return self.step_six(data)

    def one_step(self, data):
        try:
            token = services.General().generate_token()
            profile = UserViewSet().create_profile(
                {
                    "password": services.General().crypt(data["password"]),
                    "token": token,
                    "email": data["email"]
                }
            )

            user = UserViewSet().create_user(profile)
            if not user:
                JsonResponse({"error": "create error"})

            return JsonResponse(
                {
                    "id": profile.pk
                }
            )
        except KeyError:
            return JsonResponse({"error": "argument not found"})

    def step_two(self, data):
        try:
            profile_id = data["profile_id"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"error": "argument not found"})
        try:
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found"})

        if profile.token == auth:
            profile.is_active = True
            profile.save()
            user.step = 2
            user.save()

            return JsonResponse({"id": profile_id})
        else:
            return JsonResponse({"error": "not valid"})

    def step_three(self, data):
        try:
            profile_id = data["profile_id"]
            name = data["name"]
            type_c = data["type_c"]
        except KeyError:
            return JsonResponse({"error": "argument not found"})
        try:
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found"})

        user.name = name
        user.type = type_c
        user.step = 3
        user.save()
        return JsonResponse({"id": profile_id})

    def step_four(self, data):
        try:
            profile_id = data["profile_id"]
            phone = data["phone"]
        except KeyError:
            return JsonResponse({"error": "argument not found"})
        try:
            user = models.Company.objects.get(profile=profile_id)
            profile = models.Profile.objects.get(id=profile_id)
        except:
            return JsonResponse({"error": "not found"})
        profile.phone = phone
        user.step = 4
        user.save()
        return JsonResponse({"id": profile_id})

    def step_five(self, data):
        try:
            profile_id = data["profile_id"]
            city = data["city"]
            country = data["country"]
            language = data["language"]
        except KeyError:
            return JsonResponse({"error": "argument not found"})
        try:
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found"})
        if not language and not country and not city:
            return JsonResponse({"error": "field not filled"})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        return JsonResponse({"id": profile_id})

    def step_six(self, data):
        try:
            profile_id = data["profile_id"]
            representatives_phones = data["representatives_phones"]
            representatives_emails = data["representatives_emails"]
        except KeyError:
            return JsonResponse({"error": "argument not found"})
        try:
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found"})

        user.representatives_phones = representatives_phones
        user.representatives_emails = representatives_emails
        user.step = 6
        user.save()
        return JsonResponse({"id": profile_id})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance