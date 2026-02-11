"""
Serializers pour l'API users
"""
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'utilisateur
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'utilisateur
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone', 'address']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
