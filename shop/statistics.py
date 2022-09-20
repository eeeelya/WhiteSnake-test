from django.db.models import Count, F, Sum

from provider.models import ProviderHistory
from shop.models import ShopCar, ShopHistory


def get_costs(pk=None):
    return ProviderHistory.objects.filter(shop__id=pk).aggregate(total_costs=Sum("price"))


def get_proceeds(pk=None):
    return ShopHistory.objects.filter(shop__id=pk).aggregate(total_proceeds=Sum("price"))


def get_cars_price(pk=None):
    return ShopCar.objects.filter(shop__id=pk).values("car").annotate(cars_price=F("price") * F("count"))


def get_clients_popular_countries(pk=None):
    return (
        ShopHistory.objects.filter(shop__id=pk)
        .values("client__location")
        .annotate(location_count=Count("client__location"))
    )
