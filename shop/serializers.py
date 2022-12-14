import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.models import User
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
        user = get_object_or_404(User, id=self.context["request"].user.id)

        return Shop.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.updated = datetime.datetime.now()

        return super().update(instance, validated_data)


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
            "purchase_time",
        )


class ShopSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSale
        fields = (
            "car",
            "name",
            "start_datetime",
            "end_datetime",
            "discount_amount",
            "description",
        )

    def create(self, validated_data):
        shop = get_object_or_404(Shop, user=self.context["request"].user.id)

        return ShopSale.objects.create(shop=shop, **validated_data)

    def update(self, instance, validated_data):
        instance.updated = datetime.datetime.now()

        return super().update(instance, validated_data)
