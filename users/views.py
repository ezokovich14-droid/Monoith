"""
Views pour l'API users
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer, UserCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les utilisateurs
    CRUD complet : Create, Read, Update, Delete
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """
        Récupérer les commandes d'un utilisateur
        Exemple de communication INTERNE dans le monolithe
        """
        user = self.get_object()
        from orders.models import Order
        from orders.serializers import OrderSerializer
        
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
