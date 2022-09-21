from django.db.models import Count, F, Sum

from provider.models import ProviderHistory
from shop.models import ShopCar, ShopHistory


def get_costs(shop_id=None):
    return ProviderHistory.objects.filter(shop__id=shop_id).aggregate(total_costs=Sum("price"))


def get_proceeds(shop_id=None):
    return ShopHistory.objects.filter(shop__id=shop_id).aggregate(total_proceeds=Sum("price"))


def get_cars_price(shop_id=None):
    return ShopCar.objects.filter(shop__id=shop_id).values("car").annotate(cars_price=F("price") * F("count"))


def get_clients_popular_countries(shop_id=None):
    return (
        ShopHistory.objects.filter(shop__id=shop_id)
        .values("client__location")
        .annotate(location_count=Count("client__location"))
    )
