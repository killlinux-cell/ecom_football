# 📧 Guide Complet - Système de Notifications Email

## 🎯 Vue d'ensemble

Le système de notifications email a été entièrement implémenté pour votre e-commerce de maillots de football. Il permet d'envoyer automatiquement des emails professionnels à vos clients à chaque étape de leur parcours d'achat.

## 🚀 Fonctionnalités Implémentées

### **📬 Types d'Emails Automatiques**

1. **✅ Confirmation de commande** - Envoyé immédiatement après création
2. **✅ Confirmation de paiement** - Quand le paiement est validé
3. **✅ Notification d'expédition** - Quand la commande est expédiée
4. **✅ Notification de livraison** - Quand la commande est livrée
5. **✅ Rappel de panier abandonné** - 24h après abandon
6. **✅ Alerte stock faible** - Pour les administrateurs

### **🎨 Templates Professionnels**

- ✅ Design responsive et moderne
- ✅ Compatible mobile et desktop
- ✅ Branding cohérent avec votre site
- ✅ Templates HTML et texte
- ✅ Personnalisation complète

### **⚙️ Gestion Avancée**

- ✅ Dashboard de gestion des emails
- ✅ Logs détaillés de tous les envois
- ✅ Configuration SMTP flexible
- ✅ Templates éditables
- ✅ Tests d'envoi intégrés

## 📋 Installation et Configuration

### **1. Ajouter l'App au Projet**

Ajoutez `notifications` à votre `INSTALLED_APPS` dans `settings.py` :

```python
INSTALLED_APPS = [
    # ... autres apps
    'notifications',
]
```

### **2. Appliquer les Migrations**

```bash
python manage.py makemigrations notifications
python manage.py migrate
```

### **3. Initialiser les Templates**

```bash
python manage.py init_email_templates
```

### **4. Ajouter les URLs**

Dans votre `urls.py` principal :

```python
urlpatterns = [
    # ... autres URLs
    path('dashboard/emails/', include('notifications.urls')),
]
```

### **5. Configurer les Signaux**

Dans votre `apps.py` :

```python
class EcomMaillotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecom_maillot'
    
    def ready(self):
        import notifications.signals
```

## ⚙️ Configuration SMTP

### **1. Accéder aux Paramètres**

Allez dans le dashboard : `/dashboard/emails/settings/`

### **2. Configuration Gmail (Recommandé)**

```
Serveur SMTP: smtp.gmail.com
Port: 587
Utiliser TLS: ✅
Email: votre-email@gmail.com
Mot de passe: votre-mot-de-passe-app
```

### **3. Configuration Autre Fournisseur**

- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Serveur personnalisé**: Selon votre hébergeur

### **4. Paramètres Avancés**

- ✅ **Activer/Désactiver** le système globalement
- ✅ **Choisir quels emails** envoyer automatiquement
- ✅ **Limiter le nombre** d'emails par heure
- ✅ **Configurer le délai** des rappels de panier

## 📊 Dashboard de Gestion

### **Accès au Dashboard**

URL : `/dashboard/emails/`

### **Fonctionnalités Disponibles**

1. **📊 Statistiques en temps réel**
   - Total d'emails envoyés
   - Taux de succès/échec
   - Emails par type
   - Activité récente

2. **📧 Gestion des Templates**
   - Édition des templates HTML
   - Prévisualisation en temps réel
   - Activation/désactivation
   - Tests d'envoi

3. **📋 Logs d'Emails**
   - Historique complet des envois
   - Statuts détaillés
   - Possibilité de renvoyer
   - Filtres et recherche

4. **⚙️ Configuration**
   - Paramètres SMTP
   - Options d'envoi
   - Tests de configuration

## 🎨 Personnalisation des Templates

### **Variables Disponibles**

#### **Confirmation de Commande**
```html
{{ customer_name }}          <!-- Nom du client -->
{{ order.order_number }}     <!-- Numéro de commande -->
{{ order.total }}           <!-- Total de la commande -->
{{ order_items }}           <!-- Articles de la commande -->
{{ shipping_address }}      <!-- Adresse de livraison -->
```

#### **Confirmation de Paiement**
```html
{{ payment_amount }}        <!-- Montant payé -->
{{ payment_method }}        <!-- Méthode de paiement -->
{{ payment.completed_at }}  <!-- Date de paiement -->
```

#### **Rappel de Panier**
```html
{{ cart_items }}           <!-- Articles du panier -->
{{ user }}                 <!-- Utilisateur -->
```

### **Structure des Templates**

