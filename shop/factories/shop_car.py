import factory.fuzzy
from core.factories.car import CarFactory
from factory.django import DjangoModelFactory
from shop.factories.shop import ShopFactory
from shop.models import ShopCar


class ShopCarFactory(DjangoModelFactory):
    shop = factory.SubFactory(ShopFactory)
    car = factory.SubFactory(CarFactory)
    count = factory.Faker("pyint", min_value=0, max_value=1000)
    price = "10.00"

    class Meta:
        model = ShopCar
