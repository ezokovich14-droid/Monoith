"""
Models pour la gestion des produits
"""
from django.db import models


class Product(models.Model):
    """
    Modèle pour les produits
    """
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Prix"
    )
    stock = models.IntegerField(default=0, verbose_name="Stock")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def reduce_stock(self, quantity):
        """
        Réduire le stock - Méthode interne au monolithe
        """
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False

    def is_available(self, quantity=1):
        """
        Vérifier la disponibilité
        """
        return self.is_active and self.stock >= quantity
