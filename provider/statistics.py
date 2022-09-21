from django.db.models import Count, F

from provider.models import ProviderCar, ProviderHistory


def get_sold_cars(provider_id=None):
    return ProviderHistory.objects.filter(provider__id=provider_id).values("car").annotate(car_count=Count("car"))


def get_unsold_cars(provider_id=None):
    return ProviderCar.objects.filter(provider__id=provider_id).values("car").annotate(car_count=F("count"))
