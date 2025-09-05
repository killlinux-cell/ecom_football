#!/usr/bin/env python
"""
Script pour initialiser les paramètres de livraison
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def init_shipping_settings():
    """Initialise les paramètres de livraison"""
    print("🚚 Initialisation des paramètres de livraison...")
    
    try:
        from core.models import ShippingSettings
        
        # Vérifier si des paramètres existent déjà
        existing_settings = ShippingSettings.objects.filter(is_active=True).first()
        
        if existing_settings:
            print(f"✅ Paramètres existants trouvés:")
            print(f"   - Frais de livraison: {existing_settings.delivery_fee} FCFA")
            print(f"   - Seuil livraison gratuite: {existing_settings.free_delivery_threshold} FCFA")
            print(f"   - Statut: {'Actif' if existing_settings.is_active else 'Inactif'}")
        else:
            # Créer des paramètres par défaut
            settings = ShippingSettings.objects.create(
                delivery_fee=1000,
                free_delivery_threshold=25000,
                is_active=True
            )
            print(f"✅ Paramètres créés avec succès:")
            print(f"   - Frais de livraison: {settings.delivery_fee} FCFA")
            print(f"   - Seuil livraison gratuite: {settings.free_delivery_threshold} FCFA")
            print(f"   - Statut: Actif")
        
        # Tester le calcul des frais
        print("\n🧪 Test des calculs de livraison:")
        settings = ShippingSettings.get_active_settings()
        
        test_amounts = [15000, 25000, 30000, 50000]
        for amount in test_amounts:
            shipping_cost = settings.calculate_shipping_cost(amount)
            print(f"   - Sous-total {amount:,} FCFA → Frais: {shipping_cost} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_shipping_settings()
    if success:
        print("\n🎉 Initialisation terminée avec succès!")
        print("📦 Le système de livraison est maintenant configuré")
    else:
        print("\n💥 Échec de l'initialisation")
        sys.exit(1)
