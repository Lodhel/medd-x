import datetime

from django.db import models
from .services import General


class Profile(models.Model):
    token = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.date.today().strftime('%Y-%m-%d %H:%M'))
    secure = models.BooleanField(default=False)
    anonym = models.BooleanField(default=False)
    company = models.BooleanField(default=False)
    other = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'profile'


class User(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    email = models.EmailField(max_length=32, unique=True, null=True)
    phone = models.CharField(max_length=16, unique=True, null=True)  # secure
    sms_code = models.CharField(max_length=4, null=True)  # secure
    cover_name = models.CharField(max_length=64, null=True)  # anonym
    first_name = models.CharField(max_length=64, null=True)  # secure
    middle_name = models.CharField(max_length=64, null=True)  # company
    last_name = models.CharField(max_length=64, null=True)  # secure
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
    step = models.IntegerField(default=0)

    def __str__(self):
        return str(self.profile)

    class Meta:
        db_table = 'user'
