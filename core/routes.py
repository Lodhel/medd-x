from aiohttp import web
from aiohttp.web_response import json_response
from validate_email import validate_email

from models import Profile, Patient
from services.operations import General

from aiohttp_cors import CorsViewMixin


routes = web.RouteTableDef()


class BaseProfileLogic:
    def get_data(self, user, profile):
        return json_response(
            {
                "data": {
                    "id": profile.id,
                    "token": profile.token,
                    "is_active": profile.is_active,
                    "secure": user.secure,
                    "phone": user.phone,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.first_name,
                    "cover_name": user.first_name,
                    "language": user.language,
                    "country": user.country,
                    "city": user.city
                }
            }
        )

    def get_user_and_profile(self, auth):
        if validate_email(auth):
            user = Patient.query.where(Patient.email == auth).gino.first()
        else:
            user = Patient.query.where(Patient.phone == auth).gino.first()

        if not user:
            return json_response(
                {
                    "error": "user not found"
                }
            )

        profile = Profile.get(Patient.profile_id)

        return {
            "user": user,
            "profile": profile
        }


@routes.view("/profile/")
class ProfileViewSet(web.View, CorsViewMixin):
    async def post(self):
        data = await self.request.json()  # TODO is_active
        try:
            auth = data["auth"]
            password = General().crypt(data["password"])
        except KeyError:
            return json_response(
                {
                    "error": "parameter not found"
                }
            )

        user_data = BaseProfileLogic().get_user_and_profile(auth)
        profile = await user_data["profile"]
        user = await user_data["user"]

        if profile.password == password:
            return BaseProfileLogic().get_data(user, profile)
        else:
            return json_response(
                {
                    "error": "auth is wrong"
                }
            )


@routes.view("/check_sms/")
class ProfileViewSet(web.View, CorsViewMixin):
    async def post(self):
        data = await self.request.json()
        try:
            auth = data["auth"]
            code = data["code"]
        except KeyError:
            return json_response(
                {
                    "error": "parameter not found"
                }
            )

        user_data = BaseProfileLogic().get_user_and_profile(auth)
        profile = user_data["profile"]
        user = user_data["user"]

        if user.sms_code == code:
            profile.is_active = True
            await profile.update(is_active=True).apply()

            return BaseProfileLogic().get_data(user, profile)
        else:
            return json_response(
                {
                    "error": "code is wrong"
                }
            )