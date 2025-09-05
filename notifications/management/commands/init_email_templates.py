"""
Commande Django pour initialiser les templates d'emails par défaut
"""

from django.core.management.base import BaseCommand
from notifications.models import EmailTemplate


class Command(BaseCommand):
    help = 'Initialise les templates d\'emails par défaut'

    def handle(self, *args, **options):
        self.stdout.write("📧 Initialisation des templates d'emails...")
        
        templates_data = [
            {
                'name': 'Confirmation de commande',
                'template_type': 'order_confirmation',
                'subject': 'Confirmation de votre commande #{order_number}',
                'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>🎉 Merci pour votre commande !</h2>

<p>Bonjour <strong>{{ customer_name }}</strong>,</p>

<p>Nous avons bien reçu votre commande <strong>#{{ order.order_number }}</strong> et nous vous en remercions !</p>

<div class="order-details">
    <h3>📋 Détails de votre commande</h3>
    
    {% for item in order_items %}
    <div class="order-item">
        <div class="product-info">
            <div class="product-name">{{ item.product_name }}</div>
            <div class="product-details">
                Taille: {{ item.size }} | Quantité: {{ item.quantity }}
            </div>
        </div>
        <div class="price">{{ item.total_price|floatformat:0 }} FCFA</div>
    </div>
    {% endfor %}
</div>

<div class="total-section">
    <div class="total-row">
        <span>Sous-total:</span>
        <span>{{ order.subtotal|floatformat:0 }} FCFA</span>
    </div>
    <div class="total-row">
        <span>Frais de livraison:</span>
        <span>{{ order.shipping_cost|floatformat:0 }} FCFA</span>
    </div>
    <div class="total-row final">
        <span>Total:</span>
        <span>{{ order.total|floatformat:0 }} FCFA</span>
    </div>
</div>

{% if shipping_address %}
<div class="order-details">
    <h3>📍 Adresse de livraison</h3>
    <p>
        <strong>{{ shipping_address.first_name }} {{ shipping_address.last_name }}</strong><br>
        {{ shipping_address.address }}<br>
        {{ shipping_address.city }}, {{ shipping_address.postal_code }}<br>
        {{ shipping_address.country }}<br>
        📞 {{ shipping_address.phone }}
    </p>
</div>
{% endif %}

<div style="text-align: center; margin: 30px 0;">
    <a href="{{ order.get_absolute_url }}" class="button">Voir ma commande</a>
</div>

<h3>💳 Prochaines étapes</h3>
<ol>
    <li><strong>Paiement</strong> : Vous recevrez un email de confirmation une fois le paiement validé</li>
    <li><strong>Préparation</strong> : Nous préparerons votre commande avec soin</li>
    <li><strong>Expédition</strong> : Vous serez notifié dès l'expédition</li>
    <li><strong>Livraison</strong> : Suivez votre colis jusqu'à la livraison</li>
</ol>

<p>Si vous avez des questions concernant votre commande, n'hésitez pas à nous contacter.</p>

<p>Merci encore pour votre confiance !</p>

<p><strong>L'équipe Maillots Football</strong></p>
{% endblock %}''',
                'text_content': '''Bonjour {{ customer_name }},

Merci pour votre commande #{{ order.order_number }} !

Détails de votre commande:
{% for item in order_items %}
- {{ item.product_name }} (Taille: {{ item.size }}, Quantité: {{ item.quantity }}) - {{ item.total_price|floatformat:0 }} FCFA
{% endfor %}

Sous-total: {{ order.subtotal|floatformat:0 }} FCFA
Frais de livraison: {{ order.shipping_cost|floatformat:0 }} FCFA
Total: {{ order.total|floatformat:0 }} FCFA

Prochaines étapes:
1. Paiement: Vous recevrez un email de confirmation une fois le paiement validé
2. Préparation: Nous préparerons votre commande avec soin
3. Expédition: Vous serez notifié dès l'expédition
4. Livraison: Suivez votre colis jusqu'à la livraison

Merci pour votre confiance !
L'équipe Maillots Football'''
            },
            {
                'name': 'Confirmation de paiement',
                'template_type': 'payment_confirmation',
                'subject': 'Paiement confirmé - Commande #{order_number}',
                'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>✅ Paiement confirmé !</h2>

<p>Bonjour <strong>{{ customer_name }}</strong>,</p>

<p>Excellente nouvelle ! Votre paiement pour la commande <strong>#{{ order.order_number }}</strong> a été confirmé avec succès.</p>

<div class="order-details">
    <h3>💳 Détails du paiement</h3>
    <div class="order-item">
        <div class="product-info">
            <div class="product-name">Montant payé</div>
            <div class="product-details">Méthode: {{ payment_method }}</div>
        </div>
        <div class="price">{{ payment_amount|floatformat:0 }} FCFA</div>
    </div>
</div>

<div style="text-align: center; margin: 30px 0;">
    <a href="{{ order.get_absolute_url }}" class="button">Suivre ma commande</a>
</div>

<h3>🚀 Prochaines étapes</h3>
<ol>
    <li><strong>Préparation</strong> : Nous préparons votre commande avec soin (1-2 jours ouvrables)</li>
    <li><strong>Expédition</strong> : Vous recevrez un email avec le numéro de suivi</li>
    <li><strong>Livraison</strong> : Livraison sous 3-5 jours ouvrables</li>
</ol>

<p>Merci pour votre confiance et votre achat !</p>

<p><strong>L'équipe Maillots Football</strong></p>
{% endblock %}''',
                'text_content': '''Bonjour {{ customer_name }},

Votre paiement pour la commande #{{ order.order_number }} a été confirmé !

Montant payé: {{ payment_amount|floatformat:0 }} FCFA
Méthode: {{ payment_method }}

Prochaines étapes:
1. Préparation: Nous préparons votre commande avec soin (1-2 jours ouvrables)
2. Expédition: Vous recevrez un email avec le numéro de suivi
3. Livraison: Livraison sous 3-5 jours ouvrables

Merci pour votre confiance !
L'équipe Maillots Football'''
            },
            {
                'name': 'Commande expédiée',
                'template_type': 'order_shipped',
                'subject': 'Votre commande #{order_number} est expédiée !',
                'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>📦 Votre commande est expédiée !</h2>

<p>Bonjour <strong>{{ customer_name }}</strong>,</p>

<p>Excellente nouvelle ! Votre commande <strong>#{{ order.order_number }}</strong> a été expédiée et est en route vers vous.</p>

<div class="order-details">
    <h3>📋 Détails de l'expédition</h3>
    <div class="order-item">
        <div class="product-info">
            <div class="product-name">Numéro de commande</div>
            <div class="product-details">Référence: {{ order.order_number }}</div>
        </div>
        <div class="price">#{{ order.order_number }}</div>
    </div>
</div>

<div style="text-align: center; margin: 30px 0;">
    <a href="{{ order.get_absolute_url }}" class="button">Suivre ma commande</a>
</div>

<h3>⏰ Délai de livraison</h3>
<div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
    <h4 style="margin: 0 0 10px 0; color: #856404;">📅 Livraison prévue</h4>
    <p style="margin: 0;"><strong>3-5 jours ouvrables</strong> après l'expédition</p>
</div>

<p>Merci pour votre patience et votre confiance !</p>

<p><strong>L'équipe Maillots Football</strong></p>
{% endblock %}''',
                'text_content': '''Bonjour {{ customer_name }},

Votre commande #{{ order.order_number }} a été expédiée !

Livraison prévue: 3-5 jours ouvrables après l'expédition

Merci pour votre patience !
L'équipe Maillots Football'''
            },
            {
                'name': 'Rappel de panier abandonné',
                'template_type': 'cart_reminder',
                'subject': 'Vous avez oublié quelque chose dans votre panier !',
                'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>🛒 Vous avez oublié quelque chose !</h2>

<p>Bonjour <strong>{{ customer_name }}</strong>,</p>

<p>Nous avons remarqué que vous avez laissé des articles dans votre panier. Ne les laissez pas vous échapper !</p>

<div class="order-details">
    <h3>🛍️ Articles dans votre panier</h3>
    
    {% for item in cart_items %}
    <div class="order-item">
        <div class="product-info">
            <div class="product-name">{{ item.product.name }}</div>
            <div class="product-details">
                Taille: {{ item.size }} | Quantité: {{ item.quantity }}
            </div>
        </div>
        <div class="price">{{ item.total_price|floatformat:0 }} FCFA</div>
    </div>
    {% endfor %}
</div>

<div style="text-align: center; margin: 30px 0;">
    <a href="{% url 'cart:cart_detail' %}" class="button">Finaliser ma commande</a>
</div>

<div style="background-color: #e8f5e8; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0;">
    <h4 style="margin: 0 0 10px 0; color: #28a745;">🎁 Offre spéciale !</h4>
    <p style="margin: 0;">Finalisez votre commande dans les 24h et bénéficiez de la livraison gratuite !</p>
</div>

<p>Ne laissez pas ces magnifiques maillots vous échapper !</p>

<p><strong>L'équipe Maillots Football</strong></p>
{% endblock %}''',
                'text_content': '''Bonjour {{ customer_name }},

Vous avez laissé des articles dans votre panier !

Articles:
{% for item in cart_items %}
- {{ item.product.name }} (Taille: {{ item.size }}, Quantité: {{ item.quantity }}) - {{ item.total_price|floatformat:0 }} FCFA
{% endfor %}

Finalisez votre commande maintenant et bénéficiez de la livraison gratuite !

L'équipe Maillots Football'''
            },
            {
                'name': 'Alerte stock faible',
                'template_type': 'stock_alert',
                'subject': 'Alerte: Stock faible pour {{ product_name }}',
                'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>⚠️ Alerte Stock Faible</h2>

<p>Bonjour <strong>{{ admin_name }}</strong>,</p>

<p>Le stock du produit <strong>{{ product.name }}</strong> est faible et nécessite votre attention.</p>

<div class="order-details">
    <h3>📦 Détails du produit</h3>
    <div class="order-item">
        <div class="product-info">
            <div class="product-name">{{ product.name }}</div>
            <div class="product-details">Stock actuel: {{ current_stock }} unités</div>
        </div>
        <div class="price" style="color: #dc3545;">{{ current_stock }} restants</div>
    </div>
</div>

<div style="background-color: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; margin: 20px 0;">
    <h4 style="margin: 0 0 10px 0; color: #721c24;">🚨 Action requise</h4>
    <p style="margin: 0;">Veuillez réapprovisionner ce produit rapidement pour éviter les ruptures de stock.</p>
</div>

<div style="text-align: center; margin: 30px 0;">
    <a href="/dashboard/products/{{ product.id }}/" class="button">Gérer le produit</a>
</div>

<p><strong>Équipe Maillots Football</strong></p>
{% endblock %}''',
                'text_content': '''Alerte Stock Faible

Le stock du produit "{{ product.name }}" est faible.

Stock actuel: {{ current_stock }} unités

Action requise: Veuillez réapprovisionner ce produit rapidement.

Équipe Maillots Football'''
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for template_data in templates_data:
            template, created = EmailTemplate.objects.get_or_create(
                template_type=template_data['template_type'],
                defaults=template_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"✅ Template créé: {template.name}")
            else:
                # Mettre à jour le template existant
                template.name = template_data['name']
                template.subject = template_data['subject']
                template.html_content = template_data['html_content']
                template.text_content = template_data['text_content']
                template.is_active = True
                template.save()
                updated_count += 1
                self.stdout.write(f"🔄 Template mis à jour: {template.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f"🎉 {created_count} template(s) créé(s), {updated_count} mis à jour(s)")
        )
