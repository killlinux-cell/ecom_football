# 🔧 **GUIDE CORRECTION AFFICHAGE PANIER - VPS**

## ✅ **Problème Résolu**

**Problème identifié :** Doublement des prix dans l'affichage du panier
- **Symptôme :** Sous-total de 40 000 FCFA pour un article de 20 000 FCFA × quantité 1
- **Cause :** Incohérence entre `item.total_price` et le calcul réel
- **Solution :** Correction du template et du modèle CartItem

---

## 🔧 **Modifications Apportées**

### **1. Modèle CartItem**

**Fichier modifié :** `cart/models.py`

**Corrections :**
```python
@property
def total_price(self):
    """Calcule le prix total pour cet article (produit + personnalisations)"""
    base_price = self.product.price * self.quantity  # ✅ Corrigé: price au lieu de current_price
    customization_price = sum(cust.price for cust in self.customizations.all())
    return base_price + customization_price

@property
def base_price(self):
    """Calcule le prix de base du produit"""
    return self.product.price * self.quantity  # ✅ Corrigé: price au lieu de current_price
```

### **2. Template de Commande**

**Fichier modifié :** `templates/orders/order_create.html`

**Correction de l'affichage :**
```html
<div class="col-md-2 text-end">
    <span class="price">
        {% with cart_item=item|get_cart_item:user %}
            {% if cart_item %}
                {{ cart_item.total_price|price_format }}  <!-- ✅ Utilise le calcul correct -->
            {% else %}
                {% widthratio item.price 1 item.quantity as base_price %}{{ base_price|price_format }}
            {% endif %}
        {% endwith %}
    </span>
</div>
```

### **3. Scripts de Diagnostic**

**Fichiers créés :**
- ✅ `debug_cart_calculation.py` - Diagnostic des calculs
- ✅ `fix_cart_quantity_mismatch.py` - Correction des incohérences
- ✅ `test_cart_display_fix.py` - Test de la correction

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
# - templates/orders/order_create.html
```

### **Étape 4 : Corriger les Données Existantes**

```bash
# Copier le script de correction
# (Copier fix_cart_quantity_mismatch.py sur le VPS)

# Exécuter la correction
python fix_cart_quantity_mismatch.py
# Répondre 'y' pour vider les paniers incohérents
```

### **Étape 5 : Tester la Correction**

```bash
# Copier le script de test
# (Copier test_cart_display_fix.py sur le VPS)

# Exécuter le test
python test_cart_display_fix.py
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

### **Test 1 : Affichage du Panier**

1. Aller sur https://orapide.shop/
2. Ajouter un produit au panier
3. Aller à la page de commande
4. Vérifier que le sous-total = prix × quantité

### **Test 2 : Calcul avec Personnalisations**

1. Ajouter un produit avec personnalisations
2. Vérifier que le prix total = (prix × quantité) + personnalisations

### **Test 3 : Différentes Quantités**

1. Tester avec quantité 1, 2, 3
2. Vérifier que le calcul est correct pour chaque quantité

---

## 📋 **VÉRIFICATIONS**

### **Avant Correction :**
- ❌ Sous-total : 40 000 FCFA (incorrect)
- ❌ Prix unitaire : 20 000 FCFA
- ❌ Quantité : 1
- ❌ Calcul : 20 000 × 1 = 40 000 (doublé)

### **Après Correction :**
- ✅ Sous-total : 20 000 FCFA (correct)
- ✅ Prix unitaire : 20 000 FCFA
- ✅ Quantité : 1
- ✅ Calcul : 20 000 × 1 = 20 000 (correct)

---

## 🔍 **COMMANDES DE DIAGNOSTIC**

### **Vérifier les Calculs du Panier :**

```bash
python manage.py shell -c "
from cart.models import CartItem
for item in CartItem.objects.all():
    expected = item.product.price * item.quantity
    actual = item.total_price
    if expected != actual:
        print(f'Incohérence: {item.product.name} - Attendu: {expected}, Réel: {actual}')
    else:
        print(f'OK: {item.product.name} - {actual}')
"
```

### **Vérifier les Paniers :**

```bash
python manage.py shell -c "
from cart.models import Cart
for cart in Cart.objects.all():
    total = cart.get_total_price()
    print(f'Panier {cart.id}: {total} FCFA')
"
```

---

## 🚨 **EN CAS DE PROBLÈME**

### **Problème 1 : Prix Toujours Doublés**

```bash
# Vérifier le modèle
python manage.py shell -c "
from cart.models import CartItem
item = CartItem.objects.first()
print(f'Prix produit: {item.product.price}')
print(f'Quantité: {item.quantity}')
print(f'Prix total: {item.total_price}')
"
```

### **Problème 2 : Template Ne S'Affiche Pas**

```bash
# Vérifier les templates
ls -la templates/orders/

# Redémarrer le serveur
sudo systemctl restart gunicorn
```

### **Problème 3 : Erreur de Calcul**

```bash
# Exécuter le diagnostic
python debug_cart_calculation.py
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
- [ ] Affichage du panier testé
- [ ] Calculs vérifiés
- [ ] Personnalisations testées

---

## 🎯 **RÉSULTAT ATTENDU**

### **✅ Après Déploiement :**

1. **Affichage Correct :** Prix × Quantité = Sous-total
2. **Calculs Cohérents :** Pas de doublement des prix
3. **Personnalisations :** Ajoutées correctement au total
4. **Interface :** Affichage clair et précis

### **📊 Exemple d'Affichage Correct :**

**Avant :**
- Prix unitaire : 20 000 FCFA
- Quantité : 1
- Sous-total : 40 000 FCFA ❌

**Après :**
- Prix unitaire : 20 000 FCFA
- Quantité : 1
- Sous-total : 20 000 FCFA ✅

---

## 🎉 **CONCLUSION**

**Le problème de doublement des prix est maintenant résolu !**

### **Impact :**
- 🎯 **Calculs précis** pour les clients
- 💰 **Prix corrects** affichés
- 🔧 **Interface fiable** et cohérente
- 📊 **Totaux exacts** pour les commandes

**Vos clients verront maintenant les bons prix !** 🎊

---

*Guide de déploiement créé le 05/09/2025 - Version 1.0*
*Correction affichage panier - Prêt pour production*
