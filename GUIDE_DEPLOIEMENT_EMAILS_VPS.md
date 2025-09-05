# 🚀 Guide Déploiement Emails sur VPS

## ❌ **Problème Identifié**

Sur le VPS, lors du test d'envoi d'email, vous obtenez l'erreur :
```
Template non trouvé!
```

**Cause :** Les templates d'emails n'ont pas été initialisés sur le serveur de production.

---

## ✅ **Solution - Commandes à Exécuter sur le VPS**

### **1. Se Connecter au VPS**

```bash
ssh root@votre-vps-ip
cd /var/www/ecom_football  # ou le chemin de votre projet
source venv/bin/activate   # activer l'environnement virtuel
```

### **2. Appliquer les Migrations (si pas déjà fait)**

```bash
python manage.py migrate
```

### **3. Initialiser les Templates d'Emails**

```bash
python manage.py init_email_templates
```

**Résultat attendu :**
```
📧 Initialisation des templates d'emails...
✅ Template créé: Confirmation de commande
✅ Template créé: Confirmation de paiement
✅ Template créé: Notification d'expédition
✅ Template créé: Notification de livraison
✅ Template créé: Rappel de panier abandonné
✅ Template créé: Alerte stock faible
🎉 6 template(s) créé(s), 0 mis à jour(s)
```

### **4. Vérifier les Templates**

```bash
python manage.py shell
```

Dans le shell Python :
```python
from notifications.models import EmailTemplate
templates = EmailTemplate.objects.all()
for template in templates:
    print(f"- {template.name} ({template.template_type}) - {'Actif' if template.is_active else 'Inactif'}")
exit()
```

### **5. Configurer les Paramètres SMTP**

Aller dans l'interface d'administration :
```
https://votre-domaine.com/dashboard/emails/settings/
```

Configurer :
- **SMTP Host** : `smtp.gmail.com` (pour Gmail)
- **SMTP Port** : `587`
- **SMTP Username** : votre email Gmail
- **SMTP Password** : mot de passe d'application Gmail
- **Use TLS** : ✅ Activé
- **From Email** : votre email
- **From Name** : "Maillots Football"

### **6. Tester l'Envoi d'Email**

Dans l'interface d'administration :
1. Aller dans `/dashboard/emails/settings/`
2. Section "Test d'envoi"
3. Remplir :
   - **Email destinataire** : votre email de test
   - **Type de template** : `order_confirmation`
4. Cliquer sur "Envoyer Email de Test"

---

## 🔧 **Script Automatique de Déploiement**

Si vous préférez, vous pouvez utiliser le script automatique :

```bash
# Télécharger le script sur le VPS
wget https://raw.githubusercontent.com/votre-repo/deploy_email_templates_vps.py

# Ou créer le fichier manuellement
nano deploy_email_templates_vps.py
# Copier le contenu du script

# Exécuter le script
python deploy_email_templates_vps.py
```

---

## 🧪 **Tests de Validation**

### **Test 1 : Vérifier les Templates**

```bash
python manage.py shell
```

```python
from notifications.models import EmailTemplate
print("Templates disponibles:")
for template in EmailTemplate.objects.filter(is_active=True):
    print(f"✅ {template.template_type}: {template.name}")
```

### **Test 2 : Tester le Service d'Emails**

```python
from notifications.email_service import get_email_service
service = get_email_service()
print(f"Service configuré: {service.settings is not None}")
if service.settings:
    print(f"Email expéditeur: {service.settings.from_email}")
    print(f"Statut: {'Actif' if service.settings.is_active else 'Inactif'}")
```

### **Test 3 : Envoi d'Email de Test**

```python
from notifications.models import EmailTemplate
from notifications.email_service import get_email_service

# Récupérer un template
template = EmailTemplate.objects.filter(template_type='order_confirmation', is_active=True).first()
if template:
    print(f"✅ Template trouvé: {template.name}")
else:
    print("❌ Template non trouvé")
```

---

## 🚨 **Dépannage**

### **Erreur : "Template non trouvé"**

**Solution :**
```bash
python manage.py init_email_templates
```

### **Erreur : "SMTP Authentication failed"**

**Solutions :**
1. Vérifier les identifiants SMTP
2. Utiliser un mot de passe d'application Gmail
3. Vérifier que "Accès moins sécurisé" est activé (Gmail)

### **Erreur : "Connection refused"**

**Solutions :**
1. Vérifier le port SMTP (587 pour Gmail)
2. Vérifier que TLS est activé
3. Vérifier les règles de firewall du VPS

### **Erreur : "Module not found"**

**Solution :**
```bash
# Vérifier que l'app notifications est dans INSTALLED_APPS
python manage.py shell
```

```python
from django.conf import settings
print('notifications' in settings.INSTALLED_APPS)
```

---

## 📋 **Checklist de Déploiement**

- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Templates initialisés (`python manage.py init_email_templates`)
- [ ] Paramètres SMTP configurés
- [ ] Test d'envoi réussi
- [ ] Templates visibles dans l'admin
- [ ] Service d'emails fonctionnel

---

## 🎉 **Résultat Final**

Après ces étapes, vous devriez avoir :

✅ **6 templates d'emails** créés et actifs
✅ **Service d'emails** configuré et fonctionnel  
✅ **Tests d'envoi** qui fonctionnent
✅ **Interface d'administration** accessible
✅ **Système complet** opérationnel

**Votre système d'emails est maintenant déployé et fonctionnel sur le VPS !** 🚀📧

---

*Guide de déploiement - Version 1.0*
*Pour ecom_maillot - Déploiement VPS*
