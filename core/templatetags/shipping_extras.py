from django import template
from decimal import Decimal
from core.models import ShippingSettings

register = template.Library()


@register.simple_tag
def calculate_shipping_cost(subtotal):
    """Calcule les frais de livraison selon le sous-total"""
    shipping_settings = ShippingSettings.get_active_settings()
    return shipping_settings.calculate_shipping_cost(subtotal)


@register.simple_tag
def get_shipping_settings():
    """Récupère les paramètres de livraison"""
    return ShippingSettings.get_active_settings()


@register.filter
def is_free_shipping(subtotal):
    """Vérifie si la livraison est gratuite"""
    shipping_settings = ShippingSettings.get_active_settings()
    return subtotal >= shipping_settings.free_delivery_threshold
