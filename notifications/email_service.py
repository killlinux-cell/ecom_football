"""
Service d'envoi d'emails pour l'e-commerce
"""

import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .models import EmailTemplate, EmailLog, EmailSettings
from orders.models import Order
from payments.models import Payment

logger = logging.getLogger(__name__)


class EmailService:
    """Service centralisé pour l'envoi d'emails"""
    
    def __init__(self):
        self.settings = self._get_email_settings()
    
    def _get_email_settings(self):
        """Récupère les paramètres email"""
        try:
            return EmailSettings.objects.first()
        except (EmailSettings.DoesNotExist, Exception):
            # Gérer le cas où la table n'existe pas encore (migrations non appliquées)
            return None
    
    def _get_template(self, template_type):
        """Récupère un template par type"""
        try:
            return EmailTemplate.objects.get(
                template_type=template_type,
                is_active=True
            )
        except (EmailTemplate.DoesNotExist, Exception):
            logger.error(f"Template {template_type} non trouvé")
            return None
    
    def _create_email_log(self, template, recipient_email, recipient_name, subject, 
                         email_data, order=None, payment=None, user=None):
        """Crée un log d'email"""
        try:
            return EmailLog.objects.create(
                template=template,
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                subject=subject,
                email_data=email_data,
                order=order,
                payment=payment,
                user=user,
                status='pending'
            )
        except Exception as e:
            logger.error(f"Erreur création log email: {str(e)}")
            return None
    
    def _send_email(self, email_log, html_content, text_content=None):
        """Envoie l'email et met à jour le log"""
        if not email_log:
            logger.error("EmailLog est None, impossible d'envoyer l'email")
            return False
            
        if not self.settings or not self.settings.is_active:
            logger.warning("Système d'email désactivé")
            email_log.status = 'failed'
            email_log.error_message = "Système d'email désactivé"
            email_log.save()
            return False
        
        try:
            # Configuration de l'email
            from_email = f"{self.settings.from_name} <{self.settings.from_email}>"
            
            # Création de l'email
            email = EmailMultiAlternatives(
                subject=email_log.subject,
                body=text_content or html_content,
                from_email=from_email,
                to=[email_log.recipient_email]
            )
            
            # Ajout du contenu HTML
            if html_content:
                email.attach_alternative(html_content, "text/html")
            
            # Envoi
            email.send()
            
            # Mise à jour du log
            email_log.status = 'sent'
            email_log.sent_at = timezone.now()
            email_log.save()
            
            logger.info(f"Email envoyé avec succès à {email_log.recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur envoi email: {str(e)}")
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
            return False
    
    def send_order_confirmation(self, order):
        """Envoie la confirmation de commande"""
        if not self.settings or not self.settings.send_order_confirmations:
            return False
        
        template = self._get_template('order_confirmation')
        if not template:
            return False
        
        # Préparation des données
        email_data = {
            'order': order,
            'order_items': order.items.all(),
            'customer_name': f"{order.user.first_name} {order.user.last_name}".strip(),
            'order_total': order.total,
            'shipping_address': order.shipping_address,
        }
        
        # Rendu du contenu
        html_content = self._render_template(template.html_content, email_data)
        text_content = self._render_template(template.text_content, email_data) if template.text_content else None
        
        # Création du log
        email_log = self._create_email_log(
            template=template,
            recipient_email=order.user.email,
            recipient_name=email_data['customer_name'],
            subject=template.subject.format(order_number=order.order_number),
            email_data=email_data,
            order=order,
            user=order.user
        )
        
        return self._send_email(email_log, html_content, text_content)
    
    def send_payment_confirmation(self, payment):
        """Envoie la confirmation de paiement"""
        if not self.settings or not self.settings.send_payment_confirmations:
            return False
        
        template = self._get_template('payment_confirmation')
        if not template:
            return False
        
        order = payment.order
        
        # Préparation des données
        email_data = {
            'order': order,
            'payment': payment,
            'order_items': order.items.all(),
            'customer_name': f"{order.user.first_name} {order.user.last_name}".strip(),
            'payment_amount': payment.amount,
            'payment_method': payment.get_payment_method_display(),
        }
        
        # Rendu du contenu
        html_content = self._render_template(template.html_content, email_data)
        text_content = self._render_template(template.text_content, email_data) if template.text_content else None
        
        # Création du log
        email_log = self._create_email_log(
            template=template,
            recipient_email=order.user.email,
            recipient_name=email_data['customer_name'],
            subject=template.subject.format(order_number=order.order_number),
            email_data=email_data,
            order=order,
            payment=payment,
            user=order.user
        )
        
        return self._send_email(email_log, html_content, text_content)
    
    def send_shipping_notification(self, order):
        """Envoie la notification d'expédition"""
        if not self.settings or not self.settings.send_shipping_notifications:
            return False
        
        template = self._get_template('order_shipped')
        if not template:
            return False
        
        # Préparation des données
        email_data = {
            'order': order,
            'order_items': order.items.all(),
            'customer_name': f"{order.user.first_name} {order.user.last_name}".strip(),
            'shipping_address': order.shipping_address,
        }
        
        # Rendu du contenu
        html_content = self._render_template(template.html_content, email_data)
        text_content = self._render_template(template.text_content, email_data) if template.text_content else None
        
        # Création du log
        email_log = self._create_email_log(
            template=template,
            recipient_email=order.user.email,
            recipient_name=email_data['customer_name'],
            subject=template.subject.format(order_number=order.order_number),
            email_data=email_data,
            order=order,
            user=order.user
        )
        
        return self._send_email(email_log, html_content, text_content)
    
    def send_delivery_notification(self, order):
        """Envoie la notification de livraison"""
        template = self._get_template('order_delivered')
        if not template:
            return False
        
        # Préparation des données
        email_data = {
            'order': order,
            'order_items': order.items.all(),
            'customer_name': f"{order.user.first_name} {order.user.last_name}".strip(),
        }
        
        # Rendu du contenu
        html_content = self._render_template(template.html_content, email_data)
        text_content = self._render_template(template.text_content, email_data) if template.text_content else None
        
        # Création du log
        email_log = self._create_email_log(
            template=template,
            recipient_email=order.user.email,
            recipient_name=email_data['customer_name'],
            subject=template.subject.format(order_number=order.order_number),
            email_data=email_data,
            order=order,
            user=order.user
        )
        
        return self._send_email(email_log, html_content, text_content)
    
    def send_cart_reminder(self, user, cart_items):
        """Envoie un rappel de panier abandonné"""
        if not self.settings or not self.settings.send_cart_reminders:
            return False
        
        template = self._get_template('cart_reminder')
        if not template:
            return False
        
        # Préparation des données
        email_data = {
            'user': user,
            'cart_items': cart_items,
            'customer_name': f"{user.first_name} {user.last_name}".strip(),
        }
        
        # Rendu du contenu
        html_content = self._render_template(template.html_content, email_data)
        text_content = self._render_template(template.text_content, email_data) if template.text_content else None
        
        # Création du log
        email_log = self._create_email_log(
            template=template,
            recipient_email=user.email,
            recipient_name=email_data['customer_name'],
            subject=template.subject,
            email_data=email_data,
            user=user
        )
        
        return self._send_email(email_log, html_content, text_content)
    
    def send_stock_alert(self, product, current_stock):
        """Envoie une alerte de stock faible aux administrateurs"""
        if not self.settings or not self.settings.send_stock_alerts:
            return False
        
        template = self._get_template('stock_alert')
        if not template:
            return False
        
        # Récupérer les administrateurs
        from django.contrib.auth.models import User
        admins = User.objects.filter(is_staff=True, is_active=True)
        
        results = []
        for admin in admins:
            # Préparation des données
            email_data = {
                'product_name': product.name,
                'product_price': float(product.price),
                'product_category': product.category.name if product.category else '',
                'current_stock': current_stock,
                'admin_name': f"{admin.first_name} {admin.last_name}".strip(),
            }
            
            # Rendu du contenu
            html_content = self._render_template(template.html_content, email_data)
            text_content = self._render_template(template.text_content, email_data) if template.text_content else None
            
            # Création du log
            email_log = self._create_email_log(
                template=template,
                recipient_email=admin.email,
                recipient_name=email_data['admin_name'],
                subject=template.subject.format(product_name=product.name),
                email_data=email_data,
                user=admin
            )
            
            result = self._send_email(email_log, html_content, text_content)
            results.append(result)
        
        return any(results)
    
    def _render_template(self, template_content, context):
        """Rend un template avec le contexte donné"""
        try:
            from django.template import Template, Context
            template = Template(template_content)
            return template.render(Context(context))
        except Exception as e:
            logger.error(f"Erreur rendu template: {str(e)}")
            return template_content


# Instance globale du service (initialisation paresseuse)
_email_service_instance = None

def get_email_service():
    """Retourne l'instance du service email (initialisation paresseuse)"""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance

# Alias pour la compatibilité
email_service = get_email_service()
