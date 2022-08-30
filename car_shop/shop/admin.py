from django.contrib import admin

from shop.models import Shop, ShopCar, ShopHistory, ShopSale

admin.site.register(Shop)
admin.site.register(ShopCar)
admin.site.register(ShopSale)
admin.site.register(ShopHistory)
