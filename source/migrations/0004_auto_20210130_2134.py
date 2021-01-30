# Generated by Django 3.1.5 on 2021-01-30 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0003_auto_20210130_2001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='type',
            new_name='type_c',
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
