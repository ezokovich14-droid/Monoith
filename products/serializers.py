"""
Serializers pour l'API products
"""
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer pour les produits
    """
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 
            'stock', 'is_active', 'availability',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_availability(self, obj):
        """
        Afficher la disponibilité
        """
        return "En stock" if obj.is_available() else "Rupture de stock"
