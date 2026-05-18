from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "role",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
            phone_number=validated_data["phone_number"],
        )

        role = validated_data['role']

        if role == 'supplier':
            group = Group.objects.get(name='Supplier')

        elif role == 'buyer':
            group = Group.objects.get(name='Buyer')

        elif role == 'admin':
            group = Group.objects.get(name='Admin')

        user.groups.add(group)

        return user


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)