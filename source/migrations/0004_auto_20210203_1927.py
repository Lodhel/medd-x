# Generated by Django 3.1.5 on 2021-02-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0003_auto_20210203_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default='2021-02-03 19:27'),
        ),
    ]
