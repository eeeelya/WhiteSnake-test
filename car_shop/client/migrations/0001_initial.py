# Generated by Django 4.1.1 on 2022-09-07 11:05

import client.models
import datetime
import django.core.validators
from django.db import migrations, models
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('updated', models.DateTimeField(default=datetime.datetime.now)),
                ('age', models.IntegerField(default=18, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('sex', models.CharField(choices=[('M', 'Man'), ('W', 'Woman'), ('-', 'None')], default='-', max_length=1)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('specification', models.JSONField(default=client.models.get_default_specification)),
            ],
            options={
                'db_table': 'client',
            },
        ),
    ]