import datetime

from client.models import Client
from core.models import Base, Car
from shop.models import Shop
from django.db import models
from django.contrib.auth.models import User


class Provider(Base):
    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        db_table = 'provider'

    name = models.CharField(default='', max_length=120)
    email = models.CharField(default='', max_length=120)
    foundation_year = models.DateField(default=datetime.date.today().year)
    total_clients = models.IntegerField(default=0)
    balance = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    cars = models.ManyToManyField(Car, through='ProviderCars')


class ProviderCars(models.Model):
    class Meta:
        db_table = 'provider_car'

    price = models.IntegerField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class ProviderHistory(models.Model):
    class Meta:
        db_table = 'provider_history'

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Shop, on_delete=models.CASCADE)
    buy_time = models.DateTimeField(default=datetime.datetime.now())
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)


class UniqueClient(models.Model):
    class Meta:
        db_table = 'unique_client'

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    total_purchases = models.IntegerField(default=0)


class ProviderUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pass
