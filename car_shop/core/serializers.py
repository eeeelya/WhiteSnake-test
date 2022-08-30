from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import Car, Sale, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all)])
    password = serializers.CharField(write_only=True, required=True)
    confirmation_password = serializers.CharField(write_only=True, required=True)  # NAME

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "password",
            "confirmation_password",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmation_password"]:
            raise serializers.ValidationError({"detail": "pass != pass_2"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            user_type=validated_data["user_type"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "name",
            "manufacture_year",
            "type",
            "color",
            "fuel",
            "description",
        )


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = (
            "name",
            "start_date",
            "end_date",
            "discount_amount",
            "description",
        )
