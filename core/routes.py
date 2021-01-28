from aiohttp import web
from aiohttp.web_response import json_response
from validate_email import validate_email

from models import Profile, Patient

from aiohttp_cors import CorsViewMixin


routes = web.RouteTableDef()


@routes.view("/profile/")
class CoinViewSet(web.View, CorsViewMixin):
    async def post(self):
        data = await self.request.json()
        try:
            auth = data["auth"]
        except KeyError:
            return json_response(
                {
                    "error": "parameter not found"
                }
            )
        if validate_email(auth):
            user = await Patient.query.where(Patient.email == data["auth"]).gino.first()
        else:
            user = await Patient.query.where(Patient.phone == data["auth"]).gino.first()

        if not user:
            return json_response(
                {
                    "error": "parameter not found"
                }
            )

        profile = await Profile.get(Patient.profile_id)
        profile.is_active = True
        await profile.update(is_active=True).apply()

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