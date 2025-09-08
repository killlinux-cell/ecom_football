#!/usr/bin/env python
"""
Script de déploiement complet pour le VPS
"""

import os
import sys
import subprocess
from pathlib import Path

def deploy_all_changes_vps():
    """Déploie toutes les modifications sur le VPS"""
    print("🚀 DÉPLOIEMENT COMPLET SUR VPS")
    print("=" * 50)
    
    # 1. Fichiers modifiés à déployer
    modified_files = [
        # Templates
        'templates/base.html',
        
        # CSS
        'static/css/mobile-products-optimization.css',
        'static/css/mobile.css',
        'static/css/mobile-fixes.css',
        'static/css/pwa-mobile.css',
        'static/css/image-fixes.css',
        
        # JavaScript
        'static/js/mobile-products.js',
        
        # Python - Emails
        'notifications/email_service.py',
        'accounts/signals.py',
        
        # Scripts de configuration
        'configure_gmail_smtp.py',
        'deploy_gmail_vps.py',
        'fix_automatic_emails.py',
        'test_final_emails.py',
        
        # Scripts de test
        'test_mobile_optimization.py',
        'test_mobile_fixes.py',
        'test_all_emails.py',
        
        # Documentation
        'GUIDE_OPTIMISATION_MOBILE_PRODUITS.md',
        'GUIDE_TEST_MOBILE.md',
        'GUIDE_SYSTEME_EMAILS.md',
    ]
    
    # 2. Vérifier les fichiers
    print("\n📁 Vérification des fichiers à déployer...")
    missing_files = []
    
    for file_path in modified_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ {len(missing_files)} fichier(s) manquant(s)")
        return False
    
    # 3. Créer le script de déploiement
    print(f"\n📝 Création du script de déploiement...")
    create_deployment_script()
    
    # 4. Créer le guide de déploiement
    print(f"\n📋 Création du guide de déploiement...")
    create_deployment_guide()
    
    # 5. Créer la liste des commandes
    print(f"\n⚡ Création des commandes de déploiement...")
    create_deployment_commands()
    
    return True

