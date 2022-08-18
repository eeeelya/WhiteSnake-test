import datetime

from django.core.validators import MinValueValidator
from django.db import models

from client.models import Client
from core.models import Car, SpecialInformation, User, UserInformation


class Shop(SpecialInformation, UserInformation):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=120)
    cars = models.ManyToManyField(Car, through="ShopCar")
    car_types = models.JSONField()
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=0, validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = "shop"


class ShopCar(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    count = models.IntegerField(default=0)

    class Meta:
        db_table = "shop_car"


class ShopHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "shop_history"
