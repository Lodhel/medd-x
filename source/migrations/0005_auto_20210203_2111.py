# Generated by Django 3.1.5 on 2021-02-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0004_auto_20210203_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_send',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_step',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cookie',
            name='date_check',
            field=models.DateTimeField(default='2021-02-03 21:11'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default='2021-02-03 21:11'),
        ),
    ]
