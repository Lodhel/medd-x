import datetime

from django.db import models
from ..core.services.operations import General


class Profile(models.Model):
    email = models.EmailField(max_length=32, unique=True, null=True)
    token = models.CharField(max_length=255, default=General().generate_token())
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.date.today().strftime('%Y-%m-%d %H:%M'))

    def __str__(self):
        return str(self.pk)


class Patient(models.Model):
    profile = models.OneToOneField(Profile)
    secure = models.BooleanField(default=False)
    phone = models.CharField(max_length=16, null=True)  # secure
    sms_code = models.CharField(max_length=4, null=True)  # secure
    cover_name = models.CharField(max_length=32, null=True)  # anonym
    first_name = models.CharField(max_length=32, null=True)  # secure
    last_name = models.CharField(max_length=32, null=True)  # secure
    LANG_CHOICES = (
        ('1', 'en'),
        ('2', 'de'),
        ('3', 'fr'),
        ('4', 'sp'),
        ('5', 'ru'),
        ('6', 'pt'),
        ('7', 'it'),
        ('8', 'ja'),
        ('9', 'ko'),
        ('10', 'zh'),
        ('11', 'tr'),
    )
    language = models.CharField(max_length=2, choices=LANG_CHOICES)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)