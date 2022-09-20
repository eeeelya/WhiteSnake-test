import datetime

from rest_framework import serializers

from core.models import User
from provider.models import Provider, ProviderCar, ProviderHistory, ProviderSale


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            "name",
            "foundation_year",
            "total_clients",
            "balance",
            "location",
            "phone_number",
        )

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)

        return Provider.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.updated = datetime.datetime.now()

        return super().update(instance, validated_data)


class ProviderCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderCar
        fields = (
            "provider",
            "car",
            "price",
            "count",
        )


class ProviderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderHistory
        fields = (
            "provider",
            "car",
            "shop",
            "price",
            "purchase_time",
        )


class ProviderSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderSale
        fields = (
            "shop",
            "name",
            "start_datetime",
            "end_datetime",
            "discount_amount",
            "description",
        )

    def create(self, validated_data):
        provider = Provider.objects.get(user=self.context["request"].user.id)
        return ProviderSale.objects.create(provider=provider, **validated_data)

    def update(self, instance, validated_data):
        instance.updated = datetime.datetime.now()

        return super().update(instance, validated_data)
