import asyncio

from gino import Gino

db = Gino()


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer(), primary_key=True)
    is_active = db.Column()
    date_joined = db.Column()
    token = db.Column()


class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    email = db.Column(nullable=True)
    phone = db.Column(db.String(), nullable=True)
    sms_code = db.Column()
    cover_name = db.Column()
    first_name = db.Column()
    last_name = db.Column()
    language = db.Column()
    country = db.Column()
    city = db.Column()
    secure = db.Column()


async def connect():
    await db.set_bind('postgresql://postgres:q319546@localhost/med')

asyncio.get_event_loop().run_until_complete(connect())