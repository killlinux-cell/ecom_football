#!/usr/bin/env python
"""
Script de configuration automatique Gmail SMTP
Configure les paramètres SMTP pour Gmail
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def configure_gmail_smtp():
    """Configure automatiquement Gmail SMTP"""
    print("📧 CONFIGURATION GMAIL SMTP")
    print("=" * 50)
    
    try:
        from notifications.models import EmailSettings
        
        # Demander les informations à l'utilisateur
        print("Configuration Gmail SMTP")
        print("-" * 30)
        
        email = input("Votre email Gmail (ex: anakoisrael352@gmail.com): ").strip()
        if not email:
            print("❌ Email requis")
            return False
        
        print("\n⚠️  IMPORTANT: Vous devez utiliser un MOT DE PASSE D'APPLICATION")
        print("Pas votre mot de passe Gmail normal !")
        print("1. Allez sur myaccount.google.com")
        print("2. Sécurité → Mots de passe des applications")
        print("3. Créez un mot de passe pour 'Django Email'")
        print("4. Copiez le mot de passe de 16 caractères")
        print()
        
        password = input("Mot de passe d'application Gmail (16 caractères): ").strip()
        if not password:
            print("❌ Mot de passe d'application requis")
            return False
        
        from_name = input("Nom de l'expéditeur (ex: Maillots Football): ").strip()
        if not from_name:
            from_name = "Maillots Football"
        
        # Créer ou mettre à jour la configuration
        settings_obj, created = EmailSettings.objects.get_or_create(
            defaults={
                'from_email': email,
                'from_name': from_name,
                'smtp_host': 'smtp.gmail.com',
                'smtp_port': 587,
                'use_tls': True,
                'is_active': True,
                'send_order_confirmations': True,
                'send_payment_confirmations': True,
                'send_shipping_notifications': True,
                'send_cart_reminders': True,
                'send_stock_alerts': True,
                'max_emails_per_hour': 100,
                'cart_reminder_delay_hours': 24
            }
        )
        
        # Mettre à jour avec les nouvelles valeurs
        settings_obj.smtp_host = 'smtp.gmail.com'
        settings_obj.smtp_port = 587
        settings_obj.smtp_username = email
        settings_obj.smtp_password = password
        settings_obj.use_tls = True
        settings_obj.from_email = email
        settings_obj.from_name = from_name
        settings_obj.is_active = True
        settings_obj.save()
        
        if created:
            print(f"✅ Configuration Gmail créée")
        else:
            print(f"✅ Configuration Gmail mise à jour")
        
        print(f"\n📧 Configuration SMTP:")
        print(f"   Serveur: {settings_obj.smtp_host}")
        print(f"   Port: {settings_obj.smtp_port}")
        print(f"   Email: {settings_obj.smtp_username}")
        print(f"   TLS: {'Activé' if settings_obj.use_tls else 'Désactivé'}")
        print(f"   Expéditeur: {settings_obj.from_name} <{settings_obj.from_email}>")
        
        # Tester la configuration
        print(f"\n🧪 Test de la configuration...")
        try:
            from notifications.email_service import get_email_service
            email_service = get_email_service()
            
            # Test simple de connexion SMTP
            import smtplib
            from email.mime.text import MIMEText
            
            server = smtplib.SMTP(settings_obj.smtp_host, settings_obj.smtp_port)
            server.starttls()
            server.login(settings_obj.smtp_username, settings_obj.smtp_password)
            server.quit()
            
            print("✅ Connexion SMTP réussie !")
            print("✅ Configuration Gmail validée")
            
        except Exception as e:
            print(f"❌ Erreur de test SMTP: {str(e)}")
            print("⚠️  Vérifiez votre mot de passe d'application")
            return False
        
        print(f"\n🎉 CONFIGURATION TERMINÉE!")
        print("=" * 50)
        print("✅ Gmail SMTP configuré avec succès")
        print("✅ Vous pouvez maintenant envoyer des emails")
        print("✅ Allez sur /dashboard/emails/ pour gérer les emails")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("📧 CONFIGURATION GMAIL SMTP")
    print("=" * 50)
    print("Ce script va configurer Gmail SMTP pour votre application")
    print("Vous aurez besoin de:")
    print("• Votre email Gmail")
    print("• Un mot de passe d'application Gmail (pas votre mot de passe normal)")
    print("=" * 50)
    
    # Demander confirmation
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Configuration annulée")
        return False
    
    # Exécuter la configuration
    success = configure_gmail_smtp()
    
    if not success:
        print(f"\n❌ ERREUR LORS DE LA CONFIGURATION")
        print("⚠️  Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
