from rest_framework import serializers

from client.models import Client
from core.models import User


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
