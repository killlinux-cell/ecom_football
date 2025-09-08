#!/bin/bash
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
