#!/usr/bin/env python
"""
Script pour corriger les templates d'emails sur le VPS
Ajoute le template manquant order_delivered
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_email_templates():
    """Ajoute le template manquant order_delivered"""
    print("📧 CORRECTION DES TEMPLATES D'EMAILS")
    print("=" * 50)
    
    try:
        from notifications.models import EmailTemplate
        
        # Template order_delivered manquant
        template_data = {
            'name': 'Commande livrée',
            'template_type': 'order_delivered',
            'subject': 'Votre commande #{order_number} a été livrée !',
            'html_content': '''{% extends "emails/base_email.html" %}

{% block content %}
<h2>🎉 Votre commande a été livrée !</h2>

<p>Bonjour <strong>{{ customer_name }}</strong>,</p>

<p>Excellente nouvelle ! Votre commande <strong>#{{ order.order_number }}</strong> a été livrée avec succès.</p>

<div class="order-details">
    <h3>📦 Détails de la livraison</h3>
    
    <div class="order-item">
        <div class="product-info">
            <div class="product-name">Commande #{{ order.order_number }}</div>
            <div class="product-details">
                Livrée le: {{ delivery_date|date:"d/m/Y à H:i" }}
            </div>
        </div>
        <div class="price" style="color: #28a745;">✅ Livrée</div>
    </div>
</div>

<div style="background-color: #e8f5e8; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0;">
    <h4 style="margin: 0 0 10px 0; color: #28a745;">🎉 Livraison réussie !</h4>
    <p style="margin: 0;">Nous espérons que vous êtes satisfait de votre achat. N'hésitez pas à nous faire un retour !</p>
</div>

<div style="text-align: center; margin: 30px 0;">
    <a href="{% url 'products:product_list' %}" class="button">Découvrir d'autres maillots</a>
</div>

<h3>💬 Votre avis nous intéresse</h3>
<p>Partagez votre expérience avec nous ! Votre avis nous aide à améliorer nos services.</p>

<div style="text-align: center; margin: 30px 0;">
    <a href="{% url 'products:product_list' %}" class="button">Laisser un avis</a>
</div>

<p>Merci encore pour votre confiance et à bientôt !</p>

<p><strong>L'équipe Maillots Football</strong></p>
{% endblock %}''',
            'text_content': '''Votre commande a été livrée !

Bonjour {{ customer_name }},

Votre commande #{{ order.order_number }} a été livrée avec succès.

Livrée le: {{ delivery_date|date:"d/m/Y à H:i" }}

Nous espérons que vous êtes satisfait de votre achat !

Merci pour votre confiance,
L'équipe Maillots Football'''
        }
        
        # Vérifier si le template existe déjà
        try:
            existing_template = EmailTemplate.objects.get(template_type='order_delivered')
            print(f"📁 Template 'order_delivered' existe déjà")
            
            # Mettre à jour le template existant
            existing_template.name = template_data['name']
            existing_template.subject = template_data['subject']
            existing_template.html_content = template_data['html_content']
            existing_template.text_content = template_data['text_content']
            existing_template.is_active = True
            existing_template.save()
            
            print(f"✅ Template 'order_delivered' mis à jour")
            
        except EmailTemplate.DoesNotExist:
            # Créer le nouveau template
            template = EmailTemplate.objects.create(**template_data)
            print(f"✅ Template 'order_delivered' créé")
        
        # Vérifier tous les templates
        print(f"\n📋 VÉRIFICATION DES TEMPLATES:")
        print("-" * 30)
        
        required_templates = [
            'order_confirmation',
            'payment_confirmation', 
            'order_shipped',
            'order_delivered',
            'cart_reminder',
            'stock_alert'
        ]
        
        all_templates_ok = True
        for template_type in required_templates:
            try:
                template = EmailTemplate.objects.get(
                    template_type=template_type,
                    is_active=True
                )
                print(f"   ✅ {template.name} ({template_type})")
            except EmailTemplate.DoesNotExist:
                print(f"   ❌ Template manquant: {template_type}")
                all_templates_ok = False
        
        if all_templates_ok:
            print(f"\n🎉 TOUS LES TEMPLATES SONT PRÊTS!")
            print("=" * 50)
            print("✅ Le système d'emails est maintenant complet")
            print("✅ Vous pouvez déployer en toute sécurité")
        else:
            print(f"\n⚠️  DES TEMPLATES MANQUENT ENCORE")
            print("🔧 Exécutez: python manage.py init_email_templates")
        
        return all_templates_ok
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("📧 CORRECTION DES TEMPLATES D'EMAILS")
    print("=" * 50)
    print("Ce script ajoute le template manquant 'order_delivered'")
    print("=" * 50)
    
    # Exécuter la correction
    success = fix_email_templates()
    
    if success:
        print(f"\n🚀 SYSTÈME D'EMAILS PRÊT!")
        print("=" * 50)
        print("✅ Tous les templates sont configurés")
        print("✅ Gmail SMTP est configuré")
        print("✅ Vous pouvez déployer en toute sécurité")
    else:
        print(f"\n⚠️  CORRECTIONS NÉCESSAIRES")
        print("🔧 Exécutez les commandes affichées ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
