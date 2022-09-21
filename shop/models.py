import datetime

from django.core.validators import MinValueValidator
from django.db import models

from client.models import Client
from core.models import Car, Sale, SpecialInformation, User, UserInformation


def get_default_specification():
    return {
        "name": "",
        "manufacture_year": "",
        "type": "",
        "fuel": "",
        "color": "",
        "price": 0,
    }


class Shop(SpecialInformation, UserInformation):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=120)
    cars = models.ManyToManyField(Car, through="ShopCar")
    specification = models.JSONField(default=get_default_specification)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])

    class Meta:
        db_table = "shop"


class ShopCar(SpecialInformation):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    class Meta:
        db_table = "shop_car"


class ShopHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    purchase_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "shop_history"


class ShopSale(Sale):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        db_table = "shop_sale"
