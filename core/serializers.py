"""
Serializers for user role application.
"""
from abc import ABC

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user."""

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'password', 'roles', 'permissions'
        ]
        read_only_fields = ['id', 'roles', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        depth = 1

    def create(self, validated_data):
        """Create the user with password."""
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        print(email, password)
        return get_user_model().objects.create_user(email=email, password=password, **validated_data)

    def update(self, instance, validated_data):
        # Exclude email field from update
        validated_data.pop('email', None)
        return super().update(instance, validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['user_id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data


