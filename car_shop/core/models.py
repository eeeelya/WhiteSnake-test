import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries import fields


class UserInformation(models.Model):
    location = fields.CountryField()
    phone_number = models.CharField(null=True, validators=[RegexValidator(regex=r"^\+?1?\d{9,15}$")], max_length=12)

    class Meta:
        abstract = True


class SpecialInformation(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True


class Car(SpecialInformation):
    class FuelType(models.TextChoices):
        PETROL = "P", _("Petrol")
        DIESEL = "D", _("Diesel")
        ELECTRIC = "E", _("Electric")
        HYBRID = "H", _("Hybrid")
        CAS = "G", _("Gas")

    class CarType(models.TextChoices):
        SEDAN = "Sed", _("Sedan")
        CABRIOLET = "Cab", _("Cabriolet")
        MINIVAN = "Van", _("Minivan")
        COUPE = "Cou", _("Coupe")
        PICKUP = "Pic", _("Pickup")
        HATCHBACK = "Hat", _("Hatchback")

    name = models.CharField(default="", max_length=120)
    manufacture_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)]
    )
    type = models.CharField(max_length=3, choices=CarType.choices, default=CarType.SEDAN)
    fuel = models.CharField(max_length=1, choices=FuelType.choices, default=FuelType.PETROL)
    color = models.CharField(default="", max_length=20)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "car"


class User(AbstractUser):
    class UserType(models.IntegerChoices):
        UNKNOWN = 0
        CLIENT = 1
        PROVIDER = 2
        SHOP_MANAGER = 3
        ADMIN = 4

    user_type = models.IntegerField(choices=UserType.choices, default=UserType.UNKNOWN)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = "user"


class Sale(SpecialInformation):
    name = models.CharField(default="", max_length=120)
    start_datetime = models.DateTimeField(default=datetime.datetime.now)
    end_datetime = models.DateTimeField(default=datetime.datetime.now)
    discount_amount = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
