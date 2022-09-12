import datetime

from rest_framework import serializers

from core.models import Car, User
from shop.models import Shop, ShopCar, ShopHistory, ShopSale


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            "name",
            "specification",
            "balance",
            "location",
            "phone_number",
        )

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)

        return Shop.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.updated = datetime.datetime.now()

        return instance


class ShopCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCar
        fields = (
            "shop",
            "car",
            "price",
            "count",
        )


class ShopHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopHistory
        fields = (
            "client",
            "car",
            "shop",
            "price",
            "date",
        )


class ShopSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSale
        fields = (
            "car",
            "name",
            "start_date",
            "end_date",
            "discount_amount",
            "description",
        )

    def create(self, validated_data):
        provider = Car.objects.get(user=self.context["request"].user.id)

        return ShopSale.objects.create(car=provider, **validated_data)

    def update(self, instance, validated_data):
        instance.updated = datetime.datetime.now()

        return instance