```html
{% extends "emails/base_email.html" %}

{% block content %}
<h2>Votre titre</h2>
<p>Contenu de votre email...</p>

<!-- Utiliser les classes CSS prédéfinies -->
<div class="order-details">
    <!-- Contenu -->
</div>

<div class="button">
    <a href="{{ lien }}">Bouton d'action</a>
</div>
{% endblock %}
```

## 🔄 Automatisation

### **Signaux Automatiques**

Les emails sont envoyés automatiquement grâce aux signaux Django :

- ✅ **Création de commande** → Email de confirmation
- ✅ **Paiement validé** → Email de confirmation
- ✅ **Commande expédiée** → Email de notification
- ✅ **Commande livrée** → Email de notification
- ✅ **Stock faible** → Alerte administrateur

### **Tâches Cron (Recommandé)**

Ajoutez à votre crontab pour les rappels de panier :

```bash
# Rappels de panier abandonné toutes les heures
0 * * * * cd /path/to/your/project && python manage.py send_cart_reminders

# Nettoyage des logs anciens (optionnel)
0 2 * * 0 cd /path/to/your/project && python manage.py cleanup_email_logs
```

## 🧪 Tests et Validation

### **1. Test du Système**

```bash
python test_email_system.py
```

### **2. Test d'Envoi**

Dans le dashboard :
1. Allez dans "Paramètres"
2. Cliquez sur "Email Test"
3. Choisissez un template
4. Entrez votre email
5. Cliquez sur "Envoyer"

### **3. Vérification des Logs**

Consultez les logs dans `/dashboard/emails/logs/` pour voir :
- ✅ Emails envoyés avec succès
- ❌ Emails échoués avec raisons
- ⏳ Emails en attente

## 📈 Optimisation et Performance

### **Limites Recommandées**

- **Max emails/heure** : 100-500 selon votre serveur
- **Délai rappel panier** : 24-48 heures
- **Rétention logs** : 90 jours

### **Monitoring**

Surveillez régulièrement :
- ✅ Taux de succès des envois
- ✅ Temps de réponse SMTP
- ✅ Emails échoués
- ✅ Utilisation des templates

## 🚨 Dépannage

### **Problèmes Courants**

#### **1. Emails non envoyés**
- ✅ Vérifier la configuration SMTP
- ✅ Vérifier que le système est activé
- ✅ Consulter les logs d'erreur

#### **2. Templates non trouvés**
```bash
python manage.py init_email_templates
```

#### **3. Signaux non déclenchés**
- ✅ Vérifier que `notifications.signals` est importé
- ✅ Redémarrer le serveur Django

#### **4. Erreurs SMTP**
- ✅ Vérifier les identifiants
- ✅ Activer l'authentification 2FA pour Gmail
- ✅ Utiliser un mot de passe d'application

### **Logs de Debug**

Activez les logs Django pour plus de détails :

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'notifications': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## 🎯 Prochaines Améliorations

### **Fonctionnalités Futures**

1. **📊 Analytics avancés**
   - Taux d'ouverture
   - Taux de clic
   - Segmentation des clients

2. **🎨 Éditeur WYSIWYG**
   - Interface visuelle pour les templates
   - Glisser-déposer d'éléments

3. **📱 Notifications Push**
   - Intégration avec les PWA
   - Notifications mobiles

4. **🤖 IA et Personnalisation**
   - Recommandations personnalisées
   - Optimisation automatique des horaires

## 📞 Support

### **Commandes Utiles**

```bash
# Initialiser les templates
python manage.py init_email_templates

# Envoyer les rappels de panier
python manage.py send_cart_reminders

# Test du système
python test_email_system.py

# Voir les logs en temps réel
tail -f debug.log
```

### **Fichiers Importants**

- `notifications/models.py` - Modèles de données
- `notifications/email_service.py` - Service d'envoi
- `notifications/signals.py` - Automatisation
- `notifications/templates/` - Templates HTML
- `test_email_system.py` - Tests

---

## 🎉 Félicitations !

Votre système de notifications email est maintenant opérationnel ! Vos clients recevront des emails professionnels à chaque étape de leur parcours d'achat, améliorant significativement leur expérience et votre taux de conversion.

**Prochaines étapes recommandées :**
1. ✅ Configurer votre SMTP
2. ✅ Tester l'envoi d'emails
3. ✅ Personnaliser les templates
4. ✅ Configurer les tâches cron
5. ✅ Monitorer les performances

Votre e-commerce est maintenant équipé d'un système d'emails de niveau professionnel ! 🚀
