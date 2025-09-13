#!/usr/bin/env python
"""
Script pour corriger l'authentification Gmail sur le VPS
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_gmail_authentication_vps():
    """Corrige l'authentification Gmail sur le VPS"""
    print("🔧 CORRECTION AUTHENTIFICATION GMAIL VPS")
    print("=" * 50)
    
    try:
        from notifications.models import EmailSettings
        
        # Demander les informations Gmail
        print("\n📧 Configuration Gmail pour le VPS")
        print("-" * 50)
        
        email = input("Votre email Gmail (ex: anakoisrael352@gmail.com): ").strip()
        if not email:
            print("❌ Email requis")
            return False
        
        print("\n⚠️  IMPORTANT: Vous devez créer un mot de passe d'application Gmail")
        print("1. Allez sur https://myaccount.google.com/security")
        print("2. Connectez-vous avec votre compte Gmail")
        print("3. Allez dans 'Sécurité' → 'Mots de passe d'application'")
        print("4. Sélectionnez 'Application' → 'Autre'")
        print("5. Donnez un nom (ex: 'Django VPS')")
        print("6. Copiez le mot de passe généré (16 caractères)")
        
        app_password = input("\nMot de passe d'application Gmail (16 caractères): ").strip()
        if not app_password or len(app_password) != 16:
            print("❌ Mot de passe d'application requis (16 caractères)")
            return False
        
        sender_name = input("Nom de l'expéditeur (ex: Maillots Football): ").strip()
        if not sender_name:
            sender_name = "Maillots Football"
        
        # Configuration Gmail SMTP
        gmail_config = {
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_use_tls': True,
            'smtp_username': email,
            'smtp_password': app_password,
            'sender_email': email,
            'sender_name': sender_name,
            'is_active': True,
            'send_order_confirmations': True,
            'send_payment_confirmations': True,
            'send_shipping_notifications': True,
            'send_cart_reminders': True,
            'send_stock_alerts': True,
        }
        
        # Mettre à jour ou créer la configuration
        email_settings, created = EmailSettings.objects.get_or_create(
            defaults=gmail_config
        )
        
        if not created:
            # Mettre à jour la configuration existante
            for key, value in gmail_config.items():
                setattr(email_settings, key, value)
            email_settings.save()
        
        print(f"\n✅ Configuration Gmail mise à jour")
        
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
            
            print("✅ Connexion SMTP réussie !")
            print("✅ Configuration Gmail validée")
            
        except Exception as e:
            print(f"❌ Erreur de test SMTP: {str(e)}")
            print("⚠️  Vérifiez votre mot de passe d'application")
            return False
        
        # Mettre à jour le fichier .env
        update_env_file(email, app_password)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def update_env_file(email, app_password):
    """Met à jour le fichier .env avec les nouvelles informations"""
    print(f"\n🔧 Mise à jour du fichier .env...")
    
    env_content = f"""# Configuration Gmail pour VPS
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER={email}
EMAIL_HOST_PASSWORD={app_password}

# Production
DEBUG=False
ALLOWED_HOSTS=orapide.shop,www.orapide.shop,206.72.198.105

# Clés secrètes
SECRET_KEY=django-insecure-ks99&9o(6@n%y5ukn_+a=bkm)h!=rww9tn3mrm+ecj9f$+931a
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Fichier .env mis à jour")
    except Exception as e:
        print(f"❌ Erreur mise à jour .env: {str(e)}")
    
    print(f"\n📝 Paramètres à ajouter dans vos variables d'environnement:")
    print("-" * 50)
    print(f"EMAIL_HOST=smtp.gmail.com")
    print(f"EMAIL_PORT=587")
    print(f"EMAIL_USE_TLS=True")
    print(f"EMAIL_HOST_USER={email}")
    print(f"EMAIL_HOST_PASSWORD={app_password}")

def main():
    """Fonction principale"""
    print("🔧 CORRECTION AUTHENTIFICATION GMAIL VPS")
    print("=" * 50)
    print("Ce script corrige l'authentification Gmail sur le VPS")
    print("=" * 50)
    
    # Corriger l'authentification Gmail
    success = fix_gmail_authentication_vps()
    
    if success:
        print(f"\n🎉 CONFIGURATION TERMINÉE!")
        print("=" * 50)
        print("✅ Gmail SMTP configuré avec mot de passe d'application")
        print("✅ Fichier .env mis à jour")
        print("✅ Vous pouvez maintenant envoyer des emails")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Redémarrez votre serveur: sudo systemctl restart gunicorn")
        print("2. Testez l'envoi d'emails: python test_final_emails.py")
        print("3. Vérifiez les logs d'emails")
    else:
        print(f"\n❌ CONFIGURATION ÉCHOUÉE")
        print("🔧 Vérifiez votre mot de passe d'application")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
