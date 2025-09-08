#!/usr/bin/env python
"""
Script de déploiement Gmail sur VPS
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def deploy_gmail_vps():
    """Déploie la configuration Gmail sur VPS"""
    print("🚀 DÉPLOIEMENT GMAIL SUR VPS")
    print("=" * 50)
    
    try:
        from notifications.models import EmailSettings
        
        # Configuration Gmail pour VPS
        gmail_config = {
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_use_tls': True,
            'smtp_username': 'anakoisrael352@gmail.com',
            'smtp_password': 'ticq fwgi xjnc epif',
            'sender_email': 'anakoisrael352@gmail.com',
            'sender_name': 'Maillots Football',
            'is_active': True
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
        
        print(f"\n✅ Configuration Gmail déployée sur VPS")
        
        # Afficher la configuration
        print(f"\n📧 Configuration SMTP VPS:")
        print(f"   Serveur: {email_settings.smtp_host}:{email_settings.smtp_port}")
        print(f"   Email: {email_settings.sender_email}")
        print(f"   TLS: {'Activé' if email_settings.smtp_use_tls else 'Désactivé'}")
        print(f"   Expéditeur: {email_settings.sender_name} <{email_settings.sender_email}>")
        
        # Test de la configuration
        print(f"\n🧪 Test de la configuration VPS...")
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            server = smtplib.SMTP(email_settings.smtp_host, email_settings.smtp_port)
            server.starttls()
            server.login(email_settings.smtp_username, email_settings.smtp_password)
            server.quit()
            
            print("✅ Connexion SMTP VPS réussie !")
            print("✅ Configuration Gmail VPS validée")
            
        except Exception as e:
            print(f"❌ Erreur de test SMTP VPS: {str(e)}")
            print("⚠️  Vérifiez votre configuration réseau VPS")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du déploiement VPS: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_vps_env_file():
    """Crée le fichier .env pour VPS"""
    print(f"\n🔧 Création du fichier .env pour VPS...")
    
    env_content = """# Configuration Gmail pour VPS
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=anakoisrael352@gmail.com
EMAIL_HOST_PASSWORD=ticq fwgi xjnc epif

# Autres paramètres VPS
DEBUG=False
ALLOWED_HOSTS=orapide.shop,www.orapide.shop,206.72.198.105

# Base de données (si nécessaire)
# DATABASE_URL=sqlite:///db.sqlite3

# Clés secrètes
SECRET_KEY=django-insecure-ks99&9o(6@n%y5ukn_+a=bkm)h!=rww9tn3mrm+ecj9f$+931a
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Fichier .env créé pour VPS")
    print("📝 Contenu du fichier .env:")
    print("-" * 30)
    print(env_content)

def show_vps_deployment_guide():
    """Affiche le guide de déploiement VPS"""
    print(f"\n📋 GUIDE DÉPLOIEMENT VPS GMAIL")
    print("=" * 50)
    print("1. Uploadez ce script sur votre VPS")
    print("2. Exécutez: python deploy_gmail_vps.py")
    print("3. Le script configurera automatiquement Gmail")
    print("4. Les emails fonctionneront automatiquement")
    print("5. Redémarrez votre serveur VPS")
    print("=" * 50)

def main():
    """Fonction principale"""
    print("🚀 DÉPLOIEMENT GMAIL SUR VPS")
    print("=" * 50)
    print("Ce script déploie la configuration Gmail sur VPS")
    print("=" * 50)
    
    # Afficher le guide
    show_vps_deployment_guide()
    
    # Demander confirmation
    continue_deploy = input("\nVoulez-vous déployer sur VPS ? (o/n): ").strip().lower()
    if continue_deploy != 'o':
        print("❌ Déploiement annulé")
        return False
    
    # Déployer Gmail sur VPS
    success = deploy_gmail_vps()
    
    if success:
        # Créer le fichier .env
        create_vps_env_file()
        
        print(f"\n🎉 DÉPLOIEMENT VPS TERMINÉ!")
        print("=" * 50)
        print("✅ Gmail SMTP configuré sur VPS")
        print("✅ Fichier .env créé")
        print("✅ Les emails fonctionneront automatiquement")
        print("\n📋 PROCHAINES ÉTAPES VPS:")
        print("1. Redémarrez votre serveur VPS")
        print("2. Testez l'envoi d'emails")
        print("3. Vérifiez les logs d'emails")
    else:
        print(f"\n❌ DÉPLOIEMENT VPS ÉCHOUÉ")
        print("🔧 Vérifiez votre configuration réseau VPS")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
