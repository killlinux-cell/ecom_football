# 🔧 **GUIDE CORRECTION ADMIN PRODUIT - VPS**

## ✅ **Problème Résolu**

**Erreur identifiée :** `AttributeError: 'Product' object has no attribute 'stock'`
- **Localisation :** `/django-admin/products/product/11/change/`
- **Cause :** Le signal `send_stock_alert_email` utilisait `product.stock` au lieu de `product.stock_quantity`
- **Impact :** Impossible d'éditer les produits dans l'admin Django
- **Solution :** Correction du signal et de la sérialisation JSON

---

## 🔧 **Modifications Apportées**

### **1. Signal de Stock**

**Fichier modifié :** `notifications/signals.py`

**Correction :**
```python
# AVANT (❌ Erreur)
if (old_instance.stock > 5 and instance.stock <= 5):
    get_email_service().send_stock_alert(instance, instance.stock)

# APRÈS (✅ Corrigé)
if (old_instance.stock_quantity > 5 and instance.stock_quantity <= 5):
    get_email_service().send_stock_alert(instance, instance.stock_quantity)
```

### **2. Service Email**

**Fichier modifié :** `notifications/email_service.py`

**Correction de la sérialisation JSON :**
```python
# AVANT (❌ Erreur de sérialisation)
email_data = {
    'product': product,  # Objet Django non sérialisable
    'current_stock': current_stock,
    'admin_name': f"{admin.first_name} {admin.last_name}".strip(),
}

# APRÈS (✅ Données sérialisables)
email_data = {
    'product_name': product.name,
    'product_price': float(product.price),
    'product_category': product.category.name if product.category else '',
    'current_stock': current_stock,
    'admin_name': f"{admin.first_name} {admin.last_name}".strip(),
}
```

### **3. Script de Test**

**Fichier créé :** `test_admin_product_edit.py`
- ✅ Test d'édition de stock de produit
- ✅ Test de création de produit
- ✅ Vérification des signals
- ✅ Validation de l'envoi d'emails

---

## 🚀 **DÉPLOIEMENT SUR VPS**

### **Étape 1 : Préparation**

```bash
# Se connecter au VPS
ssh root@votre-vps-ip
cd /var/www/ecom_football
source venv/bin/activate

# Sauvegarder la base de données
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
```

### **Étape 2 : Arrêter le Serveur**

```bash
# Arrêter Gunicorn
sudo systemctl stop gunicorn

# Vérifier qu'il est arrêté
sudo systemctl status gunicorn
```

### **Étape 3 : Appliquer les Modifications**

```bash
# Option A: Via Git (si vous utilisez Git)
git pull origin main

# Option B: Copier les fichiers manuellement
# Copier les fichiers modifiés :
# - notifications/signals.py
# - notifications/email_service.py
```

### **Étape 4 : Tester la Correction**

```bash
# Copier le script de test
# (Copier test_admin_product_edit.py sur le VPS)

# Exécuter le test
python test_admin_product_edit.py
```

### **Étape 5 : Redémarrer le Serveur**

```bash
# Redémarrer Gunicorn
sudo systemctl start gunicorn

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### **Étape 6 : Vérification**

```bash
# Vérifier que le site fonctionne
curl -I https://orapide.shop/

