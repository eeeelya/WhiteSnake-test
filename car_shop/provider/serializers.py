from rest_framework import serializers

from core.models import User

from .models import Provider, ProviderCar, ProviderHistory, ProviderSale


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
            "start_date",
            "end_date",
            "discount_amount",
            "description",
        )

    def create(self, validated_data):
        provider = Provider.objects.get(user=self.context["request"].user)
        return ProviderSale.objects.create(provider=provider, **validated_data)
