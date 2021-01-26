import time

import aiohttp_cors
from aiohttp import web

import asyncio


class Main:

    def _run(self):
        loop = asyncio.get_event_loop()

        app = web.Application(loop=loop)
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

    async def task_check_email(self):
        while True:
            await print(1)
            time.sleep(10)