# Vérifier les logs
sudo journalctl -u gunicorn -f
```

---

## 🧪 **TESTS POST-DÉPLOIEMENT**

### **Test 1 : Édition de Produit dans l'Admin**

1. Aller sur https://orapide.shop/django-admin/
2. Se connecter avec un compte admin
3. Aller dans **Products > Products**
4. Cliquer sur un produit existant
5. Modifier le stock (ex: de 10 à 3)
6. Sauvegarder
7. ✅ **Vérifier :** Pas d'erreur `AttributeError`

### **Test 2 : Création de Nouveau Produit**

1. Dans l'admin Django
2. Cliquer sur **Add Product**
3. Remplir les champs obligatoires
4. Définir un stock faible (≤ 5)
5. Sauvegarder
6. ✅ **Vérifier :** Produit créé sans erreur

### **Test 3 : Alerte de Stock**

1. Modifier le stock d'un produit pour qu'il soit ≤ 5
2. ✅ **Vérifier :** Email d'alerte envoyé aux admins
3. ✅ **Vérifier :** Pas d'erreur de sérialisation JSON

---

## 📋 **VÉRIFICATIONS**

### **Avant Correction :**
- ❌ Erreur : `AttributeError: 'Product' object has no attribute 'stock'`
- ❌ Impossible d'éditer les produits dans l'admin
- ❌ Erreur de sérialisation JSON dans les emails

### **Après Correction :**
- ✅ Édition de produit fonctionnelle
- ✅ Signals de stock opérationnels
- ✅ Emails d'alerte envoyés correctement
- ✅ Pas d'erreur de sérialisation

---

## 🔍 **COMMANDES DE DIAGNOSTIC**

### **Vérifier les Signals :**

```bash
python manage.py shell -c "
from notifications.signals import send_stock_alert_email
from products.models import Product
print('Signal de stock chargé correctement')
"
```

### **Vérifier les Produits :**

```bash
python manage.py shell -c "
from products.models import Product
for product in Product.objects.all()[:5]:
    print(f'Produit: {product.name} - Stock: {product.stock_quantity}')
"
```

### **Tester l'Édition :**

```bash
python manage.py shell -c "
from products.models import Product
product = Product.objects.first()
if product:
    print(f'Stock avant: {product.stock_quantity}')
    product.stock_quantity = 3
    product.save()
    print(f'Stock après: {product.stock_quantity}')
    print('✅ Édition réussie')
"
```

---

## 🚨 **EN CAS DE PROBLÈME**

### **Problème 1 : Erreur Persistante**

```bash
# Vérifier les imports
python manage.py shell -c "
from notifications.signals import *
from products.models import Product
print('Imports OK')
"
```

### **Problème 2 : Signal Ne Fonctionne Pas**

```bash
# Vérifier la configuration des signals
python manage.py shell -c "
from django.db.models.signals import pre_save
from notifications.signals import send_stock_alert_email
from products.models import Product
print('Signal connecté:', pre_save.has_listeners(Product))
"
```

### **Problème 3 : Emails Non Envoyés**

```bash
# Vérifier la configuration email
python manage.py shell -c "
from notifications.models import EmailSettings
settings = EmailSettings.objects.first()
if settings:
    print(f'Email configuré: {settings.smtp_host}')
else:
    print('Aucune configuration email trouvée')
"
```

---

## 📋 **CHECKLIST DE DÉPLOIEMENT**

- [ ] Sauvegarde de la base de données créée
- [ ] Serveur arrêté
- [ ] Fichiers modifiés appliqués
- [ ] Test de correction exécuté
- [ ] Serveur redémarré
- [ ] Site accessible
- [ ] Admin Django accessible
- [ ] Édition de produit testée
- [ ] Création de produit testée
- [ ] Alerte de stock testée

---

## 🎯 **RÉSULTAT ATTENDU**

### **✅ Après Déploiement :**

1. **Admin Fonctionnel :** Édition de produits sans erreur
2. **Signals Opérationnels :** Alertes de stock automatiques
3. **Emails Corrects :** Envoi sans erreur de sérialisation
4. **Interface Stable :** Plus d'erreur `AttributeError`

### **📊 Exemple de Fonctionnement :**

**Avant :**
- ❌ Erreur lors de l'édition de produit
- ❌ `AttributeError: 'Product' object has no attribute 'stock'`

**Après :**
- ✅ Édition de produit réussie
- ✅ Stock modifié de 10 à 3
- ✅ Email d'alerte envoyé aux admins
- ✅ Signal exécuté sans erreur

---

## 🎉 **CONCLUSION**

**Le problème d'édition de produit dans l'admin est maintenant résolu !**

### **Impact :**
- 🎯 **Admin fonctionnel** pour la gestion des produits
- 📧 **Alertes automatiques** de stock faible
- 🔧 **Signals opérationnels** et fiables
- 📊 **Interface stable** sans erreurs

**Vous pouvez maintenant éditer vos produits dans l'admin Django !** 🎊

---

*Guide de déploiement créé le 05/09/2025 - Version 1.0*
*Correction admin produit - Prêt pour production*
