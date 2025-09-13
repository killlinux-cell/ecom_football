# 🔧 Guide de Résolution des Problèmes VPS

## 🚨 Problèmes Identifiés

### ❌ **1. Template `user_welcome` non trouvé**
- **Cause** : Template d'email de bienvenue manquant
- **Solution** : Créer le template manquant

### ❌ **2. Erreur d'authentification Gmail**
- **Cause** : Mot de passe d'application incorrect ou expiré
- **Solution** : Reconfigurer Gmail avec un nouveau mot de passe

## 🔧 Solutions

### **1. Créer le Template User Welcome**

#### **Sur le VPS :**
```bash
# Exécuter le script de création
python create_user_welcome_template.py
```

#### **Ou manuellement :**
```bash
# Initialiser tous les templates
python manage.py init_email_templates

# Vérifier que le template existe
python -c "
from notifications.models import EmailTemplate
template = EmailTemplate.objects.filter(template_type='user_welcome').first()
print('Template trouvé:', template is not None)
"
```

### **2. Corriger l'Authentification Gmail**

#### **Étape 1 : Créer un nouveau mot de passe d'application**
1. **Aller sur** : https://myaccount.google.com/security
2. **Se connecter** avec votre compte Gmail
3. **Aller dans** : 'Sécurité' → 'Mots de passe d'application'
4. **Sélectionner** : 'Application' → 'Autre'
5. **Donner un nom** : 'Django VPS'
6. **Copier** le mot de passe généré (16 caractères)

#### **Étape 2 : Reconfigurer Gmail sur le VPS**
```bash
# Exécuter le script de correction
python fix_gmail_authentication_vps.py
```

#### **Étape 3 : Mettre à jour les variables d'environnement**
```bash
# Éditer le fichier .env
nano .env

# Ajouter ou modifier :
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=anakoisrael352@gmail.com
EMAIL_HOST_PASSWORD=votre_nouveau_mot_de_passe_application
```

#### **Étape 4 : Redémarrer les services**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## 🧪 Tests de Vérification

### **1. Test des Templates**
```bash
python -c "
from notifications.models import EmailTemplate
templates = EmailTemplate.objects.all()
for t in templates:
    print(f'{t.template_type}: {t.name}')
"
```

### **2. Test de la Configuration Gmail**
```bash
python -c "
from notifications.models import EmailSettings
settings = EmailSettings.objects.first()
if settings:
    print(f'SMTP: {settings.smtp_host}:{settings.smtp_port}')
    print(f'Email: {settings.sender_email}')
    print(f'TLS: {settings.smtp_use_tls}')
else:
    print('Aucune configuration trouvée')
"
```

### **3. Test Complet des Emails**
```bash
python test_final_emails.py
```

## 📋 Résultats Attendus

### **Après Correction :**
```
🎯 TEST FINAL DES EMAILS AUTOMATIQUES
==================================================
✅ Service email initialisé

👤 Test email de bienvenue...
✅ Email de bienvenue envoyé

📦 Test email de commande...
✅ Email de commande envoyé

💳 Test email de paiement...
✅ Email de paiement envoyé

📋 Vérification des logs...
   ✅ Bienvenue sur Maillots Football ! → test@example.com
   ✅ Confirmation de votre commande #CMD123 → test@example.com
   ✅ Paiement confirmé - Commande #CMD123 → test@example.com
```

## 🚨 En Cas de Problème Persistant

### **Vérifier les Logs**
```bash
# Logs Gunicorn
sudo journalctl -u gunicorn -f

# Logs Nginx
sudo tail -f /var/log/nginx/error.log

# Logs Django
tail -f /var/log/django.log
```

### **Vérifier la Configuration**
```bash
# Vérifier les variables d'environnement
env | grep EMAIL

# Vérifier la base de données
python manage.py shell
>>> from notifications.models import EmailSettings
>>> settings = EmailSettings.objects.first()
>>> print(settings.smtp_host, settings.smtp_port)
```

### **Test de Connexion SMTP**
```bash
python -c "
import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('anakoisrael352@gmail.com', 'votre_mot_de_passe')
    print('✅ Connexion SMTP réussie')
    server.quit()
except Exception as e:
    print(f'❌ Erreur SMTP: {e}')
"
```

## 🎯 Commandes de Résolution Rapide

### **Script Complet de Correction**
```bash
# 1. Créer le template manquant
python create_user_welcome_template.py

# 2. Corriger l'authentification Gmail
python fix_gmail_authentication_vps.py

# 3. Redémarrer les services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# 4. Tester
python test_final_emails.py
```

## 🎉 Succès

**Après correction, vous devriez avoir :**
- ✅ **Template user_welcome** créé et fonctionnel
- ✅ **Authentification Gmail** corrigée
- ✅ **Emails automatiques** opérationnels
- ✅ **Tests** qui passent avec succès

**Vos emails automatiques fonctionneront maintenant parfaitement !** 🚀
