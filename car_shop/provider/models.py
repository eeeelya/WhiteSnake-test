import datetime

from django.core.validators import MinValueValidator
from django.db import models

from core.models import Car, SpecialInformation, User, UserInformation
from shop.models import Shop


class Provider(SpecialInformation, UserInformation):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=120)
    foundation_year = models.DateField(default=datetime.date.today().year)
    total_clients = models.IntegerField(default=0)
    balance = models.DecimalField(
        default=0, max_digits=15, decimal_places=2, validators=[MinValueValidator(0)]
    )
    cars = models.ManyToManyField(Car, through="ProviderCar")

    # @property
    # запрос

    class Meta:
        db_table = "provider"


class ProviderCar(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "provider_car"


class ProviderHistory(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Shop, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField(default=datetime.datetime.now)
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = "provider_history"
