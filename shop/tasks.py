import datetime
from decimal import Decimal

from celery import shared_task
from client.models import Client
from core.models import Car
from provider.models import Provider, ProviderCar, ProviderHistory, ProviderSale
from shop.models import Shop, ShopCar, ShopHistory, ShopSale

EXTRA_CHARGE = Decimal(1.3)


def check_provider_sales(provider, shop) -> Decimal:
    provider_sales = ProviderSale.objects.filter(provider=provider, shop=shop)

    total_sale = 0
    for sale in provider_sales:
        total_sale += sale.discount_amount

    return Decimal(total_sale)


def check_shop_sales(shop) -> Decimal:
    shop_sales = ShopSale.objects.filter(shop=shop)

    total_sale = 0
    for sale in shop_sales:
        if sale.end_date < datetime.datetime.now() < sale.end_date:
            total_sale += sale.discount_amount

    return Decimal(total_sale)


@shared_task
def buy_car():
    shops = Shop.objects.filter(user__email_confirmed=True, is_active=True)

    for shop in shops:
        specification = shop.specification.copy()

        try:
            price = specification.pop("price")
        except KeyError:
            print("You need configure price")
            continue

        car = Car.objects.get(**specification)
        if not car:
            continue

        providers = Provider.objects.filter(
            providercar__car=car, providercar__price__lte=price, providercar__count__gte=1
        )
        if not providers:
            continue

        provider = providers.order_by("providercar__price").first()
        sale = check_provider_sales(provider, shop)
        provider_car = ProviderCar.objects.get(provider=provider, car=car)
        total_price = provider_car.price * (1 - sale)

        if shop.balance > total_price:
            provider_car.updated = datetime.datetime.now()
            provider_car.count -= 1
            provider_car.save()

            provider.balance += total_price
            provider.total_clients += 1
            provider.save()

            shop_car = ShopCar.objects.update_or_create(shop=shop, car=car)
            if not shop_car[1]:
                shop_car[0].price = total_price * EXTRA_CHARGE
                shop_car[0].updated = datetime.datetime.now()
                shop_car[0].count += 1
                shop_car[0].save()

            shop.balance -= total_price
            shop.save()

            ProviderHistory.objects.create(provider=provider, car=car, shop=shop, price=total_price)

            print("OK BUY")


@shared_task
def sell_car():
    clients = Client.objects.filter(user__email_confirmed=True, is_active=True)

    for client in clients:
        specification = client.specification.copy()

        try:
            price = specification.pop("price")
        except KeyError:
            print("You need configure price")
            continue

        car = Car.objects.get(**specification)
        if not car:
            continue

        shops = Shop.objects.filter(shopcar__car=car, shopcar__price__lte=price, shopcar__count__gte=1)
        if not shops:
            continue

        shop = shops.order_by("shopcar__price").first()
        sale = check_shop_sales(shop)
        shop_car = ShopCar.objects.get(shop=shop, car=car)
        total_price = shop_car.price * (1 - sale)

        if client.balance > total_price:

            shop_car.updated = datetime.datetime.now()
            shop_car.count -= 1
            shop_car.save()

            sale = check_shop_sales(shop)
            total_price = shop_car.price * (1 - sale)
            shop.balance += total_price
            shop.save()

            client.balance -= total_price
            client.save()

            ShopHistory.objects.create(shop=shop, car=car, client=client, price=total_price)

            print("OK SELL")
