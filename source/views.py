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
    def create_user(self, profile, target):
        instance = target(**{
            "profile": profile,
            "step": 1
        })
        instance.save()
        return instance


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

            user = UserViewSet().create_user(profile, models.Company)
            if not user:
                JsonResponse({"error": "create error", "success": False})

            return JsonResponse(
                {
                    "id": profile.pk
                }
            )
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})

    def step_two(self, data):
        try:
            profile_id = data["profile_id"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        if profile.token == auth:
            profile.is_active = True
            profile.save()
            user.step = 2
            user.save()

            return JsonResponse({"id": profile_id, "success": True})
        else:
            return JsonResponse({"error": "not valid", "success": False})

    def step_three(self, data):
        try:
            profile_id = data["profile_id"]
            name = data["name"]
            type_c = data["type_c"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        user.name = name
        user.type_c = type_c
        user.step = 3
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    def step_four(self, data):
        try:
            profile_id = data["profile_id"]
            phone = data["phone"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Company.objects.get(profile=profile_id)
            profile = models.Profile.objects.get(id=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
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
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    def step_six(self, data):
        try:
            profile_id = data["profile_id"]
            representatives_phones = data["representatives_phones"]
            representatives_emails = data["representatives_emails"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        user.representatives_phones = representatives_phones
        user.representatives_emails = representatives_emails
        user.step = 6
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance


class AnonymViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AnonymSerializer
    queryset = models.Anonym.objects.all()

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

            user = UserViewSet().create_user(profile, models.Anonym)
            if not user:
                JsonResponse({"error": "create error", "success": False})

            return JsonResponse(
                {
                    "id": profile.pk,
                    "success": True
                }
            )
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})

    def step_two(self, data):
        try:
            profile_id = data["profile_id"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Anonym.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        if profile.token == auth:
            profile.is_active = True
            profile.save()
            user.step = 2
            user.save()

            return JsonResponse({"id": profile_id, "success": True})
        else:
            return JsonResponse({"error": "not valid", "success": False})

    def step_three(self, data):
        try:
            profile_id = data["profile_id"]
            cover_name = data["cover_name"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Anonym.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        user.cover_name = cover_name
        user.step = 3
        user.save()
        return JsonResponse({"id": profile_id})

    def step_four(self, data):
        try:
            profile_id = data["profile_id"]
            city = data["city"]
            country = data["country"]
            language = data["language"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Anonym.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance


class SecureViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecureSerializer
    queryset = models.Secure.objects.all()

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
            sms_code = services.General().generate_code()
            profile = UserViewSet().create_profile(
                {
                    "password": services.General().crypt(data["password"]),
                    "sms_code": sms_code,
                    "phone": data["phone"]
                }
            )

            user = UserViewSet().create_user(profile, models.Secure)
            # services.Twillio().send(phone, sms_code)
            if not user:
                JsonResponse({"error": "create error", "success": False})

            return JsonResponse(
                {
                    "id": profile.pk,
                    "success": True
                }
            )
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})

    def step_two(self, data):
        try:
            profile_id = data["profile_id"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Secure.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        if profile.sms_code == auth:
            profile.is_active = True
            profile.save()
            user.step = 2
            user.save()

            return JsonResponse({"id": profile_id, "success": True})
        else:
            return JsonResponse({"error": "not valid", "success": False})

    def step_three(self, data):
        try:
            profile_id = data["profile_id"]
            password = data["password"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Secure.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        profile.password = services.General().crypt(password)
        profile.save()
        user.step = 3
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    def step_four(self, data):
        try:
            profile_id = data["profile_id"]
            first_name = data["first_name"]
            last_name = data["last_name"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Secure.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.first_name = first_name
        user.last_name = last_name
        user.step = 4
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    def step_five(self, data):
        try:
            profile_id = data["profile_id"]
            city = data["city"]
            country = data["country"]
            language = data["language"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Secure.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    def step_six(self, data):
        try:
            profile_id = data["profile_id"]
            questionary = data["questionary"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        user.questionary = questionary
        user.step = 6
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance


class ManagerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ManagerSerializer
    queryset = models.Manager.objects.all()

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

    def one_step(self, data):
        try:
            sms_code = services.General().generate_code()
            profile = UserViewSet().create_profile(
                {
                    "password": services.General().crypt(data["password"]),
                    "sms_code": sms_code,
                    "phone": data["phone"]
                }
            )

            user = UserViewSet().create_user(profile, models.Secure)
            # services.Twillio().send(phone, sms_code)
            if not user:
                JsonResponse({"error": "create error", "success": False})

            return JsonResponse(
                {
                    "id": profile.pk,
                    "success": True
                }
            )
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})

    def step_two(self, data):
        try:
            profile_id = data["profile_id"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Manager.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        if profile.sms_code == auth:
            profile.is_active = True
            profile.save()
            user.step = 2
            user.save()

            return JsonResponse({"id": profile_id, "success": True})
        else:
            return JsonResponse({"error": "not valid", "success": False})

    def step_three(self, data):
        try:
            profile_id = data["profile_id"]
            password = data["password"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Manager.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        profile.password = services.General().crypt(password)
        profile.save()
        user.step = 3
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    def step_four(self, data):
        try:
            profile_id = data["profile_id"]
            first_name = data["first_name"]
            middle_name = data["middle_name"]
            last_name = data["last_name"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Manager.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.step = 4
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    def step_five(self, data):
        try:
            profile_id = data["profile_id"]
            city = data["city"]
            country = data["country"]
            language = data["language"]
        except KeyError:
            return JsonResponse({"error": "argument not found", "success": False})
        try:
            user = models.Manager.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance