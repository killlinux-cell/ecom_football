# 💰 **GUIDE PAIEMENT À LA LIVRAISON - VPS**

## ✅ **Fonctionnalité Ajoutée**

**Nouvelle option de paiement :** Paiement à la livraison
- Les clients peuvent choisir de payer en espèces lors de la réception
- L'admin peut marquer les commandes comme payées après réception
- Gestion complète du statut de paiement

---

## 🔧 **Modifications Apportées**

### **1. Modèle Order**

**Fichier modifié :** `orders/models.py`

**Ajouts :**
```python
PAYMENT_METHOD_CHOICES = [
    ('paydunya', 'PayDunya'),
    ('wave_direct', 'Wave Direct'),
    ('cash_on_delivery', 'Paiement à la livraison'),
]

PAYMENT_STATUS_CHOICES = [
    ('pending', 'En attente'),
    ('paid', 'Payé'),
    ('failed', 'Échoué'),
    ('refunded', 'Remboursé'),
    ('cash_on_delivery', 'Paiement à la livraison'),
]
```

### **2. Formulaire de Commande**

**Fichier modifié :** `orders/forms.py`

**Ajout de l'option :**
```python
payment_method = forms.ChoiceField(
    choices=[
        ('paydunya', 'PayDunya (Carte bancaire)'),
        ('wave_direct', 'Wave Direct'),
        ('cash_on_delivery', 'Paiement à la livraison'),
    ],
    widget=forms.RadioSelect,
    initial='paydunya',
    label='Méthode de paiement'
)
```

### **3. Logique de Traitement**

**Fichier modifié :** `orders/views.py`

**Gestion du paiement à la livraison :**
```python
elif payment_method == 'cash_on_delivery':
    order.payment_status = 'cash_on_delivery'
    order.save()
    messages.info(request, "Votre commande sera payée lors de la livraison.")
    return redirect('orders:order_detail', order_id=order.id)
```

### **4. Interface Utilisateur**

**Fichiers modifiés :**
- `templates/orders/order_create.html` - Option de paiement
- `templates/orders/order_detail.html` - Affichage du statut

### **5. Fonctionnalité Admin**

**Nouvelle vue :** `mark_cash_payment_received`
- Permet à l'admin de marquer les commandes comme payées
- Envoie automatiquement un email de confirmation

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
# - orders/models.py
# - orders/forms.py
# - orders/views.py
# - orders/urls.py
# - templates/orders/order_create.html
# - templates/orders/order_detail.html
```

### **Étape 4 : Appliquer les Migrations**

```bash
# Appliquer les migrations
python manage.py migrate

# Vérifier les migrations
python manage.py showmigrations orders
```

### **Étape 5 : Tester la Fonctionnalité**

```bash
# Exécuter le test
python test_cash_on_delivery.py
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

### **Test 1 : Création de Commande avec Paiement à la Livraison**

1. Aller sur https://orapide.shop/
2. Ajouter un produit au panier
3. Aller à la page de commande
4. Sélectionner "Paiement à la livraison"
5. Créer la commande
6. Vérifier que le statut est "Paiement à la livraison"

### **Test 2 : Gestion Admin**

1. Aller sur https://orapide.shop/admin/
2. Voir la commande créée
3. Vérifier que le statut est correct
4. Marquer comme payée (si admin)

### **Test 3 : Interface Utilisateur**

1. Vérifier que l'option de paiement s'affiche
2. Vérifier que le statut s'affiche correctement
3. Vérifier que les messages sont appropriés

---

## 📋 **FONCTIONNALITÉS DISPONIBLES**

### **Pour les Clients :**

1. **Choix de Paiement :**
   - PayDunya (Carte bancaire)
   - Wave Direct
   - **Paiement à la livraison** ✅

2. **Processus de Commande :**
   - Sélection de la méthode de paiement
   - Création de commande sans paiement immédiat
   - Confirmation avec message explicatif

3. **Suivi de Commande :**
   - Statut "Paiement à la livraison" visible
   - Informations claires sur le processus

### **Pour l'Admin :**

1. **Gestion des Commandes :**
   - Voir les commandes en attente de paiement
   - Marquer comme payées après réception
   - Envoi automatique d'email de confirmation

2. **Interface Admin :**
   - Bouton "Marquer comme payé" sur les commandes
   - Statuts clairs et distincts
   - Historique des paiements

---

## 🔍 **COMMANDES DE DIAGNOSTIC**

### **Vérifier les Commandes avec Paiement à la Livraison :**

```bash
python manage.py shell -c "
from orders.models import Order
cash_orders = Order.objects.filter(payment_method='cash_on_delivery')
print(f'Commandes paiement à la livraison: {cash_orders.count()}')
for order in cash_orders:
    print(f'- {order.order_number}: {order.get_payment_status_display()}')
"
```

### **Vérifier les Statuts de Paiement :**

```bash
python manage.py shell -c "
from orders.models import Order
from collections import Counter
statuses = Counter(order.payment_status for order in Order.objects.all())
for status, count in statuses.items():
    print(f'{status}: {count}')
"
```

---

## 🚨 **EN CAS DE PROBLÈME**

### **Problème 1 : Migration Échoue**

```bash
# Vérifier les migrations
python manage.py showmigrations orders

# Forcer la migration
python manage.py migrate orders --fake-initial
```

### **Problème 2 : Option de Paiement Ne S'Affiche Pas**

```bash
# Vérifier les templates
ls -la templates/orders/

# Redémarrer le serveur
sudo systemctl restart gunicorn
```

### **Problème 3 : Erreur de Statut**

```bash
# Vérifier les choix dans le modèle
python manage.py shell -c "
from orders.models import Order
print('Méthodes:', Order.PAYMENT_METHOD_CHOICES)
print('Statuts:', Order.PAYMENT_STATUS_CHOICES)
"
```

---

## 📋 **CHECKLIST DE DÉPLOIEMENT**

- [ ] Sauvegarde de la base de données créée
- [ ] Serveur arrêté
- [ ] Fichiers modifiés appliqués
- [ ] Migrations appliquées
- [ ] Test de fonctionnalité réussi
- [ ] Serveur redémarré
- [ ] Site accessible
- [ ] Option de paiement visible
- [ ] Création de commande testée
- [ ] Gestion admin testée

---

## 🎯 **RÉSULTAT ATTENDU**

### **✅ Après Déploiement :**

1. **Option de Paiement :** Visible dans le formulaire de commande
2. **Processus de Commande :** Fonctionne sans paiement immédiat
3. **Statut de Commande :** "Paiement à la livraison" affiché
4. **Gestion Admin :** Bouton pour marquer comme payé
5. **Emails :** Confirmation envoyée après paiement

### **📊 Exemple d'Utilisation :**

**Client :**
1. Sélectionne "Paiement à la livraison"
2. Crée la commande
3. Reçoit confirmation
4. Paye à la livraison

**Admin :**
1. Voit la commande en attente
2. Livre la commande
3. Reçoit le paiement
4. Marque comme payé
5. Client reçoit confirmation

---

## 🎉 **CONCLUSION**

**Le système de paiement à la livraison est maintenant disponible !**

### **Impact :**
- 🚀 **Flexibilité** pour les clients
- 💰 **Plus d'options** de paiement
- 🔧 **Gestion simplifiée** pour l'admin
- 📧 **Notifications automatiques**
- 🛡️ **Processus sécurisé**

**Vos clients peuvent maintenant payer à la livraison !** 🎊

---

*Guide de déploiement créé le 05/09/2025 - Version 1.0*
*Paiement à la livraison - Prêt pour production*
