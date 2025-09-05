# 🔧 **GUIDE CORRECTION PRIX PROMOTIONNELS - VPS**

## ✅ **Problème Résolu**

**Problème identifié :** Les prix promotionnels n'étaient pas appliqués lors du paiement
- **Symptôme :** Un produit en promotion (15 000 → 10 000 FCFA) utilisait le prix normal (15 000 FCFA) au lieu du prix promotion (10 000 FCFA)
- **Cause :** Le système utilisait `product.price` au lieu de `product.current_price`
- **Impact :** Les clients payaient le prix normal même avec une promotion active
- **Solution :** Correction des modèles et vues pour utiliser les prix promotionnels

---

## 🔧 **Modifications Apportées**

### **1. Modèle CartItem**

**Fichier modifié :** `cart/models.py`

**Corrections :**
```python
# AVANT (❌ Prix normal)
@property
def total_price(self):
    base_price = self.product.price * self.quantity  # Prix normal
    customization_price = sum(cust.price for cust in self.customizations.all())
    return base_price + customization_price

@property
def base_price(self):
    return self.product.price * self.quantity  # Prix normal

# APRÈS (✅ Prix promotion)
@property
def total_price(self):
    base_price = self.product.current_price * self.quantity  # Prix promotion
    customization_price = sum(cust.price for cust in self.customizations.all())
    return base_price + customization_price

@property
def base_price(self):
    return self.product.current_price * self.quantity  # Prix promotion
```

### **2. Vue de Commande**

**Fichier modifié :** `orders/views.py`

**Correction :**
```python
# AVANT (❌ Prix obsolète du panier)
order_item = OrderItem.objects.create(
    order=order,
    product=item['product'],
    product_name=item['product'].name,
    size=item['size'],
    quantity=item['quantity'],
    price=item['price'],  # Prix obsolète du panier session
    total_price=base_price
)

# APRÈS (✅ Prix actuel avec promotion)
current_price = item['product'].current_price  # Prix promotion si applicable
base_price = current_price * item['quantity']

order_item = OrderItem.objects.create(
    order=order,
    product=item['product'],
    product_name=item['product'].name,
    size=item['size'],
    quantity=item['quantity'],
    price=current_price,  # Prix actuel (promotion)
    total_price=base_price
)
```

### **3. Modèle Product**

**Fichier vérifié :** `products/models.py`

**Propriété existante (correcte) :**
```python
@property
def current_price(self):
    """Retourne le prix actuel (promotion ou prix normal)"""
    return self.sale_price if self.sale_price else self.price
```

### **4. Scripts de Test**

**Fichiers créés :**
- ✅ `test_simple_promotional_pricing.py` - Test des prix promotionnels
- ✅ `test_order_promotional_pricing.py` - Test des commandes avec promotion

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
# - cart/models.py
# - orders/views.py
```

### **Étape 4 : Tester la Correction**

```bash
# Copier les scripts de test
# (Copier test_simple_promotional_pricing.py et test_order_promotional_pricing.py sur le VPS)

# Exécuter les tests
python test_simple_promotional_pricing.py
python test_order_promotional_pricing.py
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

### **Test 1 : Produit avec Promotion**

1. Aller sur https://orapide.shop/
2. Trouver un produit avec promotion (prix barré)
3. Ajouter au panier
4. Aller à la page de commande
5. ✅ **Vérifier :** Le prix affiché est le prix promotion

### **Test 2 : Commande avec Promotion**

1. Créer une commande avec un produit en promotion
2. Procéder au paiement
3. ✅ **Vérifier :** Le montant à payer correspond au prix promotion

### **Test 3 : Calcul des Totaux**

1. Commander un produit en promotion (ex: 15 000 → 10 000 FCFA)
2. Quantité 2 + livraison 1 000 FCFA
3. ✅ **Vérifier :** Total = (10 000 × 2) + 1 000 = 21 000 FCFA

---

## 📋 **VÉRIFICATIONS**

### **Avant Correction :**
- ❌ Prix normal : 15 000 FCFA (même avec promotion)
- ❌ Total incorrect : (15 000 × 2) + 1 000 = 31 000 FCFA
- ❌ Client paye le prix normal

