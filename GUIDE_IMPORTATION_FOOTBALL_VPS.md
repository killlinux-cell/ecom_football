# ⚽ **GUIDE IMPORTATION ÉQUIPES FOOTBALL - VPS**

## 🎯 **Objectif**

Ce guide vous permet d'importer automatiquement toutes les équipes des 5 grands championnats européens et de créer des produits de maillots correspondants.

### **Championnats Inclus :**
- 🏆 **Ligue 1** (France) - 20 équipes
- 🏆 **La Liga** (Espagne) - 20 équipes  
- 🏆 **Bundesliga** (Allemagne) - 18 équipes
- 🏆 **Serie A** (Italie) - 20 équipes
- 🏆 **Premier League** (Angleterre) - 20 équipes

**Total : 98 équipes de football professionnel**

---

## 📋 **Scripts Disponibles**

### **1. `import_football_teams.py`**
- ✅ Importe toutes les équipes des 5 championnats
- ✅ Crée la catégorie "Maillots de Football"
- ✅ Gère les slugs et noms des équipes
- ✅ Évite les doublons

### **2. `create_football_products.py`**
- ✅ Crée des produits de maillots pour toutes les équipes
- ✅ Types : domicile, extérieur, troisième, gardien, vintage
- ✅ Prix réalistes (15 000 - 20 000 FCFA)
- ✅ Descriptions détaillées

### **3. `test_football_import.py`**
- ✅ Teste l'importation des équipes
- ✅ Vérifie la création des produits
- ✅ Contrôle l'intégrité de la base de données
- ✅ Teste la fonctionnalité du site web

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

# Vérifier l'espace disque
df -h
```

### **Étape 2 : Arrêter le Serveur**

```bash
# Arrêter Gunicorn
sudo systemctl stop gunicorn

# Vérifier qu'il est arrêté
sudo systemctl status gunicorn
```

### **Étape 3 : Copier les Scripts**

```bash
# Copier les scripts sur le VPS
# (Copier import_football_teams.py, create_football_products.py, test_football_import.py)

# Vérifier que les fichiers sont présents
ls -la *.py
```

### **Étape 4 : Exécuter l'Importation**

```bash
# Étape 4.1: Importer les équipes
python import_football_teams.py

# Répondre "o" aux questions
# Voulez-vous continuer ? (o/n): o
# Voulez-vous créer des produits d'exemple ? (o/n): o
```

```bash
# Étape 4.2: Créer tous les produits
python create_football_products.py

# Répondre "o" aux questions
# Voulez-vous continuer ? (o/n): o
# Voulez-vous créer des produits spéciaux ? (o/n): o
```

### **Étape 5 : Tester l'Importation**

```bash
# Exécuter les tests
python test_football_import.py

# Vérifier que tous les tests passent
# Résultat attendu: 5/5 tests réussis
```

### **Étape 6 : Collecter les Fichiers Statiques**

```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Vérifier que les fichiers sont collectés
ls -la staticfiles/
```

### **Étape 7 : Redémarrer le Serveur**

```bash
# Redémarrer Gunicorn
sudo systemctl start gunicorn

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### **Étape 8 : Vérification**

```bash
# Vérifier que le site fonctionne
curl -I https://orapide.shop/

# Vérifier les logs
sudo journalctl -u gunicorn -f
```

---

## 🧪 **TESTS POST-DÉPLOIEMENT**

### **Test 1 : Vérifier les Équipes**

1. Aller sur https://orapide.shop/
2. Naviguer vers la liste des produits
3. ✅ **Vérifier :** Plus de 90 équipes disponibles
4. ✅ **Vérifier :** Équipes des 5 championnats présentes

### **Test 2 : Vérifier les Produits**

1. Cliquer sur une équipe populaire (PSG, Real Madrid, etc.)
2. ✅ **Vérifier :** Plusieurs types de maillots disponibles
3. ✅ **Vérifier :** Prix affichés correctement
4. ✅ **Vérifier :** Descriptions détaillées

### **Test 3 : Vérifier la Navigation**

1. Tester les filtres par équipe
2. Tester les filtres par championnat
3. ✅ **Vérifier :** Navigation fluide
4. ✅ **Vérifier :** Résultats de recherche

### **Test 4 : Vérifier les Avis**

1. Se connecter avec un compte utilisateur
2. Aller sur la page d'un produit
3. ✅ **Vérifier :** Section "Avis clients" visible
4. ✅ **Vérifier :** Formulaire d'ajout d'avis fonctionnel

---

## 📊 **RÉSULTATS ATTENDUS**

### **Après Importation des Équipes :**
- ✅ **98 équipes** importées
- ✅ **5 championnats** représentés
- ✅ **Slugs uniques** pour chaque équipe
- ✅ **Informations complètes** (nom, pays, championnat)

### **Après Création des Produits :**
- ✅ **294 produits** créés (98 équipes × 3 types)
- ✅ **Produits spéciaux** pour équipes populaires
- ✅ **Prix réalistes** (12 000 - 20 000 FCFA)
- ✅ **Descriptions détaillées** pour chaque produit

