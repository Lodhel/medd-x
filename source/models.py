import datetime

from django.db import models
from .services import General
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    token = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.date.today().strftime('%Y-%m-%d %H:%M'))
    email = models.EmailField(max_length=32, null=True)
    phone = models.CharField(max_length=16, null=True)
    sms_code = models.CharField(max_length=4, null=True)
    LANG_CHOICES = (
        ('en', 'en'),
        ('de', 'de'),
        ('fr', 'fr'),
        ('sp', 'sp'),
        ('ru', 'ru'),
        ('pt', 'pt'),
        ('it', 'it'),
        ('ja', 'ja'),
        ('ko', 'ko'),
        ('zh', 'zh'),
        ('tr', 'tr'),
    )
    language = models.CharField(max_length=2, choices=LANG_CHOICES, default="en")
    country = models.CharField(max_length=64, default="Russia")
    city = models.CharField(max_length=64, default="Moscow")

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'profile'


class Company(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    COMPANY_TYPES = (
        ('1', 'Clinic'),
        ('2', 'Insurance company'),
        ('3', 'Medtravel company'),
        ('4', 'Pharmaceutical company'),
        ('5', 'Charity foundation')
    )
    type_c = models.CharField(max_length=64, choices=COMPANY_TYPES, default="Clinic")
    name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)
    representatives_phones = ArrayField(
        models.CharField(max_length=32),
        null=True
    )
    representatives_emails = ArrayField(
        models.EmailField(max_length=64),
        null=True
    )

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'company'


class Anonym(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    cover_name = models.CharField(max_length=64, null=True)
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'anonym'