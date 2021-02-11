import asyncio
import datetime
import re

from gino import Gino

from local_settings import DATABASE


db = Gino()


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer(), primary_key=True)
    is_active = db.Column()
    is_step = db.Column()
    is_send = db.Column()
    is_sms = db.Column()
    is_email = db.Column()
    check = db.Column()
    date_joined = db.Column()
    token = db.Column()
    password = db.Column()
    email = db.Column()
    phone = db.Column()
    sms_code = db.Column()
    language = db.Column()
    country = db.Column()
    city = db.Column()


class BaseLogic:

    def make_date_string(self, string):
        string = str(string)
        string = "".join(map(str, re.findall(r'\d', string)))
        return string[0:8]

    def make_time_string(self, string):
        string = str(string)
        string = "".join(map(str, re.findall(r'\d', string)))
        return string[8:12]

    async def let_email(self):
        users = await Profile.query.where(Profile.is_email == False).gino.all()
        if users:
            users = [user for user in users if int(self.make_time_string(user.check + datetime.timedelta(minutes=5))) <= int(
                         self.make_time_string(datetime.datetime.today()))]
            for user in users:
                await user.update(is_email=True).apply()

    async def let_sms(self):
        users = await Profile.query.where(Profile.is_sms == False).gino.all()
        if users:
            users = [user for user in users if int(self.make_time_string(user.check + datetime.timedelta(minutes=2))) <= int(
                         self.make_time_string(datetime.datetime.today()))]
            for user in users:
                await user.update(is_sms=True).apply()

    async def check_is_active(self):
        users = await Profile.query.where(Profile.is_active == False).gino.all()
        if users:
            return [user.delete() for user in users if int(self.make_date_string(user.date_joined+datetime.timedelta(14))) <= int(self.make_date_string(datetime.date.today()))]

    async def get_emails(self):
        users = await Profile.query.where(Profile.is_active == False).gino.all()
        if users:
            users = [user for user in users if not user.is_send and int(self.make_date_string(user.date_joined+datetime.timedelta(3))) <= int(self.make_date_string(datetime.date.today()))]
            result = [user.email for user in users if user.email]
            users = [user.update(is_send=True).apply() for user in users]

            return result
        else:
            return None

    async def get_step(self):
        users = await Profile.query.where(Profile.is_step == False).gino.all()
        if users:
            users = [user for user in users if not user.is_send and int(self.make_date_string(user.date_joined+datetime.timedelta(1))) <= int(self.make_date_string(datetime.date.today()))]
            emails = [user.email for user in users if user.email]
            phones = [user.phone for user in users if user.phone]
            users = [user.update(is_send=True).apply() for user in users]

            return {"emails": emails, "phones": phones}
        else:
            return None

    async def get_phones(self):
        users = await Profile.query.where(Profile.is_active == False).gino.all()
        if users:
            users = [user for user in users if
                     int(self.make_date_string(user.date_joined + datetime.timedelta(3))) <= int(
                         self.make_date_string(datetime.date.today()))]
            result = [user.phone for user in users if user.phone]
            users = [user.update(is_send=True).apply() for user in users]

            return result
        else:
            return None


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


class Physician(db.Model):
    __tablename__ = "physician"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    first_name = db.Column()
    middle_name = db.Column()
    last_name = db.Column()
    step = db.Column()


class Assistant(db.Model):
    __tablename__ = "assistant"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    first_name = db.Column()
    middle_name = db.Column()
    last_name = db.Column()
    step = db.Column()


class Translator(db.Model):
    __tablename__ = "translator"

    id = db.Column(db.Integer(), primary_key=True)
    profile_id = db.Column()
    first_name = db.Column()
    middle_name = db.Column()
    last_name = db.Column()
    step = db.Column()


class Cookie(db.Model):
    __tablename__ = "cookie"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column()
    date_check = db.Column()
    data = db.Column()
    src = db.Column()


class QuestionBlock(db.Model):
    __tablename__ = "question_block"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column()
    description = db.Column()
    question_list = db.Column()
    question_group_list = db.Column()


class QuestionGroup(db.Model):
    __tablename__ = "question_group"

    id = db.Column(db.Integer(), primary_key=True)
    question_list = db.Column()


class Question(db.Model):
    __tablename__ = "question"

    id = db.Column(db.Integer(), primary_key=True)
    quest = db.Column()


class Answer(db.Model):
    __tablename__ = "answer"

    id = db.Column(db.Integer(), primary_key=True)
    quest = db.Column()
    answer = db.Column()


class Chapter(db.Model):
    __tablename__ = "chapter"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column()
    description = db.Column()
    question_list = db.Column()
    question_group_list = db.Column()
    question_block_list = db.Column()


class Questionnarie(db.Model):
    __tablename__ = "questionnarie"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column()
    description = db.Column()
    question_list = db.Column()
    question_group_list = db.Column()
    question_block_list = db.Column()
    chapter_list = db.Column()


async def connect():
    await db.set_bind('postgresql://{}:{}@{}/{}'.format(
        DATABASE["USERNAME"], DATABASE["PASSWORD"], DATABASE["HOST"], DATABASE["NAME"]
    ))

asyncio.get_event_loop().run_until_complete(connect())