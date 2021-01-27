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
        user = await Patient.query.where(Patient.email == data["email"]).gino.first()

        if data["phone"]:
            return json_response(
                {
                    "data": user.sms_code
                }
            )