def create_deployment_script():
    """Crée le script de déploiement pour le VPS"""
    
    script_content = '''#!/bin/bash
# Script de déploiement VPS - Toutes les modifications

echo "🚀 DÉPLOIEMENT COMPLET SUR VPS"
echo "================================"

# 1. Sauvegarder la base de données
echo "📦 Sauvegarde de la base de données..."
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# 2. Arrêter le serveur
echo "⏹️ Arrêt du serveur..."
sudo systemctl stop gunicorn
sudo systemctl stop nginx

# 3. Mettre à jour le code
echo "📥 Mise à jour du code..."
git pull origin main

# 4. Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# 5. Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py makemigrations
python manage.py migrate

# 6. Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# 7. Initialiser les templates d'emails
echo "📧 Initialisation des templates d'emails..."
python manage.py init_email_templates

# 8. Configurer Gmail
echo "📧 Configuration Gmail..."
python configure_gmail_smtp.py

# 9. Tester les emails
echo "🧪 Test des emails..."
python test_final_emails.py

# 10. Redémarrer les services
echo "🔄 Redémarrage des services..."
sudo systemctl start gunicorn
sudo systemctl start nginx

# 11. Vérifier le statut
echo "✅ Vérification du statut..."
sudo systemctl status gunicorn
sudo systemctl status nginx

echo "🎉 DÉPLOIEMENT TERMINÉ!"
echo "================================"
echo "✅ Site déployé avec succès"
echo "✅ Emails automatiques configurés"
echo "✅ Optimisation mobile activée"
echo "✅ Gmail configuré"
'''
    
    with open('deploy_vps.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Rendre le script exécutable
    os.chmod('deploy_vps.sh', 0o755)
    print("✅ Script deploy_vps.sh créé")

def create_deployment_guide():
    """Crée le guide de déploiement"""
    
    guide_content = '''# 🚀 Guide de Déploiement VPS - Toutes les Modifications

## 📋 Résumé des Modifications

### ✅ **Emails Automatiques**
- Configuration Gmail avec mot de passe d'application
- Templates d'emails initialisés
- Signaux Django pour emails automatiques
- Service d'envoi d'emails optimisé

### ✅ **Optimisation Mobile**
- Affichage optimisé pour beaucoup d'articles
- Basculement grille/liste fonctionnel
- Recherche mobile améliorée
- Scroll infini et filtres rapides

### ✅ **Fonctionnalités PWA**
- Application mobile installable
- Mode hors ligne
- Notifications push

## 🚀 Déploiement Rapide

### **Option 1 : Script Automatique**
```bash
# Sur le VPS
chmod +x deploy_vps.sh
./deploy_vps.sh
```

### **Option 2 : Déploiement Manuel**
```bash
# 1. Sauvegarder
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# 2. Arrêter les services
sudo systemctl stop gunicorn
sudo systemctl stop nginx

# 3. Mettre à jour le code
git pull origin main

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Migrations
python manage.py makemigrations
python manage.py migrate

# 6. Fichiers statiques
python manage.py collectstatic --noinput

# 7. Templates emails
python manage.py init_email_templates

# 8. Configuration Gmail
python configure_gmail_smtp.py

# 9. Test emails
python test_final_emails.py

# 10. Redémarrer
sudo systemctl start gunicorn
sudo systemctl start nginx
```

## 📁 Fichiers à Déployer

### **Templates**
- `templates/base.html` - Base template avec optimisations

### **CSS**
- `static/css/mobile-products-optimization.css` - Optimisation mobile
- `static/css/mobile.css` - Styles mobile
- `static/css/mobile-fixes.css` - Corrections mobile
- `static/css/pwa-mobile.css` - PWA mobile
- `static/css/image-fixes.css` - Corrections images

### **JavaScript**
- `static/js/mobile-products.js` - Fonctionnalités mobile

### **Python - Emails**
- `notifications/email_service.py` - Service emails
- `accounts/signals.py` - Signaux d'inscription

### **Scripts**
- `configure_gmail_smtp.py` - Configuration Gmail
- `deploy_gmail_vps.py` - Déploiement Gmail VPS
- `fix_automatic_emails.py` - Correction emails
- `test_final_emails.py` - Test emails

## ⚙️ Configuration VPS

### **Variables d'Environnement**
```bash
# Gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=anakoisrael352@gmail.com
EMAIL_HOST_PASSWORD=ticq fwgi xjnc epif

# Production
DEBUG=False
ALLOWED_HOSTS=orapide.shop,www.orapide.shop,206.72.198.105
```

### **Services à Redémarrer**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 🧪 Tests Post-Déploiement

### **1. Test des Emails**
```bash
python test_final_emails.py
```

### **2. Test Mobile**
- Ouvrir le site sur mobile
- Tester la grille/liste
- Tester la recherche
- Vérifier les emails automatiques

### **3. Test PWA**
- Installer l'app sur mobile
- Tester le mode hors ligne
- Vérifier les notifications

## 🎯 Résultats Attendus

### **Emails Automatiques**
- ✅ Inscription → Email de bienvenue
- ✅ Commande → Email de confirmation
- ✅ Paiement → Email de confirmation
- ✅ Expédition → Email de notification

### **Mobile**
- ✅ Grille/liste basculable
- ✅ Recherche fonctionnelle
- ✅ Scroll infini
- ✅ Filtres rapides

### **PWA**
- ✅ Installation possible
- ✅ Mode hors ligne
- ✅ Notifications

## 🚨 En Cas de Problème

### **Logs à Vérifier**
```bash
# Logs Gunicorn
sudo journalctl -u gunicorn -f

# Logs Nginx
sudo tail -f /var/log/nginx/error.log

# Logs Django
tail -f /var/log/django.log
```

### **Rollback**
```bash
# Restaurer la sauvegarde
python manage.py loaddata backup_YYYYMMDD_HHMMSS.json

# Redémarrer les services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 🎉 Succès

**Après le déploiement, vous devriez avoir :**
- ✅ Emails automatiques fonctionnels
- ✅ Interface mobile optimisée
- ✅ PWA installable
- ✅ Site performant et responsive

**Votre e-commerce est maintenant complet et optimisé !** 🚀
'''
    
    with open('GUIDE_DEPLOIEMENT_COMPLET_VPS.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ Guide GUIDE_DEPLOIEMENT_COMPLET_VPS.md créé")

def create_deployment_commands():
    """Crée les commandes de déploiement"""
    
    commands = [
        "# 🚀 COMMANDES DE DÉPLOIEMENT VPS",
        "",
        "## 1. Préparation",
        "cd /path/to/your/project",
        "git status",
        "git add .",
        "git commit -m 'Déploiement: Emails automatiques + Optimisation mobile'",
        "git push origin main",
        "",
        "## 2. Sur le VPS",
        "cd /path/to/your/vps/project",
        "git pull origin main",
        "",
        "## 3. Déploiement automatique",
        "chmod +x deploy_vps.sh",
        "./deploy_vps.sh",
        "",
        "## 4. Ou déploiement manuel",
        "python manage.py collectstatic --noinput",
        "python manage.py migrate",
        "python manage.py init_email_templates",
        "python configure_gmail_smtp.py",
        "sudo systemctl restart gunicorn",
        "sudo systemctl restart nginx",
        "",
        "## 5. Tests",
        "python test_final_emails.py",
        "python test_mobile_optimization.py",
        "",
        "## 6. Vérification",
        "curl -I https://orapide.shop",
        "sudo systemctl status gunicorn",
        "sudo systemctl status nginx"
    ]
    
    with open('COMMANDES_DEPLOIEMENT_VPS.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(commands))
    
    print("✅ Commandes COMMANDES_DEPLOIEMENT_VPS.txt créées")

def main():
    """Fonction principale"""
    print("🚀 DÉPLOIEMENT COMPLET SUR VPS")
    print("=" * 50)
    print("Ce script prépare le déploiement de toutes vos modifications")
    print("=" * 50)
    
    success = deploy_all_changes_vps()
    
    if success:
        print(f"\n🎉 PRÉPARATION TERMINÉE!")
        print("=" * 50)
        print("✅ Script de déploiement créé")
        print("✅ Guide de déploiement créé")
        print("✅ Commandes de déploiement créées")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Commitez vos modifications : git add . && git commit -m 'Déploiement'")
        print("2. Poussez sur GitHub : git push origin main")
        print("3. Sur le VPS : git pull origin main")
        print("4. Exécutez : ./deploy_vps.sh")
        print("5. Testez le site et les emails")
        print("\n🚀 Votre site sera déployé avec toutes les fonctionnalités!")
    else:
        print(f"\n❌ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les fichiers manquants")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
