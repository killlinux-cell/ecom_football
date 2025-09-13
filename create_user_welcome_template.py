#!/usr/bin/env python
"""
Script pour créer le template user_welcome manquant
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def create_user_welcome_template():
    """Crée le template user_welcome manquant"""
    print("📧 CRÉATION DU TEMPLATE USER_WELCOME")
    print("=" * 50)
    
    try:
        from notifications.models import EmailTemplate
        
        # Vérifier si le template existe déjà
        try:
            existing_template = EmailTemplate.objects.get(template_type='user_welcome')
            print("✅ Template user_welcome existe déjà")
            return True
        except EmailTemplate.DoesNotExist:
            pass
        
        # Créer le template user_welcome
        template_data = {
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
        }
        
        template = EmailTemplate.objects.create(**template_data)
        print(f"✅ Template user_welcome créé avec l'ID: {template.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("📧 CRÉATION DU TEMPLATE USER_WELCOME")
    print("=" * 50)
    
    success = create_user_welcome_template()
    
    if success:
        print(f"\n🎉 TEMPLATE CRÉÉ AVEC SUCCÈS!")
        print("=" * 50)
        print("✅ Template user_welcome disponible")
        print("✅ Email de bienvenue fonctionnel")
        print("\n📋 MAINTENANT:")
        print("1. Testez l'inscription d'un utilisateur")
        print("2. Vérifiez que l'email de bienvenue est envoyé")
    else:
        print(f"\n❌ ÉCHEC DE LA CRÉATION")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
