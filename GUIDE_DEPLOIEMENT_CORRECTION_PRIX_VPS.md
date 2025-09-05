# 🚀 **GUIDE DE DÉPLOIEMENT - CORRECTION PRIX DOUBLÉS VPS**

## ❌ **Problème Identifié**

**Incohérence observée :**
- **Prix unitaire** : 8 000 FCFA
- **Quantité** : 1
- **Personnalisations** : Aucune
- **Total de l'article** : **16 000 FCFA** (doublé !)

**Cause :** Double comptage des personnalisations lors de la création des articles de commande.

---

## ✅ **Corrections Implémentées**

### **1. Correction du Modèle OrderItem**

**Fichier modifié :** `orders/models.py`

**Ajout de la méthode :**
```python
def get_total_with_customizations(self):
    """Calcule le prix total avec personnalisations"""
    base_price = self.price * self.quantity
    customization_price = sum(cust.price for cust in self.customizations.all())
    return base_price + customization_price
```

### **2. Correction de la Logique de Création**

**Fichier modifié :** `orders/views.py`

**Changements :**
- Création de l'OrderItem avec le prix de base seulement
- Ajout des personnalisations séparément
- Recalcul du total avec personnalisations

### **3. Scripts de Test et Correction**

**Scripts créés :**
- `test_price_fix.py` - Test de la correction
- `fix_doubled_prices.py` - Correction des commandes existantes

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
# Copier orders/models.py et orders/views.py modifiés
```

### **Étape 4 : Corriger les Commandes Existantes**

```bash
# Exécuter le script de correction
python fix_doubled_prices.py
```

### **Étape 5 : Tester la Correction**

```bash
# Exécuter le test
python test_price_fix.py
```

### **Étape 6 : Redémarrer le Serveur**

```bash
# Redémarrer Gunicorn
sudo systemctl start gunicorn

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### **Étape 7 : Vérification**

```bash
# Vérifier que le site fonctionne
curl -I https://orapide.shop/

# Vérifier les logs
sudo journalctl -u gunicorn -f
```

---

## 🧪 **TESTS POST-DÉPLOIEMENT**

### **Test 1 : Création de Commande**

1. Aller sur https://orapide.shop/
2. Ajouter un produit au panier
3. Créer une commande
4. Vérifier que les prix sont cohérents

### **Test 2 : Commande avec Personnalisations**

1. Ajouter un produit avec personnalisations
2. Créer une commande
3. Vérifier que le total = prix de base + personnalisations

### **Test 3 : Vérification Admin**

1. Aller sur https://orapide.shop/admin/
2. Vérifier les commandes existantes
3. S'assurer que les totaux sont corrects

---

## 🔧 **COMMANDES DE DIAGNOSTIC**

### **Vérifier les Commandes Problématiques :**

```bash
python manage.py shell -c "
from orders.models import Order, OrderItem
for order in Order.objects.all():
    for item in order.items.all():
        expected = item.price * item.quantity
        if item.total_price != expected:
            print(f'Commande {order.order_number}: {item.product_name} - Prix: {item.price}, Total: {item.total_price}, Attendu: {expected}')
"
```

### **Vérifier les Personnalisations :**

```bash
python manage.py shell -c "
from orders.models import OrderItemCustomization
customs = OrderItemCustomization.objects.all()
print(f'Personnalisations: {customs.count()}')
for custom in customs:
    print(f'- {custom.order_item.product_name}: {custom.price} FCFA')
"
```

---

## 🚨 **EN CAS DE PROBLÈME**

### **Problème 1 : Erreur lors du Déploiement**

```bash
# Restaurer la sauvegarde
cp db.sqlite3.backup.* db.sqlite3

# Redémarrer le serveur
sudo systemctl restart gunicorn
```

### **Problème 2 : Prix Toujours Doublés**

```bash
# Exécuter la correction manuelle
python manage.py shell -c "
from orders.models import OrderItem
for item in OrderItem.objects.all():
    if item.total_price == item.price * item.quantity * 2:
        item.total_price = item.price * item.quantity
        item.save()
        print(f'Corrigé: {item.product_name}')
"
```

### **Problème 3 : Site Ne Fonctionne Plus**

```bash
# Vérifier les logs
sudo journalctl -u gunicorn -n 50

# Redémarrer les services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 📋 **CHECKLIST DE DÉPLOIEMENT**

- [ ] Sauvegarde de la base de données créée
- [ ] Serveur arrêté
- [ ] Fichiers modifiés appliqués
- [ ] Script de correction exécuté
- [ ] Test de correction réussi
- [ ] Serveur redémarré
- [ ] Site accessible
- [ ] Création de commande testée
- [ ] Prix cohérents vérifiés
- [ ] Logs propres

---

## 🎯 **RÉSULTAT ATTENDU**

### **✅ Après Déploiement :**

1. **Prix cohérents** : 8 000 FCFA × 1 = 8 000 FCFA
2. **Personnalisations correctes** : Prix de base + personnalisations
3. **Commandes fonctionnelles** sans erreur
4. **Totaux précis** dans l'admin

### **📊 Exemple de Correction :**

**Avant :**
- Prix unitaire : 8 000 FCFA
- Total : 16 000 FCFA ❌

**Après :**
- Prix unitaire : 8 000 FCFA
- Total : 8 000 FCFA ✅

---

## 🎉 **CONCLUSION**

**La correction des prix doublés est prête pour le déploiement !**

### **Impact :**
- 🚀 **Prix cohérents** dans toutes les commandes
- 💰 **Calculs précis** des totaux
- 🔧 **Logique corrigée** pour les personnalisations
- 🛡️ **Prévention** des erreurs futures

**Votre système de commandes sera parfaitement cohérent !** 🎊

---

*Guide de déploiement créé le 05/09/2025 - Version 1.0*
*Correction des prix doublés - Prêt pour production*
