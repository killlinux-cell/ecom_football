# 📧 **GUIDE CONFIGURATION OUTLOOK SMTP**

## 🎯 **Vue d'ensemble**

Ce guide vous explique comment configurer Outlook SMTP pour votre application Django de maillots de football.

## 📋 **Prérequis**

- Compte Outlook/Hotmail actif
- Authentification à 2 facteurs activée (recommandé)
- Accès à votre serveur VPS

## 🔧 **Configuration Outlook SMTP**

### **Paramètres SMTP Outlook :**
```
Serveur SMTP: smtp-mail.outlook.com
Port: 587
Sécurité: TLS (STARTTLS)
Authentification: Oui
```

### **Étapes de configuration :**

#### **1. Préparer votre compte Outlook**
1. Connectez-vous à votre compte Outlook
2. Allez dans **Paramètres** → **Sécurité**
3. Activez l'**authentification à 2 facteurs** (recommandé)
4. Notez votre email et mot de passe

#### **2. Configuration automatique (recommandée)**
```bash
# Exécuter le script de configuration
python configure_outlook_smtp.py
```

#### **3. Configuration manuelle**

**A. Mettre à jour le fichier .env :**
```bash
# Exécuter le script de mise à jour
python update_env_outlook.py
```

**B. Ou modifier manuellement le fichier .env :**
```env
# Configuration Outlook SMTP
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=votre_email@outlook.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe
```

## 🚀 **Déploiement sur VPS**

### **1. Configuration sur le VPS**
```bash
# Se connecter au VPS
ssh root@votre_vps_ip

# Aller dans le répertoire du projet
cd /var/www/ecom_football

# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter la configuration
python configure_outlook_smtp.py
```

### **2. Mettre à jour les variables d'environnement**
```bash
# Créer ou modifier le fichier .env
nano .env

# Ajouter la configuration Outlook
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=votre_email@outlook.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe
```

### **3. Redémarrer les services**
```bash
# Redémarrer Gunicorn
sudo systemctl restart gunicorn

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier les logs
sudo journalctl -u gunicorn -f
```

## 🧪 **Test de la configuration**

### **1. Test automatique**
```bash
# Vérifier le système d'emails
python check_email_system_ready.py
```

### **2. Test manuel**
```bash
# Tester l'envoi d'email
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

# Test d'envoi
send_mail(
    'Test Outlook SMTP',
    'Ceci est un test de configuration Outlook.',
    settings.EMAIL_HOST_USER,
    ['votre_email@outlook.com'],
    fail_silently=False,
)
```

## 🔍 **Dépannage**

### **Erreurs courantes :**

#### **1. "Authentication failed"**
- Vérifiez votre email et mot de passe
- Assurez-vous que l'authentification à 2 facteurs est activée
- Vérifiez que le compte n'est pas verrouillé

#### **2. "Connection refused"**
- Vérifiez que le port 587 n'est pas bloqué
- Testez la connexion : `telnet smtp-mail.outlook.com 587`

#### **3. "TLS/SSL error"**
- Vérifiez que `EMAIL_USE_TLS=True`
- Assurez-vous que le port 587 est utilisé

### **Commandes de diagnostic :**
```bash
# Tester la connexion SMTP
telnet smtp-mail.outlook.com 587

# Vérifier les logs Django
tail -f /var/log/django/error.log

# Vérifier les logs Gunicorn
sudo journalctl -u gunicorn -f
```

## 📊 **Monitoring**

### **1. Vérifier les emails envoyés**
```bash
# Aller sur le dashboard
https://votre_domaine.com/dashboard/emails/
```

### **2. Vérifier les logs d'emails**
```bash
# Voir les logs d'emails
python manage.py shell
```

```python
from notifications.models import EmailLog

# Voir les derniers emails
logs = EmailLog.objects.all().order_by('-created_at')[:10]
for log in logs:
    print(f"{log.created_at}: {log.email_type} - {log.status}")
```

## 🎯 **Avantages d'Outlook vs Gmail**

### **Outlook :**
- ✅ Pas besoin de mot de passe d'application
- ✅ Authentification standard
- ✅ Limites généreuses
- ✅ Intégration Microsoft

### **Gmail :**
- ✅ Plus populaire
- ✅ Meilleure délivrabilité
- ❌ Nécessite un mot de passe d'application
- ❌ Configuration plus complexe

## 📋 **Checklist de déploiement**

- [ ] Compte Outlook configuré
- [ ] Authentification à 2 facteurs activée
- [ ] Script de configuration exécuté
- [ ] Fichier .env mis à jour
- [ ] Services redémarrés
- [ ] Test d'envoi réussi
- [ ] Dashboard emails accessible
- [ ] Logs d'emails fonctionnels

## 🆘 **Support**

Si vous rencontrez des problèmes :

1. **Vérifiez les logs** : `sudo journalctl -u gunicorn -f`
2. **Testez la connexion** : `telnet smtp-mail.outlook.com 587`
3. **Vérifiez les variables** : `python check_email_system_ready.py`
4. **Consultez les logs d'emails** : Dashboard → Emails → Logs

## 🎉 **Conclusion**

Avec cette configuration Outlook, votre système d'emails sera :
- ✅ **Fiable** : Connexion SMTP stable
- ✅ **Sécurisé** : Authentification TLS
- ✅ **Monitored** : Logs complets
- ✅ **Scalable** : Prêt pour la production

Votre application est maintenant prête à envoyer des emails de confirmation, notifications et rappels !
