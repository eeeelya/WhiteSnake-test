from django.contrib.auth.hashers import make_password

import factory.fuzzy
from core.models import User
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    username = factory.Sequence(lambda n: "demo-user-%d" % n)
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))
    user_type = factory.fuzzy.FuzzyChoice(choices=User.UserType.choices, getter=lambda c: c[0])
    is_staff = False
    is_superuser = False
    is_active = True
    email_confirmed = True

    class Meta:
        model = User
