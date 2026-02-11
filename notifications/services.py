"""
Service de notifications
DÉMONSTRATION : Appel de fonction locale dans le monolithe
"""
from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation(order):
    """
    Envoyer un email de confirmation de commande
    
    AVANTAGE MONOLITHE :
    - Appel de fonction directe (pas d'API)
    - Accès direct à l'objet Order
    - Pas de sérialisation/désérialisation
    """
    subject = f'Confirmation de commande #{order.id}'
    
    message = f"""
    Bonjour {order.user.username},
    
    Votre commande #{order.id} a été confirmée !
    
    Montant total : {order.total_amount} FCFA
    Statut : {order.get_status_display()}
    
    Articles commandés :
    """
    
    for item in order.items.all():
        message += f"\n- {item.product.name} x{item.quantity} = {item.subtotal} FCFA"
    
    message += f"""
    
    Merci pour votre commande !
    
    L'équipe E-Commerce
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ecommerce.com',
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        print(f"✉️  Email envoyé à {order.user.email}")
        return True
    except Exception as e:
        print(f"❌ Erreur d'envoi d'email : {e}")
        return False


def send_low_stock_alert(product):
    """
    Envoyer une alerte de stock faible
    """
    subject = f'Alerte stock faible : {product.name}'
    
    message = f"""
    ALERTE STOCK FAIBLE
    
    Produit : {product.name}
    Stock actuel : {product.stock}
    
    Veuillez réapprovisionner.
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@ecommerce.com',
            recipient_list=['admin@ecommerce.com'],
            fail_silently=False,
        )
        print(f"✉️  Alerte stock envoyée pour {product.name}")
        return True
    except Exception as e:
        print(f"❌ Erreur d'envoi d'alerte : {e}")
        return False
