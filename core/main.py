import aiohttp_cors
from aiohttp import web

import asyncio

from models import BaseLogic
from routes import routes


class Main:

    def _run(self):
        loop = asyncio.get_event_loop()

        app = web.Application(loop=loop)
        app.router.add_routes(routes)
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
        })

        for route in list(app.router.routes()):
            cors.add(route)

        web.run_app(app)

    async def task_is_active(self):
        while True:
            await BaseLogic().check_is_active()
            await asyncio.sleep(86400)

    async def task_is_step(self):
        while True:
            data = await BaseLogic().get_step()
            if data:
                if data["emails"]:
                    for email in data["emails"]:
                        print(email)  # TODO send info
                if data["phones"]:
                    for phone in data["phones"]:
                        print(phone)  # TODO send info
            await asyncio.sleep(86400)

    async def task_let_email(self):
        while True:
            await BaseLogic().let_email()
            await asyncio.sleep(150)

    async def task_let_sms(self):
        while True:
            await BaseLogic().let_sms()
            await asyncio.sleep(60)

    async def task_check_email(self):
        while True:
            emails = await BaseLogic().get_emails()
            if emails:
                for email in emails:
                    print(email)  # TODO send to token
            await asyncio.sleep(86400)

    async def task_check_phone(self):
        while True:
            phones = await BaseLogic().get_phones()
            if phones:
                for phone in phones:
                    print(phone)  # TODO send to code
            await asyncio.sleep(86400)
