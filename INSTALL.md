# Installation - Version Monolithe

## 📦 Installation

### 1. Créer l'environnement virtuel

```bash
cd monolith
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Effectuer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Créer un superuser

```bash
python manage.py createsuperuser
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

### 6. Accéder à l'application

- Interface admin : http://127.0.0.1:8000/admin/
- API : http://127.0.0.1:8000/api/

---

## 🧪 Tester l'application

### Créer un produit (via API)

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Dell",
    "description": "Laptop puissant",
    "price": "850.00",
    "stock": 10
  }'
```

### Créer une commande

```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
  }'
```

---

## 📊 Structure de la base de données

Tout dans **une seule base de données SQLite** :

- `users_customuser` : Utilisateurs
- `products_product` : Produits
- `orders_order` : Commandes
- `orders_orderitem` : Détails des commandes

---

## ✅ Avantages observables

1. **Simplicité** : Une seule commande pour tout lancer
2. **Transactions** : Les commandes sont atomiques
3. **Performance** : Pas de latence réseau
4. **Debugging** : Tout dans un seul processus
