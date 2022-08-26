from django.core.validators import MinValueValidator
from django.db import models

from core.models import Car, SpecialInformation, User, UserInformation


class Client(SpecialInformation, UserInformation):
    SEX_CHOICES = (
        ("M", "Man"),
        ("W", "Woman"),
        ("-", "None"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=18, validators=[MinValueValidator(0)])
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="-")
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    cars = models.ManyToManyField(Car, through="ClientCar")
    specification = models.JSONField()

    class Meta:
        db_table = "client"


class ClientCar(SpecialInformation):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    class Meta:
        db_table = "client_car"
