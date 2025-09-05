from django.contrib import admin
from .models import ShippingSettings


@admin.register(ShippingSettings)
class ShippingSettingsAdmin(admin.ModelAdmin):
    list_display = ['delivery_fee', 'free_delivery_threshold', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['delivery_fee', 'free_delivery_threshold']
    
    fieldsets = (
        ('Paramètres de Livraison', {
            'fields': ('delivery_fee', 'free_delivery_threshold')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # S'assurer qu'il n'y a qu'un seul paramètre actif
        if obj.is_active:
            ShippingSettings.objects.filter(is_active=True).exclude(id=obj.id).update(is_active=False)
        super().save_model(request, obj, form, change)