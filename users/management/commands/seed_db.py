from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product
from orders.models import Order, OrderItem
from decimal import Decimal
import random


User = get_user_model()


class Command(BaseCommand):
    help = "Remplir la base de données avec des données de test"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Démarrage du seed de la base...")

        # ======================
        # 1. Utilisateurs
        # ======================
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@test.com",
                password="admin123"
            )
            self.stdout.write("✅ Superuser créé")
        else:
            admin = User.objects.get(username="admin")

        users = []
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={
                    "email": f"user{i}@test.com",
                    "password": "test12345"
                }
            )
            users.append(user)

        self.stdout.write(f"✅ {len(users)} utilisateurs prêts")

        # ======================
        # 2. Produits
        # ======================
        Product.objects.all().delete()

        products_data = [
            ("Laptop Dell", "Laptop puissant", 850, 10),
            ("iPhone 14", "Smartphone Apple", 1200, 5),
            ("Casque Sony", "Casque antibruit", 250, 20),
            ("Clavier Mécanique", "RGB gamer", 120, 15),
        ]

        products = []
        for name, desc, price, stock in products_data:
            product = Product.objects.create(
                name=name,
                description=desc,
                price=Decimal(price),
                stock=stock,
                is_active=True
            )
            products.append(product)

        self.stdout.write(f"✅ {len(products)} produits créés")

        # ======================
        # 3. Commandes + items
        # ======================
        Order.objects.all().delete()

        for user in users:
            order = Order.objects.create(
                user=user,
                status=random.choice(['pending', 'processing', 'shipped'])
            )

            total_items = random.randint(1, 3)
            selected_products = random.sample(products, total_items)

            for product in selected_products:
                quantity = random.randint(1, 3)

                if product.is_available(quantity):
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
                    product.reduce_stock(quantity)

            order.calculate_total()

        self.stdout.write("✅ Commandes et articles créés")
        self.stdout.write(self.style.SUCCESS("🎉 Seed terminé avec succès !"))
