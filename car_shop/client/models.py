from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import SpecialInformation, User, UserInformation


def get_default_specification():
    return {
        "name": "",
        "price": "",
        "manufacture_year": 0,
        "type": "",
        "fuel": "",
        "color": "",
    }


class Client(SpecialInformation, UserInformation):
    SEX_CHOICES = (
        ("M", "Man"),
        ("W", "Woman"),
        ("-", "None"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=18, validators=[MinValueValidator(0), MaxValueValidator(100)])
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="-")
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    specification = models.JSONField(default=get_default_specification)

    class Meta:
        db_table = "client"
