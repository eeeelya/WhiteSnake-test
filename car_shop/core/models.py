import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django_countries import fields
from phonenumber_field import modelfields


class UserInformation(models.Model):
    location = fields.CountryField()
    phone_number = modelfields.PhoneNumberField(unique=True, null=False, blank=False)

    class Meta:
        abstract = True


class SpecialInformation(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True


class Car(SpecialInformation):
    FUEL_CHOICES = (
        ("P", "Petrol"),
        ("D", "Diesel"),
        ("E", "Electric"),
        ("H", "Hybrid"),
        ("G", "Gas"),
    )

    CAR_TYPE_CHOICES = (
        ("Cab", "Cabriolet"),
        ("Van", "Minivan"),
        ("Cou", "Coupe"),
        ("Pic", "Pickup"),
        ("Sed", "Sedan"),
        ("Hat", "Hatchback"),
    )

    name = models.CharField(default="", max_length=120)
    manufacture_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)]
    )
    type = models.CharField(max_length=3, choices=CAR_TYPE_CHOICES, default="Sed")
    fuel = models.CharField(max_length=1, choices=FUEL_CHOICES, default="P")
    color = models.CharField(default="", max_length=20)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "car"


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, "Unknown"),
        (1, "Client"),
        (2, "Provider"),
        (3, "ShopManager"),
        (4, "Admin"),
    )

    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    # email_confirmed = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'

    class Meta:
        db_table = "user"


class Sale(SpecialInformation):
    name = models.CharField(default="", max_length=120)
    start_date = models.DateTimeField(default=datetime.datetime.now)
    end_date = models.DateTimeField(default=datetime.datetime.now)
    discount_amount = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )
    description = models.TextField(blank=True)

    class Meta:
        abstract = True
