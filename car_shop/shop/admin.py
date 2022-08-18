from django.contrib import admin

from .models import Shop, ShopCar, ShopHistory

admin.site.register(Shop)
admin.site.register(ShopCar)
admin.site.register(ShopHistory)
