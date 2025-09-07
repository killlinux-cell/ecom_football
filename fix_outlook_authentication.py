#!/usr/bin/env python
"""
Script pour corriger l'authentification Outlook
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_outlook_authentication():
    """Corrige l'authentification Outlook"""
    print("🔧 CORRECTION AUTHENTIFICATION OUTLOOK")
    print("=" * 50)
    print("Outlook a désactivé l'authentification de base")
    print("Nous allons configurer un mot de passe d'application")
    print("=" * 50)
    
    # Demander les informations
    print("\n📧 Configuration Outlook avec mot de passe d'application")
    print("-" * 50)
    
    email = input("Votre email Outlook (ex: anakoisrael352@outlook.com): ").strip()
    if not email:
        print("❌ Email requis")
        return False
    
    print("\n⚠️  IMPORTANT: Vous devez créer un mot de passe d'application")
    print("1. Allez sur https://account.microsoft.com/security")
    print("2. Connectez-vous avec votre compte Outlook")
    print("3. Allez dans 'Sécurité' → 'Mots de passe d'application'")
    print("4. Créez un nouveau mot de passe d'application")
    print("5. Copiez le mot de passe généré (16 caractères)")
    
    app_password = input("\nMot de passe d'application Outlook (16 caractères): ").strip()
    if not app_password or len(app_password) != 16:
        print("❌ Mot de passe d'application requis (16 caractères)")
        return False
    
    sender_name = input("Nom de l'expéditeur (ex: Maillots Football): ").strip()
    if not sender_name:
        sender_name = "Maillots Football"
    
    try:
        from notifications.models import EmailSettings
        
        # Configuration Outlook SMTP avec mot de passe d'application
        outlook_config = {
            'smtp_host': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'smtp_use_tls': True,
            'smtp_username': email,
            'smtp_password': app_password,
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
        
        print(f"\n✅ Configuration Outlook mise à jour avec mot de passe d'application")
        
        # Afficher la configuration
        print(f"\n📧 Configuration SMTP:")
        print(f"   Serveur: {email_settings.smtp_host}:{email_settings.smtp_port}")
        print(f"   Email: {email_settings.sender_email}")
        print(f"   TLS: {'Activé' if email_settings.smtp_use_tls else 'Désactivé'}")
        print(f"   Expéditeur: {email_settings.sender_name} <{email_settings.sender_email}>")
        
        # Test de la configuration
        print(f"\n🧪 Test de la configuration...")
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            server = smtplib.SMTP(email_settings.smtp_host, email_settings.smtp_port)
            server.starttls()
            server.login(email_settings.smtp_username, email_settings.smtp_password)
            server.quit()
            
            print("✅ Connexion SMTP réussie avec mot de passe d'application !")
            print("✅ Configuration Outlook validée")
            
        except Exception as e:
            print(f"❌ Erreur de test SMTP: {str(e)}")
            print("⚠️  Vérifiez votre mot de passe d'application")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def update_env_with_app_password():
    """Met à jour le fichier .env avec le mot de passe d'application"""
    print(f"\n🔧 Mise à jour du fichier .env...")
    
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
    print("• Ajoutez EMAIL_HOST_PASSWORD=votre_mot_de_passe_application")
    print("• Le mot de passe d'application doit faire 16 caractères")
    print("• Redémarrez votre serveur après modification")

def show_app_password_guide():
    """Affiche le guide pour créer un mot de passe d'application"""
    print(f"\n📋 GUIDE CRÉATION MOT DE PASSE D'APPLICATION")
    print("=" * 50)
    print("1. Allez sur https://account.microsoft.com/security")
    print("2. Connectez-vous avec votre compte Outlook")
    print("3. Allez dans 'Sécurité' → 'Mots de passe d'application'")
    print("4. Cliquez sur 'Créer un nouveau mot de passe d'application'")
    print("5. Donnez un nom (ex: 'Application Django')")
    print("6. Copiez le mot de passe généré (16 caractères)")
    print("7. Utilisez ce mot de passe dans la configuration")
    print("=" * 50)

def main():
    """Fonction principale"""
    print("🔧 CORRECTION AUTHENTIFICATION OUTLOOK")
    print("=" * 50)
    print("Ce script corrige l'authentification Outlook")
    print("=" * 50)
    
    # Afficher le guide
    show_app_password_guide()
    
    # Demander confirmation
    continue_setup = input("\nVoulez-vous continuer ? (o/n): ").strip().lower()
    if continue_setup != 'o':
        print("❌ Configuration annulée")
        return False
    
    # Configurer Outlook SMTP avec mot de passe d'application
    success = fix_outlook_authentication()
    
    if success:
        # Mettre à jour les settings Django
        update_env_with_app_password()
        
        print(f"\n🎉 CONFIGURATION TERMINÉE!")
        print("=" * 50)
        print("✅ Outlook SMTP configuré avec mot de passe d'application")
        print("✅ Vous pouvez maintenant envoyer des emails")
        print("✅ Allez sur /dashboard/emails/ pour gérer les emails")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Mettez à jour vos variables d'environnement")
        print("2. Redémarrez votre serveur")
        print("3. Testez l'envoi d'emails")
    else:
        print(f"\n❌ CONFIGURATION ÉCHOUÉE")
        print("🔧 Vérifiez votre mot de passe d'application")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
