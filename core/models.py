from django.db import models
from django.core.validators import MinValueValidator


class ShippingSettings(models.Model):
    """Paramètres de livraison"""
    delivery_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=1000,
        validators=[MinValueValidator(0)],
        verbose_name="Frais de livraison (FCFA)"
    )
    free_delivery_threshold = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=25000,
        validators=[MinValueValidator(0)],
        verbose_name="Seuil livraison gratuite (FCFA)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Paramètre de livraison"
        verbose_name_plural = "Paramètres de livraison"

    def __str__(self):
        return f"Livraison: {self.delivery_fee} FCFA (Gratuit > {self.free_delivery_threshold} FCFA)"

    @classmethod
    def get_active_settings(cls):
        """Récupère les paramètres actifs"""
        settings = cls.objects.filter(is_active=True).first()
        if not settings:
            # Créer des paramètres par défaut
            settings = cls.objects.create()
        return settings

    def calculate_shipping_cost(self, subtotal):
        """Calcule les frais de livraison selon le sous-total"""
        if subtotal >= self.free_delivery_threshold:
            return 0
        return self.delivery_fee