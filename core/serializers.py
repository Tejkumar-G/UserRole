"""
Serializers for user role application.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user."""

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'password', 'groups'
        ]
        read_only_fields = ['id', 'groups', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True},
        }
        depth = 1

    def create(self, validated_data):
        """Create the user with password."""
        password = validated_data.pop('password', None)
        email = validated_data.pop('email')
        user = get_user_model().objects.create_user(email=email, **validated_data)
        user.set_password(make_password(password))
        user.save()
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


