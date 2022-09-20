import factory.fuzzy
from core.factories.car import CarFactory
from factory.django import DjangoModelFactory
from shop.factories.shop import ShopFactory
from shop.models import ShopCar


class ShopCarFactory(DjangoModelFactory):
    shop = factory.SubFactory(ShopFactory)
    car = factory.SubFactory(CarFactory)
    price = "10.00"
    count = 10

    class Meta:
        model = ShopCar