### **Après Correction :**
- ✅ Prix promotion : 10 000 FCFA (promotion appliquée)
- ✅ Total correct : (10 000 × 2) + 1 000 = 21 000 FCFA
- ✅ Client paye le prix promotion

---

## 🔍 **COMMANDES DE DIAGNOSTIC**

### **Vérifier les Prix Promotionnels :**

```bash
python manage.py shell -c "
from products.models import Product
for product in Product.objects.filter(sale_price__isnull=False):
    print(f'Produit: {product.name}')
    print(f'  Prix normal: {product.price} FCFA')
    print(f'  Prix promotion: {product.sale_price} FCFA')
    print(f'  Prix actuel: {product.current_price} FCFA')
    print()
"
```

### **Vérifier les Paniers :**

```bash
python manage.py shell -c "
from cart.models import CartItem
for item in CartItem.objects.all():
    print(f'Panier: {item.product.name}')
    print(f'  Prix unitaire: {item.product.current_price} FCFA')
    print(f'  Prix total: {item.total_price} FCFA')
    print()
"
```

### **Vérifier les Commandes :**

```bash
python manage.py shell -c "
from orders.models import OrderItem
for item in OrderItem.objects.all():
    print(f'Commande: {item.product_name}')
    print(f'  Prix unitaire: {item.price} FCFA')
    print(f'  Prix total: {item.total_price} FCFA')
    print()
"
```

---

## 🚨 **EN CAS DE PROBLÈME**

### **Problème 1 : Prix Toujours Normaux**

```bash
# Vérifier la propriété current_price
python manage.py shell -c "
from products.models import Product
product = Product.objects.filter(sale_price__isnull=False).first()
if product:
    print(f'Prix normal: {product.price}')
    print(f'Prix promotion: {product.sale_price}')
    print(f'Prix actuel: {product.current_price}')
"
```

### **Problème 2 : Panier Utilise Mauvais Prix**

```bash
# Vérifier le calcul du panier
python manage.py shell -c "
from cart.models import CartItem
item = CartItem.objects.first()
if item:
    print(f'Prix produit: {item.product.current_price}')
    print(f'Prix panier: {item.base_price}')
    print(f'Calcul: {item.product.current_price} × {item.quantity}')
"
```

### **Problème 3 : Commande Utilise Mauvais Prix**

```bash
# Vérifier les commandes
python manage.py shell -c "
from orders.models import OrderItem
item = OrderItem.objects.first()
if item:
    print(f'Prix produit: {item.product.current_price}')
    print(f'Prix commande: {item.price}')
    print(f'Cohérent: {item.price == item.product.current_price}')
"
```

---

## 📋 **CHECKLIST DE DÉPLOIEMENT**

- [ ] Sauvegarde de la base de données créée
- [ ] Serveur arrêté
- [ ] Fichiers modifiés appliqués
- [ ] Tests de correction exécutés
- [ ] Serveur redémarré
- [ ] Site accessible
- [ ] Produit avec promotion testé
- [ ] Commande avec promotion testée
- [ ] Calculs de totaux vérifiés
- [ ] Paiement avec promotion testé

---

## 🎯 **RÉSULTAT ATTENDU**

### **✅ Après Déploiement :**

1. **Prix Promotionnels :** Appliqués automatiquement
2. **Calculs Corrects :** Totaux basés sur les prix promotionnels
3. **Paiements Justes :** Clients paient le prix promotion
4. **Interface Cohérente :** Affichage et calculs alignés

### **📊 Exemple de Fonctionnement :**

**Avant :**
- Prix normal : 15 000 FCFA
- Prix promotion : 10 000 FCFA
- Prix payé : 15 000 FCFA ❌

**Après :**
- Prix normal : 15 000 FCFA
- Prix promotion : 10 000 FCFA
- Prix payé : 10 000 FCFA ✅

---

## 🎉 **CONCLUSION**

**Le problème des prix promotionnels est maintenant résolu !**

### **Impact :**
- 🎯 **Prix justes** pour les clients
- 💰 **Promotions respectées** automatiquement
- 🔧 **Calculs précis** et cohérents
- 📊 **Interface fiable** et transparente

**Vos clients bénéficient maintenant des vraies promotions !** 🎊

---

*Guide de déploiement créé le 05/09/2025 - Version 1.0*
*Correction prix promotionnels - Prêt pour production*
