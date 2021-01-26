import datetime

from django.db import models


class Profile(models.Model):
    email = models.EmailField(max_length=32, unique=True, null=True)
    token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.date.today().strftime('%Y-%m-%d %H:%M'))  # TODO check

    def __str__(self):
        return str(self.pk)


class Patient(models.Model):
    profile = models.OneToOneField(Profile)
    secure = models.BooleanField(default=False)
    phone = models.CharField(max_length=16)