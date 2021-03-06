import datetime

from aiohttp import web
from aiohttp.web_response import json_response
from validate_email import validate_email

from models import Profile
from models import Company
from models import Secure
from models import Anonym
from models import Manager
from models import Physician
from models import Assistant
from models import Translator
from models import Cookie

from questionnarie_views import QuestionView

from services.operations import General

from aiohttp_cors import CorsViewMixin


routes = web.RouteTableDef()


class BaseView:
    async def save_cookie(self, title, data, src):

        cookie = Cookie(
            title=title,
            date_check=datetime.date.today(),
            data=data,
            src=src
        )
        await cookie.create()


class BaseProfileLogic:

    def get_data(self, profile):
        return {
            "id": profile.id,
            "token": profile.token,
            "is_active": profile.is_active,
            "phone": profile.phone,
            "sms_code": profile.sms_code,
            "email": profile.email,
            "language": profile.language,
            "country": profile.country,
            "city": profile.city
        }


@routes.view("/api/auth/company/")
class CompanyViewSet(web.View, CorsViewMixin):

    def make_response(self, data, company):
        return {
            "data": {
                **data,
                "type_c": company.type_c,
                "name": company.name,
                "representatives_phones": company.representatives_phones,
                "representatives_emails": company.representatives_emails,
                "step": company.step
            },
            "success": True
        }

    async def post(self):
        data = await self.request.json()
        await BaseView().save_cookie(self.request.headers["User-Agent"],
                                     ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"],
                                     self.request.url.raw_path_qs)
        try:
            email = data["email"]
            password = General().crypt(data["password"])
            profile = await Profile.query.where(Profile.email == email).gino.first()
            company = await Company.query.where(Company.profile_id == profile.id).gino.first()
        except:
            return json_response(
                {
                    "error": "not found",
                    "success": False
                }
            )

        if profile.password == password and profile.is_active:
            await profile.update(token=General().generate_token()).apply()
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, company))
        else:
            return json_response(
                {
                    "error": "auth is wrong",
                    "success": False
                }
            )


@routes.view("/api/auth/anonym/")
class AnonymViewSet(web.View, CorsViewMixin):

    def make_response(self, data, anonym):
        return {
            "data": {
                **data,
                "first_name": anonym.cover_name,
                "step": anonym.step
            },
            "success": True
        }

    async def post(self):
        data = await self.request.json()
        await BaseView().save_cookie(self.request.headers["User-Agent"],
                                     ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"],
                                     self.request.url.raw_path_qs)
        try:
            email = data["email"]
            password = General().crypt(data["password"])
            profile = await Profile.query.where(Profile.email == email).gino.first()
            secure = await Anonym.query.where(Anonym.profile_id == profile.id).gino.first()
        except:
            return json_response(
                {
                    "error": "not found",
                    "success": False
                }
            )

        if profile.password == password and profile.is_active:
            await profile.update(token=General().generate_token()).apply()
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, secure))
        else:
            return json_response(
                {
                    "error": "auth is wrong",
                    "success": False
                }
            )


@routes.view("/api/auth/secure/")
class SecureViewSet(web.View, CorsViewMixin):

    def make_response(self, data, secure):
        return {
            "data": {
                **data,
                "first_name": secure.first_name,
                "last_name": secure.last_name,
                "questionary": secure.questionary,
                "step": secure.step
            },
            "success": True
        }

    async def post(self):
        data = await self.request.json()
        await BaseView().save_cookie(self.request.headers["User-Agent"],
                                     ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"],
                                     self.request.url.raw_path_qs)
        try:
            auth = data["auth"]
            if validate_email(auth):
                profile = await Profile.query.where(Profile.email == auth).gino.first()
            else:
                profile = await Profile.query.where(Profile.phone == auth).gino.first()
            password = General().crypt(data["password"])
            secure = await Secure.query.where(Secure.profile_id == profile.id).gino.first()
        except:
            return json_response(
                {
                    "error": "not found",
                    "success": False
                }
            )

        if profile.password == password and profile.is_active:
            await profile.update(token=General().generate_token()).apply()
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, secure))
        else:
            return json_response(
                {
                    "error": "auth is wrong",
                    "success": False
                }
            )


@routes.view("/api/auth/manager/")
class ManagerViewSet(web.View, CorsViewMixin):

    def make_response(self, data, manager):
        return {
            "data": {
                **data,
                "first_name": manager.first_name,
                "middle_name": manager.middle_name,
                "last_name": manager.last_name,
                "step": manager.step
            },
            "success": True
        }

    async def post(self):
        data = await self.request.json()
        await BaseView().save_cookie(self.request.headers["User-Agent"],
                                     ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"],
                                     self.request.url.raw_path_qs)
        try:
            auth = data["auth"]
            if validate_email(auth):
                profile = await Profile.query.where(Profile.email == auth).gino.first()
            else:
                profile = await Profile.query.where(Profile.phone == auth).gino.first()
            password = General().crypt(data["password"])
            manager = await Manager.query.where(Manager.profile_id == profile.id).gino.first()
        except:
            return json_response(
                {
                    "error": "not found",
                    "success": False
                }
            )

        if profile.password == password and profile.is_active:
            await profile.update(token=General().generate_token()).apply()
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, manager))
        else:
            return json_response(
                {
                    "error": "auth is wrong",
                    "success": False
                }
            )


