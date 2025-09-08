#!/usr/bin/env python
"""
Script de test pour tous les emails automatiques
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_all_emails():
    """Teste tous les emails automatiques"""
    print("🧪 TEST COMPLET DES EMAILS AUTOMATIQUES")
    print("=" * 50)
    
    try:
        from notifications.email_service import get_email_service
        from django.contrib.auth.models import User
        from orders.models import Order
        from payments.models import Payment
        from cart.models import CartItem
        from products.models import Product
        
        email_service = get_email_service()
        if not email_service:
            print("❌ Service email non initialisé")
            return False
        
        print("✅ Service email initialisé")
        
        # 1. Test email de bienvenue
        print("\n👤 Test email de bienvenue...")
        try:
            # Créer un utilisateur de test
            test_user, created = User.objects.get_or_create(
                email='test@example.com',
                defaults={
                    'username': 'testuser',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            
            if created:
                print("✅ Utilisateur de test créé")
            else:
                print("✅ Utilisateur de test existant")
            
            # Tester l'email de bienvenue
            result = email_service.send_user_welcome(test_user)
            if result:
                print("✅ Email de bienvenue envoyé avec succès")
            else:
                print("❌ Échec envoi email de bienvenue")
                
        except Exception as e:
            print(f"❌ Erreur test email bienvenue: {str(e)}")
        
        # 2. Test email de confirmation de commande
        print("\n📦 Test email de confirmation de commande...")
        try:
            # Récupérer une commande existante ou créer une de test
            order = Order.objects.first()
            if order:
                result = email_service.send_order_confirmation(order)
                if result:
                    print("✅ Email de confirmation de commande envoyé")
                else:
                    print("❌ Échec envoi email de confirmation")
            else:
                print("⚠️ Aucune commande trouvée pour le test")
                
        except Exception as e:
            print(f"❌ Erreur test email commande: {str(e)}")
        
        # 3. Test email de confirmation de paiement
        print("\n💳 Test email de confirmation de paiement...")
        try:
            payment = Payment.objects.first()
            if payment:
                result = email_service.send_payment_confirmation(payment)
                if result:
                    print("✅ Email de confirmation de paiement envoyé")
                else:
                    print("❌ Échec envoi email de paiement")
            else:
                print("⚠️ Aucun paiement trouvé pour le test")
                
        except Exception as e:
            print(f"❌ Erreur test email paiement: {str(e)}")
        
        # 4. Vérifier les logs d'emails
        print("\n📋 Vérification des logs d'emails...")
        try:
            from notifications.models import EmailLog
            
            recent_logs = EmailLog.objects.order_by('-created_at')[:5]
            if recent_logs:
                print(f"✅ {recent_logs.count()} emails récents trouvés:")
                for log in recent_logs:
                    status_icon = "✅" if log.status == 'sent' else "❌"
                    print(f"   {status_icon} {log.subject} → {log.recipient_email} ({log.status})")
            else:
                print("⚠️ Aucun log d'email trouvé")
                
        except Exception as e:
            print(f"❌ Erreur vérification logs: {str(e)}")
        
        # 5. Test de la configuration SMTP
        print("\n🔧 Test de la configuration SMTP...")
        try:
            import smtplib
            
            settings = email_service.settings
            if settings:
                server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
                server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.quit()
                print("✅ Connexion SMTP réussie")
            else:
                print("❌ Configuration SMTP non trouvée")
                
        except Exception as e:
            print(f"❌ Erreur test SMTP: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def show_email_status():
    """Affiche le statut des emails"""
    print("\n📊 STATUT DES EMAILS AUTOMATIQUES")
    print("=" * 50)
    
    try:
        from notifications.models import EmailSettings, EmailTemplate, EmailLog
        
        # Configuration
        settings = EmailSettings.objects.first()
        if settings:
            print(f"📧 Configuration: {settings.from_email}")
            print(f"   - Système actif: {'✅' if settings.is_active else '❌'}")
            print(f"   - Confirmation commandes: {'✅' if settings.send_order_confirmations else '❌'}")
            print(f"   - Confirmation paiements: {'✅' if settings.send_payment_confirmations else '❌'}")
            print(f"   - Notifications expédition: {'✅' if settings.send_shipping_notifications else '❌'}")
            print(f"   - Rappels panier: {'✅' if settings.send_cart_reminders else '❌'}")
        else:
            print("❌ Aucune configuration email")
        
        # Templates
        templates = EmailTemplate.objects.filter(is_active=True)
        print(f"\n📝 Templates actifs: {templates.count()}")
        for template in templates:
            print(f"   ✅ {template.name} ({template.template_type})")
        
        # Logs récents
        recent_logs = EmailLog.objects.order_by('-created_at')[:10]
        sent_count = recent_logs.filter(status='sent').count()
        failed_count = recent_logs.filter(status='failed').count()
        
        print(f"\n📊 Statistiques récentes:")
        print(f"   - Emails envoyés: {sent_count}")
        print(f"   - Emails échoués: {failed_count}")
        print(f"   - Total: {recent_logs.count()}")
        
    except Exception as e:
        print(f"❌ Erreur statut: {str(e)}")

def main():
    """Fonction principale"""
    print("🧪 TEST COMPLET DES EMAILS AUTOMATIQUES")
    print("=" * 50)
    print("Ce script teste tous les emails automatiques")
    print("=" * 50)
    
    # Afficher le statut
    show_email_status()
    
    # Tester tous les emails
    success = test_all_emails()
    
    if success:
        print(f"\n🎉 TESTS TERMINÉS!")
        print("=" * 50)
        print("✅ Tous les emails ont été testés")
        print("✅ Vérifiez les logs pour les détails")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Testez l'inscription d'un utilisateur")
        print("2. Testez une commande complète")
        print("3. Vérifiez les emails reçus")
        print("4. Consultez les logs dans /dashboard/emails/")
    else:
        print(f"\n❌ TESTS ÉCHOUÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
