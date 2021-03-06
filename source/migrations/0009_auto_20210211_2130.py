# Generated by Django 3.1.5 on 2021-02-11 18:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0008_auto_20210210_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('question_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('question_group_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('question_block_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
            ],
            options={
                'db_table': 'chapter',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quest', models.TextField()),
                ('answer', models.TextField()),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='QuestionBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('question_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('question_group_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
            ],
            options={
                'db_table': 'question_block',
            },
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
            options={
                'db_table': 'question_group',
            },
        ),
        migrations.CreateModel(
            name='Questionnarie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('question_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('question_group_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('question_block_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('chapter_list', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
            ],
            options={
                'db_table': 'questionnarie',
            },
        ),
        migrations.AlterField(
            model_name='cookie',
            name='date_check',
            field=models.DateTimeField(default='2021-02-11 21:30'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='check',
            field=models.DateTimeField(default='2021-02-11 21:30'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(default='2021-02-11 21:30'),
        ),
    ]
