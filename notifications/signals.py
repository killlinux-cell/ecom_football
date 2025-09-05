"""
Signaux Django pour déclencher automatiquement les emails
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .email_service import email_service
from orders.models import Order
from payments.models import Payment
from products.models import Product
from cart.models import CartItem
from django.contrib.auth.models import User


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """Envoie un email de confirmation lors de la création d'une commande"""
    if created:
        # Attendre un peu pour s'assurer que tous les OrderItems sont créés
        from django.db import transaction
        transaction.on_commit(
            lambda: email_service.send_order_confirmation(instance)
        )


@receiver(post_save, sender=Payment)
def send_payment_confirmation_email(sender, instance, created, **kwargs):
    """Envoie un email de confirmation lors de la validation d'un paiement"""
    if instance.status == 'completed' and instance.completed_at:
        # Vérifier si c'est un nouveau paiement validé
        if created or (not created and instance._state.adding is False):
            # Vérifier si l'email n'a pas déjà été envoyé
            from .models import EmailLog
            existing_log = EmailLog.objects.filter(
                payment=instance,
                template__template_type='payment_confirmation',
                status='sent'
            ).exists()
            
            if not existing_log:
                email_service.send_payment_confirmation(instance)


@receiver(pre_save, sender=Order)
def send_shipping_notification_email(sender, instance, **kwargs):
    """Envoie un email de notification lors de l'expédition"""
    if instance.pk:  # Commande existante
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            # Vérifier si le statut a changé vers 'shipped'
            if (old_instance.status != 'shipped' and 
                instance.status == 'shipped'):
                email_service.send_shipping_notification(instance)
        except Order.DoesNotExist:
            pass


@receiver(pre_save, sender=Order)
def send_delivery_notification_email(sender, instance, **kwargs):
    """Envoie un email de notification lors de la livraison"""
    if instance.pk:  # Commande existante
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            # Vérifier si le statut a changé vers 'delivered'
            if (old_instance.status != 'delivered' and 
                instance.status == 'delivered'):
                email_service.send_delivery_notification(instance)
        except Order.DoesNotExist:
            pass


@receiver(pre_save, sender=Product)
def send_stock_alert_email(sender, instance, **kwargs):
    """Envoie une alerte de stock faible"""
    if instance.pk:  # Produit existant
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            # Vérifier si le stock a baissé en dessous du seuil
            if (old_instance.stock > 5 and instance.stock <= 5):
                email_service.send_stock_alert(instance, instance.stock)
        except Product.DoesNotExist:
            pass


# Fonction pour gérer les rappels de panier abandonné
def send_cart_reminder_emails():
    """Envoie des rappels pour les paniers abandonnés"""
    from django.utils import timezone
    from datetime import timedelta
    
    # Récupérer les utilisateurs avec des paniers abandonnés depuis 24h
    cutoff_time = timezone.now() - timedelta(hours=24)
    
    # Récupérer les utilisateurs uniques avec des paniers
    users_with_carts = User.objects.filter(
        cart_items__created_at__lt=cutoff_time,
        cart_items__isnull=False
    ).distinct()
    
    for user in users_with_carts:
        # Récupérer les articles du panier
        cart_items = CartItem.objects.filter(
            cart__user=user,
            created_at__lt=cutoff_time
        )
        
        if cart_items.exists():
            # Vérifier si un rappel n'a pas déjà été envoyé
            from .models import EmailLog
            existing_reminder = EmailLog.objects.filter(
                user=user,
                template__template_type='cart_reminder',
                created_at__gte=cutoff_time
            ).exists()
            
            if not existing_reminder:
                email_service.send_cart_reminder(user, cart_items)


# Commande de gestion pour les rappels de panier
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Envoie les rappels de panier abandonné'
    
    def handle(self, *args, **options):
        self.stdout.write("Envoi des rappels de panier abandonné...")
        send_cart_reminder_emails()
        self.stdout.write(
            self.style.SUCCESS("Rappels de panier envoyés avec succès!")
        )
