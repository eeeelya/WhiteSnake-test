import factory.fuzzy
from core.models import Car
from factory.django import DjangoModelFactory

FUEL_TYPE_IDS = [x[0] for x in Car.FuelType.choices]
CAR_TYPE_IDS = [x[0] for x in Car.CarType.choices]


class CarFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "test-car-%d" % n)
    manufacture_year = 2000
    fuel = factory.fuzzy.FuzzyChoice(FUEL_TYPE_IDS)
    type = factory.fuzzy.FuzzyChoice(CAR_TYPE_IDS)
    color = factory.Faker("color")
    description = "Test description"

    class Meta:
        model = Car
