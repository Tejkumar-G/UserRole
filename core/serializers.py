"""
Serializers for user role application.
"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user."""

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'password', 'groups', 'strategy_access'
        ]
        read_only_fields = ['id', 'groups', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True},
            'strategy_access': {'read_only': True},
        }
        depth = 1

    def create(self, validated_data):
        """Create the user with password."""
        password = validated_data.pop('password', None)
        email = validated_data.pop('email')
        user = get_user_model().objects.create_user(email=email, **validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class LoginUserSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        attrs['user'] = user
        return attrs
