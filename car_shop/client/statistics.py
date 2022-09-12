from django.db.models import Count, Sum

from shop.models import ShopHistory


def get_own_cars(pk=None):
    return ShopHistory.objects.filter(client__id=pk).values("car").annotate(car_count=Count("car"))


def get_costs(pk=None):
    return ShopHistory.objects.filter(client__id=pk).aggregate(total_costs=Sum("price"))
