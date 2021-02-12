import datetime

from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets
from . import models, serializers, services, send_service


class UserViewSet:

    def check_for_unique(self, data):
        if "phone" in data:
            try:
                profile = models.Profile.objects.get(phone=data["phone"])
                return profile
            except:
                pass
        elif "email" in data:
            try:
                profile = models.Profile.objects.get(email=data["email"])
                return profile
            except:
                return None
        else:
            return None


    def save_cookie(self, data, cookie, url):
        if data:
            data_set = ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"]
        else:
            data_set = None

        instance = {
            "data": data_set,
            "title": cookie,
            "src": url
        }

        frame = models.Cookie(**instance)
        frame.save()

    @transaction.atomic()
    def create_profile(self, data):
        if self.check_for_unique(data):
            return None
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
        try:
            UserViewSet().save_cookie(self.request.data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")
        token = self.request._request.META['HTTP_AUTHORIZATION']
        try:
            profile = models.Profile.objects.get(token=token)
            company = models.Company.objects.get(profile=profile.id)
            data = {
                "user": {
                    "id": profile.id,
                    "email": profile.email,
                    "phone": profile.phone,
                    "language": profile.language,
                    "country": profile.country,
                    "city": profile.city,
                    "type_c": company.type_c,
                    "name": company.name,
                    "step": company.step,
                    "representatives_phones": company.representatives_phones,
                    "representatives_emails": company.representatives_emails
                }
            }
            return JsonResponse({"success": True, "data": data})
        except:
            return JsonResponse({'success': False})

    def is_step(self, data):
        try:
            UserViewSet().save_cookie(data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")

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
            sms_code = services.General().generate_code()
            profile = UserViewSet().create_profile(
                {
                    "password": services.General().crypt(data["password"]),
                    "token": token,
                    "sms_code": sms_code,
                    "email": data["email"]
                }
            )
            if not profile:
                return JsonResponse({"error": "email field is unique", "success": False})

            user = UserViewSet().create_user(profile, models.Company)
            if not user:
                return JsonResponse({"error": "create error", "success": False})

            profile.check = datetime.datetime.today()
            profile.is_email = False
            profile.save()

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
            profile = models.Profile.objects.get(pk=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        is_unique = UserViewSet().check_for_unique(data)
        if is_unique:
            return JsonResponse({"error": "phone field is unique", "success": False})

        profile.phone = phone
        profile.save()
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
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        # TODO created users

        user.representatives_phones = representatives_phones  # TODO send invite to phones
        user.representatives_emails = representatives_emails  # TODO send invite to emails
        user.step = 6
        user.save()
        profile.is_step = True
        profile.save()
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
        try:
            UserViewSet().save_cookie(self.request.data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")
        token = self.request._request.META['HTTP_AUTHORIZATION']
        try:
            profile = models.Profile.objects.get(token=token)
            anonym = models.Anonym.objects.get(profile=profile.id)
            data = {
                "user": {
                    "id": profile.id,
                    "email": profile.email,
                    "phone": profile.phone,
                    "language": profile.language,
                    "country": profile.country,
                    "city": profile.city,
                    "cover_name": anonym.cover_name,
                    "step": anonym.step
                }
            }
            return JsonResponse({"success": True, "data": data})
        except:
            return JsonResponse({'success': False})

    def is_step(self, data):
        try:
            UserViewSet().save_cookie(data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")

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
            sms_code = services.General().generate_code()
            profile = UserViewSet().create_profile(
                {
                    "password": services.General().crypt(data["password"]),
                    "token": token,
                    "sms_code": sms_code,
                    "email": data["email"]
                }
            )
            if not profile:
                return JsonResponse({"error": "email field is unique", "success": False})

            user = UserViewSet().create_user(profile, models.Anonym)
            send_service.Sendor().send_to_email(email=data["email"], code=sms_code)
            if not user:
                return JsonResponse({"error": "create error", "success": False})

            profile.check = datetime.datetime.today()
            profile.is_email = False
            profile.save()

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
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Anonym.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        profile.is_step = True
        profile.save()
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
        try:
            UserViewSet().save_cookie(self.request.data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")
        token = self.request._request.META['HTTP_AUTHORIZATION']
        try:
            profile = models.Profile.objects.get(token=token)
            secure = models.Secure.objects.get(profile=profile.id)
            data = {
                "user": {
                    "id": profile.id,
                    "email": profile.email,
                    "phone": profile.phone,
                    "language": profile.language,
                    "country": profile.country,
                    "city": profile.city,
                    "first_name": secure.first_name,
                    "last_name": secure.last_name,
                    "step": secure.step,
                    "questionary": secure.questionary
                }
            }
            return JsonResponse({"success": True, "data": data})
        except:
            return JsonResponse({'success': False})

    def is_step(self, data):
        try:
            UserViewSet().save_cookie(data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")

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
            token = services.General().generate_token()
            profile = UserViewSet().create_profile(
                {
                    "sms_code": sms_code,
                    "token": token,
                    "phone": data["phone"]
                }
            )
            if not profile:
                return JsonResponse({"error": "phone field is unique", "success": False})

            user = UserViewSet().create_user(profile, models.Secure)
            send_service.Sendor().send_sms(phone=data["phone"], code=sms_code)
            if not user:
                return JsonResponse({"error": "create error", "success": False})

            profile.check = datetime.datetime.today()
            profile.is_sms = False
            profile.save()

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
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Company.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})

        user.questionary = questionary
        user.step = 6
        user.save()
        profile.is_step = True
        profile.save()
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
        try:
            UserViewSet().save_cookie(self.request.data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")
        token = self.request._request.META['HTTP_AUTHORIZATION']
        try:
            profile = models.Profile.objects.get(token=token)
            manager = models.Manager.objects.get(profile=profile.id)
            data = {
                "user": {
                    "id": profile.id,
                    "email": profile.email,
                    "phone": profile.phone,
                    "language": profile.language,
                    "country": profile.country,
                    "city": profile.city,
                    "first_name": manager.first_name,
                    "middle_name": manager.midle_name,
                    "last_name": manager.last_name,
                    "step": manager.step
                }
            }
            return JsonResponse({"success": True, "data": data})
        except:
            return JsonResponse({'success': False})

    def is_step(self, data):
        try:
            UserViewSet().save_cookie(data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")

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
            token = services.General().generate_token()
            profile = UserViewSet().create_profile(
                {
                    "sms_code": sms_code,
                    "token": token,
                    "phone": data["phone"]
                }
            )
            if not profile:
                return JsonResponse({"error": "phone field is unique", "success": False})

            user = UserViewSet().create_user(profile, models.Manager)
            send_service.Sendor().send_sms(phone=data["phone"], code=sms_code)
            if not user:
                return JsonResponse({"error": "create error", "success": False})

            profile.check = datetime.datetime.today()
            profile.is_sms = False
            profile.save()

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
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Manager.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        profile.is_step = True
        profile.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance


class AssistantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AssistantSerializer
    queryset = models.Assistant.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            UserViewSet().save_cookie(self.request.data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")
        token = self.request._request.META['HTTP_AUTHORIZATION']
        try:
            profile = models.Profile.objects.get(token=token)
            assistant = models.Assistant.objects.get(profile=profile.id)
            data = {
                "user": {
                    "id": profile.id,
                    "email": profile.email,
                    "phone": profile.phone,
                    "language": profile.language,
                    "country": profile.country,
                    "city": profile.city,
                    "first_name": assistant.first_name,
                    "middle_name": assistant.midle_name,
                    "last_name": assistant.last_name,
                    "step": assistant.step
                }
            }
            return JsonResponse({"success": True, "data": data})
        except:
            return JsonResponse({'success': False})

    def is_step(self, data):
        try:
            UserViewSet().save_cookie(data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")

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
            token = services.General().generate_token()
            profile = UserViewSet().create_profile(
                {
                    "sms_code": sms_code,
                    "token": token,
                    "phone": data["phone"]
                }
            )
            if not profile:
                return JsonResponse({"error": "phone field is unique", "success": False})

            user = UserViewSet().create_user(profile, models.Assistant)
            send_service.Sendor().send_sms(phone=data["phone"], code=sms_code)
            if not user:
                return JsonResponse({"error": "create error", "success": False})

            profile.check = datetime.datetime.today()
            profile.is_sms = False
            profile.save()

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
            user = models.Assistant.objects.get(profile=profile_id)
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
            user = models.Assistant.objects.get(profile=profile_id)
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
            user = models.Assistant.objects.get(profile=profile_id)
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
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Assistant.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        profile.is_step = True
        profile.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance


class TranslatorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TranslatorSerializer
    queryset = models.Translator.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            UserViewSet().save_cookie(self.request.data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")
        token = self.request._request.META['HTTP_AUTHORIZATION']
        try:
            profile = models.Profile.objects.get(token=token)
            translator = models.Translator.objects.get(profile=profile.id)
            data = {
                "user": {
                    "id": profile.id,
                    "email": profile.email,
                    "phone": profile.phone,
                    "language": profile.language,
                    "country": profile.country,
                    "city": profile.city,
                    "first_name": translator.first_name,
                    "middle_name": translator.midle_name,
                    "last_name": translator.last_name,
                    "step": translator.step
                }
            }
            return JsonResponse({"success": True, "data": data})
        except:
            return JsonResponse({'success': False})

    def is_step(self, data):
        try:
            UserViewSet().save_cookie(data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")

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
            token = services.General().generate_token()
            profile = UserViewSet().create_profile(
                {
                    "sms_code": sms_code,
                    "token": token,
                    "phone": data["phone"]
                }
            )
            if not profile:
                return JsonResponse({"error": "phone field is unique", "success": False})

            user = UserViewSet().create_user(profile, models.Translator)
            send_service.Sendor().send_sms(phone=data["phone"], code=sms_code)
            if not user:
                return JsonResponse({"error": "create error", "success": False})

            profile.check = datetime.datetime.today()
            profile.is_sms = False
            profile.save()

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
            user = models.Translator.objects.get(profile=profile_id)
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
            user = models.Translator.objects.get(profile=profile_id)
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
            user = models.Translator.objects.get(profile=profile_id)
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
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Translator.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        profile.is_step = True
        profile.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance


class PhysicianViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PhysicianSerializer
    queryset = models.Physician.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            UserViewSet().save_cookie(self.request.data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")
        token = self.request._request.META['HTTP_AUTHORIZATION']
        try:
            profile = models.Profile.objects.get(token=token)
            physician = models.Physician.objects.get(profile=profile.id)
            data = {
                "user": {
                    "id": profile.id,
                    "email": profile.email,
                    "phone": profile.phone,
                    "language": profile.language,
                    "country": profile.country,
                    "city": profile.city,
                    "first_name": physician.first_name,
                    "middle_name": physician.midle_name,
                    "last_name": physician.last_name,
                    "step": physician.step
                }
            }
            return JsonResponse({"success": True, "data": data})
        except:
            return JsonResponse({'success': False})

    def is_step(self, data):
        try:
            UserViewSet().save_cookie(data, self.request._request.META["HTTP_USER_AGENT"], self.request._request.META["PATH_INFO"])
        except:
            print("cookie save error")

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
            token = services.General().generate_token()
            profile = UserViewSet().create_profile(
                {
                    "sms_code": sms_code,
                    "token": token,
                    "phone": data["phone"]
                }
            )
            if not profile:
                return JsonResponse({"error": "phone field is unique", "success": False})

            user = UserViewSet().create_user(profile, models.Physician)
            send_service.Sendor().send_sms(phone=data["phone"], code=sms_code)
            if not user:
                return JsonResponse({"error": "create error", "success": False})

            profile.check = datetime.datetime.today()
            profile.is_sms = False
            profile.save()

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
            user = models.Physician.objects.get(profile=profile_id)
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
            user = models.Physician.objects.get(profile=profile_id)
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
            user = models.Physician.objects.get(profile=profile_id)
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
            profile = models.Profile.objects.get(pk=profile_id)
            user = models.Physician.objects.get(profile=profile_id)
        except:
            return JsonResponse({"error": "not found", "success": False})
        user.language = language
        user.country = country
        user.city = city
        user.step = 5
        user.save()
        profile.is_step = True
        profile.save()
        return JsonResponse({"id": profile_id, "success": True})

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        data = request.data
        instance = self.is_step(data)
        return instance