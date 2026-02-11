"""
Views pour l'API orders
DÉMONSTRATION DES AVANTAGES DU MONOLITHE :
- Transactions atomiques
- Accès direct aux modèles
- Pas de latence réseau
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from products.models import Product
from users.models import CustomUser
from notifications.services import send_order_confirmation


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commandes
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic  # AVANTAGE MONOLITHE : Transaction atomique facile
    def create(self, request):
        """
        Créer une commande avec items
        
        DÉMONSTRATION :
        1. Validation
        2. Création de la commande
        3. Création des items
        4. Réduction du stock (accès direct au modèle Product)
        5. Envoi de notification (appel de fonction local)
        
        Tout cela dans UNE SEULE TRANSACTION !
        """
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        items_data = serializer.validated_data['items']

        try:
            # Récupérer l'utilisateur (accès direct à la DB)
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Créer la commande
        order = Order.objects.create(user=user)

        # Créer les items et vérifier le stock
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                transaction.set_rollback(True)
                return Response(
                    {'error': f'Produit {item_data["product_id"]} non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )

            quantity = item_data['quantity']

            # Vérifier la disponibilité
            if not product.is_available(quantity):
                transaction.set_rollback(True)
                return Response(
                    {'error': f'Stock insuffisant pour {product.name}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Créer l'item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

            # Réduire le stock (ACCÈS DIRECT - pas d'API)
            product.reduce_stock(quantity)

        # Calculer le total
        order.calculate_total()

        # Envoyer notification (APPEL LOCAL - pas d'API)
        send_order_confirmation(order)

        # Retourner la commande créée
        response_serializer = OrderSerializer(order)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Annuler une commande et restaurer le stock
        """
        order = self.get_object()

        if order.status != 'pending':
            return Response(
                {'error': 'Seules les commandes en attente peuvent être annulées'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Restaurer le stock
            for item in order.items.all():
                item.product.stock += item.quantity
                item.product.save()

            # Changer le statut
            order.status = 'cancelled'
            order.save()

        return Response({'message': 'Commande annulée avec succès'})

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        Récupérer les commandes de l'utilisateur connecté
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        orders = Order.objects.filter(user_id=user_id)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
