from gino import Gino
import asyncio

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')


async def main():
    await db.set_bind('postgresql://localhost/med')

asyncio.get_event_loop().run_until_complete(main())