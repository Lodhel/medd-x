import asyncio

from gino import Gino

db = Gino()


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer(), primary_key=True)
    is_active = db.Column()
    date_joined = db.Column()


class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer(), primary_key=True)
    profile = db.Column()
    email = db.Column(db.EmailType(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    sms_code = db.Column()


async def connect():
    await db.set_bind('postgres:q319546//localhost/med')

asyncio.get_event_loop().run_until_complete(connect())