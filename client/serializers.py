import datetime

from django.shortcuts import get_object_or_404
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
            "specification",
            "phone_number",
        )

    def create(self, validated_data):
        user = get_object_or_404(User, id=self.context["request"].user.id)

        return Client.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.updated = datetime.datetime.now()

        return super().update(instance, validated_data)
