# Generated by Django 3.1.5 on 2021-01-30 17:01

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0002_auto_20210129_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'Clinic'), ('2', 'Insurance company'), ('3', 'Medtravel company'), ('4', 'Pharmaceutical company'), ('5', 'Charity foundation')], default='Clinic', max_length=64)),
                ('name', models.CharField(max_length=64, null=True)),
                ('step', models.IntegerField(default=0)),
                ('representatives_phones', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), null=True, size=None)),
                ('representatives_emails', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=64), null=True, size=None)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.RemoveField(
            model_name='profile',
            name='anonym',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='company',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='other',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='secure',
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Moscow', max_length=64),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(default='Russia', max_length=64),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='language',
            field=models.CharField(choices=[('en', 'en'), ('de', 'de'), ('fr', 'fr'), ('sp', 'sp'), ('ru', 'ru'), ('pt', 'pt'), ('it', 'it'), ('ja', 'ja'), ('ko', 'ko'), ('zh', 'zh'), ('tr', 'tr')], default='en', max_length=2),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='sms_code',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default='2021-01-30 00:00'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='company',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.profile'),
        ),
    ]
