"""
Script de démonstration du MONOLITHE
Exécuter : python test_monolith.py

Ce script démontre les avantages du monolithe :
- Transactions atomiques
- Accès direct aux modèles
- Pas de latence réseau
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import CustomUser
from products.models import Product
from orders.models import Order, OrderItem
from notifications.services import send_order_confirmation
from django.db import transaction


def test_monolith():
    """
    Test complet du monolithe
    """
    print("=" * 60)
    print("🏢 DÉMONSTRATION DU MONOLITHE")
    print("=" * 60)
    
    # 1. Créer un utilisateur
    print("\n📝 Étape 1 : Création d'un utilisateur")
    user, created = CustomUser.objects.get_or_create(
        username='john_doe',
        defaults={
            'email': 'john@example.com',
            'phone': '+228 90 00 00 00',
            'address': 'Lomé, Togo'
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    print(f"✅ Utilisateur créé : {user.username} ({user.email})")
    
    # 2. Créer des produits
    print("\n📦 Étape 2 : Création de produits")
    products_data = [
        {'name': 'Laptop Dell XPS 15', 'description': 'Ordinateur portable haut de gamme', 'price': 850000, 'stock': 5},
        {'name': 'iPhone 15 Pro', 'description': 'Smartphone Apple dernière génération', 'price': 650000, 'stock': 10},
        {'name': 'AirPods Pro', 'description': 'Écouteurs sans fil Apple', 'price': 85000, 'stock': 20},
    ]
    
    products = []
    for data in products_data:
        product, created = Product.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        products.append(product)
        print(f"✅ Produit : {product.name} - {product.price} FCFA (Stock: {product.stock})")
    
    # 3. Créer une commande (TRANSACTION ATOMIQUE)
    print("\n🛒 Étape 3 : Création d'une commande (Transaction atomique)")
    
    try:
        with transaction.atomic():
            # Créer la commande
            order = Order.objects.create(user=user)
            print(f"✅ Commande #{order.id} créée pour {user.username}")
            
            # Ajouter des items
            items_to_add = [
                {'product': products[0], 'quantity': 1},  # Laptop
                {'product': products[2], 'quantity': 2},  # AirPods x2
            ]
            
            for item_data in items_to_add:
                product = item_data['product']
                quantity = item_data['quantity']
                
                # Vérifier le stock (ACCÈS DIRECT au modèle)
                if not product.is_available(quantity):
                    raise Exception(f"Stock insuffisant pour {product.name}")
                
                # Créer l'item
                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                print(f"  📌 Item ajouté : {product.name} x{quantity} = {item.subtotal} FCFA")
                
                # Réduire le stock (ACCÈS DIRECT - pas d'API)
                product.reduce_stock(quantity)
                print(f"  📉 Stock réduit : {product.name} (reste : {product.stock})")
            
            # Calculer le total
            order.calculate_total()
            print(f"\n💰 Montant total : {order.total_amount} FCFA")
            
            # Envoyer notification (APPEL LOCAL - pas d'API)
            print("\n📧 Envoi de la notification...")
            send_order_confirmation(order)
            
            print("\n✅ COMMANDE CRÉÉE AVEC SUCCÈS !")
            print(f"   Transaction atomique : TOUTES les opérations ont réussi")
            
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        print("   Transaction atomique : ROLLBACK de toutes les opérations")
    
    # 4. Afficher les commandes de l'utilisateur
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES COMMANDES")
    print("=" * 60)
    
    user_orders = Order.objects.filter(user=user)
    for order in user_orders:
        print(f"\n🧾 Commande #{order.id}")
        print(f"   Statut : {order.get_status_display()}")
        print(f"   Total : {order.total_amount} FCFA")
        print(f"   Date : {order.created_at.strftime('%d/%m/%Y %H:%M')}")
        print(f"   Articles :")
        for item in order.items.all():
            print(f"     - {item.product.name} x{item.quantity} = {item.subtotal} FCFA")
    
    # 5. Vérifier les stocks
    print("\n" + "=" * 60)
    print("📦 STOCKS ACTUELS")
    print("=" * 60)
    
    for product in Product.objects.all():
        availability = "✅ En stock" if product.is_available() else "❌ Rupture"
        print(f"{availability} - {product.name} : {product.stock} unités")
    
    print("\n" + "=" * 60)
    print("🎯 AVANTAGES DU MONOLITHE DÉMONTRÉS :")
    print("=" * 60)
    print("✅ 1. Transaction atomique (tout ou rien)")
    print("✅ 2. Accès direct aux modèles (pas d'API)")
    print("✅ 3. Pas de latence réseau")
    print("✅ 4. Communication interne rapide")
    print("✅ 5. Simplicité de développement")
    print("=" * 60)


if __name__ == '__main__':
    test_monolith()
