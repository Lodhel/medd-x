# Generated by Django 3.1.5 on 2021-01-27 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=32, null=True, unique=True)),
                ('token', models.CharField(default='e44946aa-07e6-4c7a-b35c-f9b4aa32', max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default='2021-01-27 00:00')),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secure', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=16, null=True, unique=True)),
                ('sms_code', models.CharField(default='0224', max_length=4, null=True)),
                ('cover_name', models.CharField(max_length=32, null=True)),
                ('first_name', models.CharField(max_length=32, null=True)),
                ('last_name', models.CharField(max_length=32, null=True)),
                ('language', models.CharField(choices=[('1', 'en'), ('2', 'de'), ('3', 'fr'), ('4', 'sp'), ('5', 'ru'), ('6', 'pt'), ('7', 'it'), ('8', 'ja'), ('9', 'ko'), ('10', 'zh'), ('11', 'tr')], max_length=2)),
                ('country', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.profile')),
            ],
            options={
                'db_table': 'patient',
            },
        ),
    ]
