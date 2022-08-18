from django.contrib import admin

from .models import Provider, ProviderCar, ProviderHistory

admin.site.register(Provider)
admin.site.register(ProviderCar)
admin.site.register(ProviderHistory)
