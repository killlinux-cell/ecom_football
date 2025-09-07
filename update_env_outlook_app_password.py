#!/usr/bin/env python
"""
Script pour mettre à jour le fichier .env avec le mot de passe d'application Outlook
"""

import os
import sys

def update_env_file_with_app_password():
    """Met à jour le fichier .env avec le mot de passe d'application Outlook"""
    print("📧 MISE À JOUR DU FICHIER .ENV POUR OUTLOOK (MOT DE PASSE D'APPLICATION)")
    print("=" * 70)
    
    # Demander les informations
    print("Configuration Outlook SMTP avec mot de passe d'application")
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
    
    # Configuration Outlook avec mot de passe d'application
    outlook_config = {
        'EMAIL_HOST': 'smtp-mail.outlook.com',
        'EMAIL_PORT': '587',
        'EMAIL_USE_TLS': 'True',
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'EMAIL_HOST_USER': email,
        'EMAIL_HOST_PASSWORD': app_password
    }
    
    # Chemin du fichier .env
    env_file = '.env'
    
    try:
        # Lire le fichier .env existant
        existing_lines = []
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                existing_lines = f.readlines()
        
        # Créer un dictionnaire des variables existantes
        existing_vars = {}
        for line in existing_lines:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                existing_vars[key] = value
        
        # Mettre à jour avec les nouvelles valeurs
        for key, value in outlook_config.items():
            existing_vars[key] = value
        
        # Écrire le fichier .env mis à jour
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("# Configuration Outlook SMTP avec mot de passe d'application\n")
            f.write("# Généré automatiquement\n\n")
            
            # Écrire les variables email
            f.write("# Configuration Email Outlook\n")
            for key, value in outlook_config.items():
                f.write(f"{key}={value}\n")
            
            f.write("\n")
            
            # Écrire les autres variables existantes (non email)
            f.write("# Autres variables\n")
            for key, value in existing_vars.items():
                if not key.startswith('EMAIL_'):
                    f.write(f"{key}={value}\n")
        
        print(f"\n✅ Fichier .env mis à jour avec succès")
        print(f"📁 Fichier: {os.path.abspath(env_file)}")
        
        # Afficher la configuration
        print(f"\n📧 Configuration Outlook:")
        print("-" * 30)
        for key, value in outlook_config.items():
            if 'PASSWORD' in key:
                print(f"{key}=••••••••")
            else:
                print(f"{key}={value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {str(e)}")
        return False

def create_env_example_with_app_password():
    """Crée un fichier .env.example avec la configuration Outlook et mot de passe d'application"""
    print(f"\n📝 Création du fichier .env.example...")
    
    example_content = """# Configuration Outlook SMTP avec mot de passe d'application
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=votre_email@outlook.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_application

# Autres variables
SECRET_KEY=votre_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    try:
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(example_content)
        
        print("✅ Fichier .env.example créé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")
        return False

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
    print("📧 MISE À JOUR .ENV POUR OUTLOOK (MOT DE PASSE D'APPLICATION)")
    print("=" * 70)
    print("Ce script met à jour votre fichier .env avec Outlook SMTP")
    print("en utilisant un mot de passe d'application")
    print("=" * 70)
    
    # Afficher le guide
    show_app_password_guide()
    
    # Demander confirmation
    continue_setup = input("\nVoulez-vous continuer ? (o/n): ").strip().lower()
    if continue_setup != 'o':
        print("❌ Mise à jour annulée")
        return False
    
    # Mettre à jour le fichier .env
    success = update_env_file_with_app_password()
    
    if success:
        # Créer le fichier .env.example
        create_env_example_with_app_password()
        
        print(f"\n🎉 MISE À JOUR TERMINÉE!")
        print("=" * 50)
        print("✅ Fichier .env mis à jour avec Outlook SMTP")
        print("✅ Mot de passe d'application configuré")
        print("✅ Fichier .env.example créé")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Redémarrez votre serveur Django")
        print("2. Testez l'envoi d'emails")
        print("3. Vérifiez les logs pour les erreurs")
    else:
        print(f"\n❌ MISE À JOUR ÉCHOUÉE")
        print("🔧 Vérifiez les permissions du fichier .env")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
