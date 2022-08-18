from django.core.validators import MinValueValidator
from django.db import models

from core.models import SpecialInformation, User, UserInformation


class Client(SpecialInformation, UserInformation):
    SEX_CHOICES = (
        ("M", "Man"),
        ("W", "Woman"),
        ("-", "None"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(default="", max_length=120)
    surname = models.CharField(default="", max_length=120)
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="-")
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = "client"
