import factory
from core.factories.user import UserFactory
from factory.django import DjangoModelFactory
from shop.models import Shop, get_default_specification


class ShopFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory, user_type=3)
    name = factory.Sequence(lambda n: "test-shop-%d" % n)
    specification = get_default_specification()
    balance = "200.00"
    # cars
    phone_number = factory.Sequence(lambda n: "123-456-789%d" % n)
    location = "BY"
    is_active = True

    class Meta:
        model = Shop
