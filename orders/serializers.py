"""
Serializers pour l'API orders
"""
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer pour les articles de commande
    """
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['id', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer pour les commandes
    """
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'status', 
            'total_amount', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer pour créer une commande avec items
    """
    user_id = serializers.IntegerField()
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )

    def validate_items(self, value):
        """
        Valider les items
        """
        if not value:
            raise serializers.ValidationError("La commande doit contenir au moins un article")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Chaque item doit avoir product_id et quantity")
            if item['quantity'] <= 0:
                raise serializers.ValidationError("La quantité doit être supérieure à 0")
        
        return value
