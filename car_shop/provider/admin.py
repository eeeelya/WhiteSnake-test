from django.contrib import admin

from provider.models import Provider, ProviderCar, ProviderHistory, ProviderSale

admin.site.register(Provider)
admin.site.register(ProviderCar)
admin.site.register(ProviderSale)
admin.site.register(ProviderHistory)
