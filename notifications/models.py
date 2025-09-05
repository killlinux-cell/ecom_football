from django.db import models
from django.contrib.auth.models import User
from orders.models import Order
from payments.models import Payment


class EmailTemplate(models.Model):
    """Modèle pour gérer les templates d'emails"""
    
    TEMPLATE_TYPES = [
        ('order_confirmation', 'Confirmation de commande'),
        ('payment_confirmation', 'Confirmation de paiement'),
        ('order_shipped', 'Commande expédiée'),
        ('order_delivered', 'Commande livrée'),
        ('cart_reminder', 'Rappel de panier abandonné'),
        ('stock_alert', 'Alerte stock faible'),
        ('promotion', 'Email de promotion'),
        ('welcome', 'Email de bienvenue'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom du template")
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES, verbose_name="Type de template")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    html_content = models.TextField(verbose_name="Contenu HTML")
    text_content = models.TextField(blank=True, verbose_name="Contenu texte")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Template Email"
        verbose_name_plural = "Templates Email"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class EmailLog(models.Model):
    """Log des emails envoyés"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('sent', 'Envoyé'),
        ('failed', 'Échoué'),
        ('bounced', 'Retourné'),
    ]
    
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, verbose_name="Template")
    recipient_email = models.EmailField(verbose_name="Email destinataire")
    recipient_name = models.CharField(max_length=100, blank=True, verbose_name="Nom destinataire")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    
    # Relations optionnelles
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Commande")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Paiement")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilisateur")
    
    # Données de l'email
    email_data = models.JSONField(default=dict, verbose_name="Données email")
    error_message = models.TextField(blank=True, verbose_name="Message d'erreur")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Envoyé le")
    
    class Meta:
        verbose_name = "Log Email"
        verbose_name_plural = "Logs Email"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.recipient_email} ({self.status})"


class EmailSettings(models.Model):
    """Paramètres de configuration des emails"""
    
    # Configuration SMTP
    smtp_host = models.CharField(max_length=100, default='smtp.gmail.com', verbose_name="Serveur SMTP")
    smtp_port = models.IntegerField(default=587, verbose_name="Port SMTP")
    smtp_username = models.EmailField(verbose_name="Email SMTP")
    smtp_password = models.CharField(max_length=100, verbose_name="Mot de passe SMTP")
    use_tls = models.BooleanField(default=True, verbose_name="Utiliser TLS")
    
    # Configuration expéditeur
    from_email = models.EmailField(verbose_name="Email expéditeur")
    from_name = models.CharField(max_length=100, default="Maillots Football", verbose_name="Nom expéditeur")
    
    # Paramètres généraux
    is_active = models.BooleanField(default=True, verbose_name="Système actif")
    send_order_confirmations = models.BooleanField(default=True, verbose_name="Confirmer les commandes")
    send_payment_confirmations = models.BooleanField(default=True, verbose_name="Confirmer les paiements")
    send_shipping_notifications = models.BooleanField(default=True, verbose_name="Notifications d'expédition")
    send_cart_reminders = models.BooleanField(default=True, verbose_name="Rappels de panier")
    send_stock_alerts = models.BooleanField(default=True, verbose_name="Alertes de stock")
    
    # Limites
    max_emails_per_hour = models.IntegerField(default=100, verbose_name="Max emails/heure")
    cart_reminder_delay_hours = models.IntegerField(default=24, verbose_name="Délai rappel panier (heures)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Configuration Email"
        verbose_name_plural = "Configurations Email"
    
    def __str__(self):
        return f"Configuration Email - {self.from_email}"
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule configuration
        if not self.pk and EmailSettings.objects.exists():
            # Si c'est une nouvelle instance et qu'il en existe déjà une, ne pas sauvegarder
            return
        super().save(*args, **kwargs)