### **Statistiques par Championnat :**
- 🏆 **Ligue 1 :** 20 équipes, ~60 produits
- 🏆 **La Liga :** 20 équipes, ~60 produits
- 🏆 **Bundesliga :** 18 équipes, ~54 produits
- 🏆 **Serie A :** 20 équipes, ~60 produits
- 🏆 **Premier League :** 20 équipes, ~60 produits

---

## 🔍 **COMMANDES DE DIAGNOSTIC**

### **Vérifier les Équipes Importées :**

```bash
python manage.py shell -c "
from products.models import Team
print('=== ÉQUIPES PAR CHAMPIONNAT ===')
for league in ['Ligue 1', 'La Liga', 'Bundesliga', 'Serie A', 'Premier League']:
    count = Team.objects.filter(league=league).count()
    print(f'{league}: {count} équipes')
print(f'\\nTotal: {Team.objects.count()} équipes')
"
```

### **Vérifier les Produits Créés :**

```bash
python manage.py shell -c "
from products.models import Product
print('=== PRODUITS PAR TYPE ===')
types = ['domicile', 'exterieur', 'troisieme', 'gardien', 'vintage']
for product_type in types:
    count = Product.objects.filter(slug__contains=product_type).count()
    print(f'{product_type}: {count} produits')
print(f'\\nTotal: {Product.objects.count()} produits')
"
```

### **Vérifier les Produits par Championnat :**

```bash
python manage.py shell -c "
from products.models import Product
print('=== PRODUITS PAR CHAMPIONNAT ===')
for league in ['Ligue 1', 'La Liga', 'Bundesliga', 'Serie A', 'Premier League']:
    count = Product.objects.filter(team__league=league).count()
    print(f'{league}: {count} produits')
"
```

### **Vérifier les Produits en Promotion :**

```bash
python manage.py shell -c "
from products.models import Product
promo_count = Product.objects.filter(sale_price__isnull=False).count()
total_count = Product.objects.count()
print(f'Produits en promotion: {promo_count}/{total_count}')
print(f'Pourcentage: {(promo_count/total_count)*100:.1f}%')
"
```

---

## 🚨 **EN CAS DE PROBLÈME**

### **Problème 1 : Erreur d'Importation**

```bash
# Vérifier les logs d'erreur
python import_football_teams.py 2>&1 | tee import_log.txt

# Vérifier la base de données
python manage.py shell -c "
from products.models import Team
print(f'Équipes actuelles: {Team.objects.count()}')
"
```

### **Problème 2 : Produits Non Créés**

```bash
# Vérifier les produits existants
python manage.py shell -c "
from products.models import Product
print(f'Produits actuels: {Product.objects.count()}')
"

# Relancer la création des produits
python create_football_products.py
```

### **Problème 3 : Erreur de Template**

```bash
# Vérifier la syntaxe
python manage.py check

# Vérifier les logs du serveur
sudo journalctl -u gunicorn -f
```

### **Problème 4 : Fichiers Statiques**

```bash
# Vérifier la collecte
python manage.py collectstatic --noinput

# Vérifier les permissions
sudo chown -R www-data:www-data staticfiles/
```

---

## 📋 **CHECKLIST DE DÉPLOIEMENT**

- [ ] Sauvegarde de la base de données créée
- [ ] Serveur arrêté
- [ ] Scripts copiés sur le VPS
- [ ] Importation des équipes exécutée
- [ ] Création des produits exécutée
- [ ] Tests d'importation passés
- [ ] Fichiers statiques collectés
- [ ] Serveur redémarré
- [ ] Site accessible
- [ ] Équipes visibles sur le site
- [ ] Produits visibles sur le site
- [ ] Navigation fonctionnelle
- [ ] Avis fonctionnels

---

## 🎯 **ÉTAPES SUIVANTES**

### **Après l'Importation :**

1. **Ajouter les Images :**
   - Télécharger les images des équipes
   - Ajouter les images des produits
   - Optimiser les images pour le web

2. **Personnaliser les Produits :**
   - Ajuster les prix si nécessaire
   - Modifier les descriptions
   - Ajouter des produits spéciaux

3. **Configurer les Promotions :**
   - Mettre en place des offres spéciales
   - Configurer les réductions
   - Créer des bundles

4. **Optimiser le SEO :**
   - Ajouter des meta descriptions
   - Optimiser les titres
   - Configurer les URLs

---

## 🎉 **CONCLUSION**

**L'importation des équipes de football est maintenant complète !**

### **Impact :**
- 🌟 **Catalogue complet** avec 98 équipes
- 🛍️ **294 produits** de maillots
- 🏆 **5 championnats** européens représentés
- 💰 **Prix réalistes** pour le marché ivoirien
- 📱 **Interface moderne** avec système d'avis

**Votre site e-commerce de maillots de football est maintenant prêt !** ⚽🎊

---

*Guide de déploiement créé le 05/09/2025 - Version 1.0*
*Importation automatique des équipes de football - Prêt pour production*