@routes.view("/api/auth/physician/")
class PhysicianViewSet(web.View, CorsViewMixin):

    def make_response(self, data, physician):
        return {
            "data": {
                **data,
                "first_name": physician.first_name,
                "middle_name": physician.middle_name,
                "last_name": physician.last_name,
                "step": physician.step
            },
            "success": True
        }

    async def post(self):
        data = await self.request.json()
        await BaseView().save_cookie(self.request.headers["User-Agent"],
                                     ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"],
                                     self.request.url.raw_path_qs)
        try:
            auth = data["auth"]
            if validate_email(auth):
                profile = await Profile.query.where(Profile.email == auth).gino.first()
            else:
                profile = await Profile.query.where(Profile.phone == auth).gino.first()
            password = General().crypt(data["password"])
            physician = await Physician.query.where(Physician.profile_id == profile.id).gino.first()
        except:
            return json_response(
                {
                    "error": "not found",
                    "success": False
                }
            )

        if profile.password == password and profile.is_active:
            await profile.update(token=General().generate_token()).apply()
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, physician))
        else:
            return json_response(
                {
                    "error": "auth is wrong",
                    "success": False
                }
            )


@routes.view("/api/auth/assistant/")
class AssistantViewSet(web.View, CorsViewMixin):

    def make_response(self, data, assistant):
        return {
            "data": {
                **data,
                "first_name": assistant.first_name,
                "middle_name": assistant.middle_name,
                "last_name": assistant.last_name,
                "step": assistant.step
            },
            "success": True
        }

    async def post(self):
        data = await self.request.json()
        await BaseView().save_cookie(self.request.headers["User-Agent"],
                                     ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"],
                                     self.request.url.raw_path_qs)
        try:
            auth = data["auth"]
            if validate_email(auth):
                profile = await Profile.query.where(Profile.email == auth).gino.first()
            else:
                profile = await Profile.query.where(Profile.phone == auth).gino.first()
            password = General().crypt(data["password"])
            assistant = await Assistant.query.where(Assistant.profile_id == profile.id).gino.first()
        except:
            return json_response(
                {
                    "error": "not found",
                    "success": False
                }
            )

        if profile.password == password and profile.is_active:
            await profile.update(token=General().generate_token()).apply()
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, assistant))
        else:
            return json_response(
                {
                    "error": "auth is wrong",
                    "success": False
                }
            )


@routes.view("/api/auth/translator/")
class TranslatorViewSet(web.View, CorsViewMixin):

    def make_response(self, data, translator):
        return {
            "data": {
                **data,
                "first_name": translator.first_name,
                "middle_name": translator.middle_name,
                "last_name": translator.last_name,
                "step": translator.step
            },
            "success": True
        }

    async def post(self):
        data = await self.request.json()
        await BaseView().save_cookie(self.request.headers["User-Agent"],
                                     ["{}: {},\r\n".format(key, value) for key, value in data.items() if key != "password"],
                                     self.request.url.raw_path_qs)
        try:
            auth = data["auth"]
            if validate_email(auth):
                profile = await Profile.query.where(Profile.email == auth).gino.first()
            else:
                profile = await Profile.query.where(Profile.phone == auth).gino.first()
            password = General().crypt(data["password"])
            translator = await Translator.query.where(Translator.profile_id == profile.id).gino.first()
        except:
            return json_response(
                {
                    "error": "not found",
                    "success": False
                }
            )

        if profile.password == password and profile.is_active:
            await profile.update(token=General().generate_token()).apply()
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, translator))
        else:
            return json_response(
                {
                    "error": "auth is wrong",
                    "success": False
                }
            )


@routes.view("/api/profile/info/")
class ProfileInfo(web.View, CorsViewMixin):

    async def get(self):
        params = self.request.rel_url.query
        if "auth" in params.keys():
            profile = await Profile.query.where(Profile.token == params["auth"]).gino.first()
            if not profile:
                return json_response({
                    "success": False,
                    "info": "user not found"
                })

            await profile.update(token=General().generate_token()).apply()
            instance = {
                "id": profile.id,
                "country": profile.country,
                "city": profile.city,
                "phone": profile.phone,
                "email": profile.email,
                "auth": profile.token
            }

            return json_response({
                "success": True,
                "data": instance
            })
        else:
            return json_response({
                "success": False,
                "info": "parameter auth not found"
            })


@routes.view("/api/question")
class QuestionViewSet(web.View, CorsViewMixin):

    async def post(self):
        data = await self.request.json()
        instance = QuestionView().post(data)

        return json_response({
            "data": instance,
            "success": True
        })