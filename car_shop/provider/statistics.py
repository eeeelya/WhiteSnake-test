from django.db.models import Count, F

from provider.models import ProviderCar, ProviderHistory


def get_sold_cars(pk=None):
    return ProviderHistory.objects.filter(provider__id=pk).values("car").annotate(car_count=Count("car"))


def get_unsold_cars(pk=None):
    return ProviderCar.objects.filter(provider__id=pk).values("car").annotate(car_count=F("count"))
