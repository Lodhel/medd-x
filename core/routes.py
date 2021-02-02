import datetime

from aiohttp import web
from aiohttp.web_response import json_response
from validate_email import validate_email

from models import Profile, Company, Secure, Anonym, Manager, Cookie
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


@routes.view("/auth/company/")
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
        except ZeroDivisionError:
            return json_response(
                {
                    "error": "not found"
                }
            )

        if profile.password == password and profile.is_active:
            data = BaseProfileLogic().get_data(profile)
            return json_response(self.make_response(data, company))
        else:
            return json_response(
                {
                    "error": "auth is wrong"
                }
            )

