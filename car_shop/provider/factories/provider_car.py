import factory.fuzzy
from core.factories.car import CarFactory
from factory.django import DjangoModelFactory
from provider.factories.provider import ProviderFactory
from provider.models import ProviderCar


class ProviderCarFactory(DjangoModelFactory):
    provider = factory.SubFactory(ProviderFactory)
    car = factory.SubFactory(CarFactory)
    price = "10.00"
    count = 10

    class Meta:
        model = ProviderCar
