from django.contrib import admin

from .models import Shop, ShopCar, ShopHistory, ShopSale

admin.site.register(Shop)
admin.site.register(ShopCar)
admin.site.register(ShopSale)
admin.site.register(ShopHistory)
