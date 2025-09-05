#!/usr/bin/env python
"""
Test du système de notifications email
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

from notifications.models import EmailTemplate, EmailLog, EmailSettings
from notifications.email_service import email_service
from orders.models import Order
from payments.models import Payment
from django.contrib.auth.models import User
from decimal import Decimal

def test_email_system():
    """Test complet du système d'emails"""
    print("🧪 Test du système de notifications email...")
    
    # 1. Vérifier les templates
    print("\n1. Vérification des templates...")
    templates = EmailTemplate.objects.all()
    print(f"📧 {templates.count()} template(s) trouvé(s)")
    
    for template in templates:
        print(f"   - {template.name} ({template.template_type}) - {'✅ Actif' if template.is_active else '❌ Inactif'}")
    
    # 2. Vérifier la configuration
    print("\n2. Vérification de la configuration...")
    settings = EmailSettings.objects.first()
    if settings:
        print(f"📧 Configuration trouvée: {settings.from_email}")
        print(f"   - SMTP: {settings.smtp_host}:{settings.smtp_port}")
        print(f"   - Actif: {'✅' if settings.is_active else '❌'}")
        print(f"   - Confirmations commande: {'✅' if settings.send_order_confirmations else '❌'}")
        print(f"   - Confirmations paiement: {'✅' if settings.send_payment_confirmations else '❌'}")
    else:
        print("❌ Aucune configuration email trouvée")
        return False
    
    # 3. Vérifier les logs d'emails
    print("\n3. Vérification des logs d'emails...")
    total_logs = EmailLog.objects.count()
    sent_logs = EmailLog.objects.filter(status='sent').count()
    failed_logs = EmailLog.objects.filter(status='failed').count()
    pending_logs = EmailLog.objects.filter(status='pending').count()
    
    print(f"📊 Total logs: {total_logs}")
    print(f"   - Envoyés: {sent_logs}")
    print(f"   - Échoués: {failed_logs}")
    print(f"   - En attente: {pending_logs}")
    
    # 4. Test d'envoi d'email (simulation)
    print("\n4. Test d'envoi d'email...")
    
    # Créer des données de test
    test_data = {
        'customer_name': 'Test User',
        'order_number': 'TEST123',
        'order_total': 25000,
        'payment_amount': 25000,
        'payment_method': 'Wave',
    }
    
    # Tester le rendu d'un template
    template = EmailTemplate.objects.filter(template_type='order_confirmation').first()
    if template:
        try:
            from django.template import Template, Context
            html_content = Template(template.html_content).render(Context(test_data))
            print(f"✅ Rendu template OK: {len(html_content)} caractères")
        except Exception as e:
            print(f"❌ Erreur rendu template: {str(e)}")
            return False
    else:
        print("❌ Template de confirmation de commande non trouvé")
        return False
    
    # 5. Vérifier les signaux
    print("\n5. Vérification des signaux...")
    
    # Vérifier qu'il y a des commandes pour tester
    orders_count = Order.objects.count()
    payments_count = Payment.objects.count()
    
    print(f"📦 Commandes disponibles: {orders_count}")
    print(f"💳 Paiements disponibles: {payments_count}")
    
    if orders_count > 0:
        print("✅ Des commandes sont disponibles pour tester les signaux")
    else:
        print("⚠️ Aucune commande disponible pour tester les signaux")
    
    # 6. Test de la commande de rappel de panier
    print("\n6. Test de la commande de rappel de panier...")
    try:
        from django.core.management import call_command
        call_command('send_cart_reminders', '--dry-run')
        print("✅ Commande de rappel de panier fonctionne")
    except Exception as e:
        print(f"❌ Erreur commande rappel panier: {str(e)}")
    
    # 7. Statistiques finales
    print("\n7. Statistiques finales...")
    print(f"📧 Templates actifs: {EmailTemplate.objects.filter(is_active=True).count()}")
    print(f"📊 Logs d'emails: {EmailLog.objects.count()}")
    print(f"⚙️ Configuration: {'✅' if EmailSettings.objects.exists() else '❌'}")
    
    print("\n🎉 Test du système d'emails terminé!")
    return True

def create_test_email_settings():
    """Crée une configuration email de test"""
    print("🔧 Création de la configuration email de test...")
    
    settings, created = EmailSettings.objects.get_or_create(
        defaults={
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_username': 'test@example.com',
            'smtp_password': 'test_password',
            'use_tls': True,
            'from_email': 'noreply@maillots-football.ci',
            'from_name': 'Maillots Football',
            'is_active': False,  # Désactivé par défaut pour les tests
            'send_order_confirmations': True,
            'send_payment_confirmations': True,
            'send_shipping_notifications': True,
            'send_cart_reminders': True,
            'send_stock_alerts': True,
            'max_emails_per_hour': 100,
            'cart_reminder_delay_hours': 24,
        }
    )
    
    if created:
        print("✅ Configuration email de test créée")
    else:
        print("✅ Configuration email de test existe déjà")
    
    return settings

if __name__ == "__main__":
    # Créer la configuration de test
    create_test_email_settings()
    
    # Tester le système
    success = test_email_system()
    
    if success:
        print("\n✅ Système d'emails prêt à l'utilisation!")
        print("\n📋 Prochaines étapes:")
        print("1. Configurer les paramètres SMTP dans le dashboard")
        print("2. Initialiser les templates: python manage.py init_email_templates")
        print("3. Tester l'envoi d'emails")
        print("4. Configurer les tâches cron pour les rappels automatiques")
    else:
        print("\n❌ Des problèmes ont été détectés dans le système d'emails")
    
    sys.exit(0 if success else 1)
