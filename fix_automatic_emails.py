#!/usr/bin/env python
"""
Script pour corriger les emails automatiques
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_automatic_emails():
    """Corrige les emails automatiques"""
    print("🔧 CORRECTION EMAILS AUTOMATIQUES")
    print("=" * 50)
    
    try:
        from notifications.models import EmailTemplate, EmailSettings, EmailLog
        from notifications.email_service import get_email_service
        from django.contrib.auth.models import User
        
        # 1. Vérifier si les templates existent
        print("\n📧 Vérification des templates d'emails...")
        
        required_templates = [
            'order_confirmation',
            'payment_confirmation', 
            'shipping_notification',
            'user_welcome',
            'cart_reminder'
        ]
        
        missing_templates = []
        for template_type in required_templates:
            try:
                template = EmailTemplate.objects.get(template_type=template_type)
                print(f"✅ Template {template_type} trouvé")
            except EmailTemplate.DoesNotExist:
                missing_templates.append(template_type)
                print(f"❌ Template {template_type} manquant")
        
        # 2. Initialiser les templates manquants
        if missing_templates:
            print(f"\n🔧 Initialisation des templates manquants...")
            init_missing_templates(missing_templates)
        
        # 3. Vérifier la configuration email
        print(f"\n⚙️ Vérification de la configuration email...")
        try:
            email_settings = EmailSettings.objects.first()
            if email_settings:
                print(f"✅ Configuration email trouvée: {email_settings.from_email}")
                print(f"   - Confirmation commandes: {'✅' if email_settings.send_order_confirmations else '❌'}")
                print(f"   - Confirmation paiements: {'✅' if email_settings.send_payment_confirmations else '❌'}")
                print(f"   - Notifications expédition: {'✅' if email_settings.send_shipping_notifications else '❌'}")
                print(f"   - Rappels panier: {'✅' if email_settings.send_cart_reminders else '❌'}")
            else:
                print("❌ Aucune configuration email trouvée")
                create_default_email_settings()
        except Exception as e:
            print(f"❌ Erreur configuration email: {str(e)}")
        
        # 4. Ajouter l'email d'inscription manquant
        print(f"\n👤 Ajout de l'email d'inscription...")
        add_user_welcome_signal()
        
        # 5. Tester les signaux
        print(f"\n🧪 Test des signaux...")
        test_email_signals()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def init_missing_templates(missing_templates):
    """Initialise les templates manquants"""
    from notifications.models import EmailTemplate
    
    templates_data = {
        'user_welcome': {
            'name': 'Email de bienvenue',
            'template_type': 'user_welcome',
            'subject': 'Bienvenue sur Maillots Football !',
            'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>🎉 Bienvenue sur Maillots Football !</h2>

<p>Bonjour <strong>{{ user.first_name }} {{ user.last_name }}</strong>,</p>

<p>Merci de vous être inscrit sur notre site ! Nous sommes ravis de vous accueillir.</p>

<div class="welcome-section">
    <h3>🏆 Découvrez nos maillots</h3>
    <p>Explorez notre collection de maillots de football des plus grandes équipes et sélections du monde.</p>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="/" class="button">Découvrir nos maillots</a>
    </div>
</div>

<div class="benefits-section">
    <h3>✨ Vos avantages</h3>
    <ul>
        <li>🚚 <strong>Livraison gratuite</strong> à partir de 50 000 FCFA</li>
        <li>💳 <strong>Paiement sécurisé</strong> par Wave, PayDunya ou à la livraison</li>
        <li>🎨 <strong>Personnalisation</strong> de vos maillots</li>
        <li>📱 <strong>Suivi de commande</strong> en temps réel</li>
    </ul>
</div>

<p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>

<p>Bonne visite !</p>

<p><strong>L'équipe Maillots Football</strong></p>
{% endblock %}''',
            'text_content': '''Bienvenue sur Maillots Football !

Bonjour {{ user.first_name }} {{ user.last_name }},

Merci de vous être inscrit sur notre site ! Nous sommes ravis de vous accueillir.

Découvrez nos maillots de football des plus grandes équipes et sélections du monde.

Vos avantages :
- Livraison gratuite à partir de 50 000 FCFA
- Paiement sécurisé par Wave, PayDunya ou à la livraison
- Personnalisation de vos maillots
- Suivi de commande en temps réel

Si vous avez des questions, n'hésitez pas à nous contacter.

Bonne visite !

L'équipe Maillots Football''',
            'is_active': True
        },
        'cart_reminder': {
            'name': 'Rappel de panier abandonné',
            'template_type': 'cart_reminder',
            'subject': 'Votre panier vous attend !',
            'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>🛒 Votre panier vous attend !</h2>

<p>Bonjour <strong>{{ user.first_name }} {{ user.last_name }}</strong>,</p>

<p>Nous avons remarqué que vous avez laissé des articles dans votre panier. Ne les laissez pas vous échapper !</p>

<div class="cart-items">
    <h3>📦 Articles dans votre panier</h3>
    
    {% for item in cart_items %}
    <div class="cart-item">
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

<div class="total-section">
    <div class="total-row final">
        <span>Total:</span>
        <span>{{ cart_total|floatformat:0 }} FCFA</span>
    </div>
</div>

<div style="text-align: center; margin: 30px 0;">
    <a href="/cart/" class="button">Finaliser ma commande</a>
</div>

<div class="urgency-section">
    <h3>⏰ Offre limitée !</h3>
    <p>Profitez de la <strong>livraison gratuite</strong> à partir de 50 000 FCFA !</p>
</div>

<p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>

<p><strong>L'équipe Maillots Football</strong></p>
{% endblock %}''',
            'text_content': '''Votre panier vous attend !

Bonjour {{ user.first_name }} {{ user.last_name }},

Nous avons remarqué que vous avez laissé des articles dans votre panier. Ne les laissez pas vous échapper !

Articles dans votre panier :
{% for item in cart_items %}
- {{ item.product.name }} (Taille: {{ item.size }}, Quantité: {{ item.quantity }}) - {{ item.total_price|floatformat:0 }} FCFA
{% endfor %}

Total: {{ cart_total|floatformat:0 }} FCFA

Finalisez votre commande : /cart/

Offre limitée : Profitez de la livraison gratuite à partir de 50 000 FCFA !

Si vous avez des questions, n'hésitez pas à nous contacter.

L'équipe Maillots Football''',
            'is_active': True
        }
    }
    
    for template_type in missing_templates:
        if template_type in templates_data:
            template_data = templates_data[template_type]
            template, created = EmailTemplate.objects.get_or_create(
                template_type=template_type,
                defaults=template_data
            )
            if created:
                print(f"✅ Template {template_type} créé")
            else:
                print(f"✅ Template {template_type} déjà existant")

def create_default_email_settings():
    """Crée la configuration email par défaut"""
    from notifications.models import EmailSettings
    
    settings, created = EmailSettings.objects.get_or_create(
        defaults={
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_username': 'anakoisrael352@gmail.com',
            'smtp_password': 'ticq fwgi xjnc epif',
            'smtp_use_tls': True,
            'sender_email': 'anakoisrael352@gmail.com',
            'sender_name': 'Maillots Football',
            'is_active': True,
            'send_order_confirmations': True,
            'send_payment_confirmations': True,
            'send_shipping_notifications': True,
            'send_cart_reminders': True,
            'send_stock_alerts': True,
        }
    )
    
    if created:
        print("✅ Configuration email par défaut créée")
    else:
        print("✅ Configuration email déjà existante")

def add_user_welcome_signal():
    """Ajoute le signal d'email de bienvenue"""
    print("👤 Ajout du signal d'email de bienvenue...")
    
    # Le signal sera ajouté dans accounts/signals.py
    signal_code = '''
@receiver(user_signed_up)
def send_welcome_email(sender, request, user, **kwargs):
    """Envoie un email de bienvenue lors de l'inscription"""
    try:
        from notifications.email_service import get_email_service
        get_email_service().send_user_welcome(user)
    except Exception as e:
        print(f"Erreur envoi email bienvenue: {str(e)}")
'''
    
    # Lire le fichier signals.py
    signals_file = 'accounts/signals.py'
    try:
        with open(signals_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si le signal existe déjà
        if 'send_welcome_email' not in content:
            # Ajouter le signal
            content += signal_code
            
            with open(signals_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Signal d'email de bienvenue ajouté")
        else:
            print("✅ Signal d'email de bienvenue déjà présent")
            
    except Exception as e:
        print(f"❌ Erreur ajout signal: {str(e)}")

def test_email_signals():
    """Teste les signaux d'emails"""
    print("🧪 Test des signaux d'emails...")
    
    try:
        from notifications.email_service import get_email_service
        from django.contrib.auth.models import User
        
        # Test du service email
        email_service = get_email_service()
        if email_service:
            print("✅ Service email initialisé")
        else:
            print("❌ Service email non initialisé")
        
        # Test des templates
        templates_to_test = ['order_confirmation', 'payment_confirmation', 'user_welcome']
        for template_type in templates_to_test:
            try:
                template = email_service._get_template(template_type)
                if template:
                    print(f"✅ Template {template_type} accessible")
                else:
                    print(f"❌ Template {template_type} non accessible")
            except Exception as e:
                print(f"❌ Erreur template {template_type}: {str(e)}")
        
    except Exception as e:
        print(f"❌ Erreur test signaux: {str(e)}")

def main():
    """Fonction principale"""
    print("🔧 CORRECTION EMAILS AUTOMATIQUES")
    print("=" * 50)
    print("Ce script corrige les emails automatiques manquants")
    print("=" * 50)
    
    # Corriger les emails automatiques
    success = fix_automatic_emails()
    
    if success:
        print(f"\n🎉 CORRECTION TERMINÉE!")
        print("=" * 50)
        print("✅ Templates d'emails initialisés")
        print("✅ Configuration email vérifiée")
        print("✅ Signal d'inscription ajouté")
        print("✅ Signaux testés")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Redémarrez votre serveur")
        print("2. Testez l'inscription d'un utilisateur")
        print("3. Testez une commande")
        print("4. Vérifiez les logs d'emails")
    else:
        print(f"\n❌ CORRECTION ÉCHOUÉE")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
