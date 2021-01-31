import asyncio

from gino import Gino

from .local_settings import DATABASE


db = Gino()


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer(), primary_key=True)
    is_active = db.Column()
    date_joined = db.Column()
    token = db.Column()
    password = db.Column()
    email = db.Column()
    phone = db.Column()
    sms_code = db.Column()
    language = db.Column()
    country = db.Column()
    city = db.Column()


class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    type_c = db.Column()
    name = db.Column()
    representatives_phones = db.Column()
    representatives_emails = db.Column()
    step = db.Column()


class Anonym(db.Model):
    __tablename__ = "anonym"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    cover_name = db.Column()
    step = db.Column()


class Secure(db.Model):
    __tablename__ = "secure"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    first_name = db.Column()
    last_name = db.Column()
    questionary = db.Column()
    step = db.Column()


class Manager(db.Model):
    __tablename__ = "manager"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    first_name = db.Column()
    middle_name = db.Column()
    last_name = db.Column()
    step = db.Column()


async def connect():
    await db.set_bind('postgresql://{}:{}@{}/{}'.format(
        DATABASE["USERNAME"], DATABASE["PASSWORD"], DATABASE["HOST"], DATABASE["NAME"]
    ))

asyncio.get_event_loop().run_until_complete(connect())