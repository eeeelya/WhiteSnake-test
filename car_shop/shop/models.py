import datetime

from client.models import Client
from core.models import Base, Car
from django.db import models
from django_countries import fields
from django.contrib.auth.models import User


class Shop(Base):
    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'
        db_table = 'shop'

    first_name = models.CharField(default='', max_length=120)
    location = fields.CountryField()
    phone_number = models.IntegerField(default=0)
    cars = models.ManyToManyField(Car, through='ShopCar')
    car_types = models.CharField()  # TODO
    balance = models.IntegerField(default=0)


class ShopCar(models.Model):
    class Meta:
        db_table = 'shop_car'

    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class ShopHistory(models.Model):
    class Meta:
        db_table = 'shop_history'

    date = models.DateTimeField(default=datetime.datetime.now())
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class ShopManagerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pass

