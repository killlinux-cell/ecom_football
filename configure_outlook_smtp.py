#!/usr/bin/env python
"""
Script pour configurer Outlook SMTP pour l'application
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def configure_outlook_smtp():
    """Configure Outlook SMTP dans EmailSettings"""
    print("📧 CONFIGURATION OUTLOOK SMTP")
    print("=" * 50)
    print("Ce script va configurer Outlook SMTP pour votre application")
    print("Vous aurez besoin de:")
    print("• Votre email Outlook/Hotmail")
    print("• Votre mot de passe Outlook")
    print("=" * 50)
    
    # Demander les informations
    print("\n📧 Configuration Outlook SMTP")
    print("-" * 30)
    
    email = input("Votre email Outlook (ex: anakoisrael352@outlook.com): ").strip()
    if not email:
        print("❌ Email requis")
        return False
    
    print("\n⚠️  IMPORTANT: Utilisez votre mot de passe Outlook normal")
    print("Outlook ne nécessite pas de mot de passe d'application")
    print("Assurez-vous que l'authentification à 2 facteurs est activée")
    
    password = input("Mot de passe Outlook: ").strip()
    if not password:
        print("❌ Mot de passe requis")
        return False
    
    sender_name = input("Nom de l'expéditeur (ex: Maillots Football): ").strip()
    if not sender_name:
        sender_name = "Maillots Football"
    
    try:
        from notifications.models import EmailSettings
        
        # Configuration Outlook SMTP
        outlook_config = {
            'smtp_host': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'smtp_use_tls': True,
            'smtp_username': email,
            'smtp_password': password,
            'sender_email': email,
            'sender_name': sender_name,
            'is_active': True
        }
        
        # Mettre à jour ou créer la configuration
        email_settings, created = EmailSettings.objects.get_or_create(
            defaults=outlook_config
        )
        
        if not created:
            # Mettre à jour la configuration existante
            for key, value in outlook_config.items():
                setattr(email_settings, key, value)
            email_settings.save()
        
        print(f"\n✅ Configuration Outlook mise à jour")
        
        # Afficher la configuration
        print(f"\n📧 Configuration SMTP:")
        print(f"   Serveur: {email_settings.smtp_host}:{email_settings.smtp_port}")
        print(f"   Email: {email_settings.sender_email}")
        print(f"   TLS: {'Activé' if email_settings.smtp_use_tls else 'Désactivé'}")
        print(f"   Expéditeur: {email_settings.sender_name} <{email_settings.sender_email}>")
        
        # Test de la configuration
        print(f"\n🧪 Test de la configuration...")
        
        try:
            from notifications.email_service import get_email_service
            email_service = get_email_service()
            
            # Test de connexion SMTP
            import smtplib
            from email.mime.text import MIMEText
            
            server = smtplib.SMTP(email_settings.smtp_host, email_settings.smtp_port)
            server.starttls()
            server.login(email_settings.smtp_username, email_settings.smtp_password)
            server.quit()
            
            print("✅ Connexion SMTP réussie !")
            print("✅ Configuration Outlook validée")
            
        except Exception as e:
            print(f"❌ Erreur de test SMTP: {str(e)}")
            print("⚠️  Vérifiez vos identifiants Outlook")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def update_django_settings():
    """Met à jour les settings Django pour Outlook"""
    print(f"\n🔧 Mise à jour des settings Django...")
    
    # Paramètres Outlook pour les settings
    outlook_settings = {
        'EMAIL_HOST': 'smtp-mail.outlook.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True,
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend'
    }
    
    print("📝 Paramètres à ajouter dans vos variables d'environnement:")
    print("-" * 50)
    for key, value in outlook_settings.items():
        print(f"{key}={value}")
    
    print(f"\n📝 Ou dans votre fichier .env:")
    print("-" * 30)
    for key, value in outlook_settings.items():
        print(f"{key}={value}")
    
    print(f"\n⚠️  IMPORTANT:")
    print("• Ajoutez EMAIL_HOST_USER=votre_email@outlook.com")
    print("• Ajoutez EMAIL_HOST_PASSWORD=votre_mot_de_passe")
    print("• Redémarrez votre serveur après modification")

def main():
    """Fonction principale"""
    print("📧 CONFIGURATION OUTLOOK SMTP")
    print("=" * 50)
    print("Ce script configure Outlook SMTP pour votre application")
    print("=" * 50)
    
    # Demander confirmation
    continue_setup = input("\nVoulez-vous continuer ? (o/n): ").strip().lower()
    if continue_setup != 'o':
        print("❌ Configuration annulée")
        return False
    
    # Configurer Outlook SMTP
    success = configure_outlook_smtp()
    
    if success:
        # Mettre à jour les settings Django
        update_django_settings()
        
        print(f"\n🎉 CONFIGURATION TERMINÉE!")
        print("=" * 50)
        print("✅ Outlook SMTP configuré avec succès")
        print("✅ Vous pouvez maintenant envoyer des emails")
        print("✅ Allez sur /dashboard/emails/ pour gérer les emails")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Mettez à jour vos variables d'environnement")
        print("2. Redémarrez votre serveur")
        print("3. Testez l'envoi d'emails")
    else:
        print(f"\n❌ CONFIGURATION ÉCHOUÉE")
        print("🔧 Vérifiez vos identifiants Outlook")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
