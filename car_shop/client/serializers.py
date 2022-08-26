from rest_framework import serializers

from core.models import User

from .models import Client, ClientCar


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "age",
            "sex",
            "balance",
            "location",
            "phone_number",
        )


class ClientCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCar
        fields = (
            "client",
            "car",
            "count",
        )

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)
        return Client.objects.create(user=user, **validated_data)
