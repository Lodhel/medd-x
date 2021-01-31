# Generated by Django 3.1.5 on 2021-01-31 15:47

import django.contrib.postgres.fields
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
                ('token', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default='2021-01-31 00:00')),
                ('email', models.EmailField(max_length=32, null=True)),
                ('phone', models.CharField(max_length=16, null=True)),
                ('sms_code', models.CharField(max_length=4, null=True)),
                ('language', models.CharField(choices=[('en', 'en'), ('de', 'de'), ('fr', 'fr'), ('sp', 'sp'), ('ru', 'ru'), ('pt', 'pt'), ('it', 'it'), ('ja', 'ja'), ('ko', 'ko'), ('zh', 'zh'), ('tr', 'tr')], default='en', max_length=2)),
                ('country', models.CharField(default='Russia', max_length=64)),
                ('city', models.CharField(default='Moscow', max_length=64)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='Secure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, null=True)),
                ('last_name', models.CharField(max_length=64, null=True)),
                ('questionary', models.TextField()),
                ('step', models.IntegerField(default=0)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.profile')),
            ],
            options={
                'db_table': 'secure',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, null=True)),
                ('middle_name', models.CharField(max_length=64, null=True)),
                ('last_name', models.CharField(max_length=64, null=True)),
                ('step', models.IntegerField(default=0)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.profile')),
            ],
            options={
                'db_table': 'manager',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_c', models.CharField(choices=[('1', 'Clinic'), ('2', 'Insurance company'), ('3', 'Medtravel company'), ('4', 'Pharmaceutical company'), ('5', 'Charity foundation')], default='Clinic', max_length=64)),
                ('name', models.CharField(max_length=64, null=True)),
                ('step', models.IntegerField(default=0)),
                ('representatives_phones', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), null=True, size=None)),
                ('representatives_emails', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=64), null=True, size=None)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.profile')),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Anonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_name', models.CharField(max_length=64, null=True)),
                ('step', models.IntegerField(default=0)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.profile')),
            ],
            options={
                'db_table': 'anonym',
            },
        ),
    ]
