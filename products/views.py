"""
Views pour l'API products
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les produits
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'stock']

    @action(detail=True, methods=['post'])
    def check_stock(self, request, pk=None):
        """
        Vérifier la disponibilité d'un produit
        """
        product = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        available = product.is_available(quantity)
        
        return Response({
            'product_id': product.id,
            'product_name': product.name,
            'requested_quantity': quantity,
            'current_stock': product.stock,
            'available': available
        })

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Lister les produits en rupture de stock
        """
        threshold = int(request.query_params.get('threshold', 5))
        products = Product.objects.filter(stock__lte=threshold, is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
