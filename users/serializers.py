from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(
        validators=[UniqueValidator(User.objects.all(), "username already taken.")]
    )

    email = serializers.EmailField(
        max_length=127,
        validators=[UniqueValidator(User.objects.all(), "email already registered.")],
    )

    password = serializers.CharField(max_length=255, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(required=False)
    is_employee = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)

    def validate(self, data):
        if "is_employee" in data.keys():
            if data["is_employee"]:
                data["is_superuser"] = True
            return data
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

            if key == "password":
                instance.set_password(value)

        instance.save()

        return instance
