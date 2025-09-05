#!/usr/bin/env python
"""
Test complet de la correction des incohérences de livraison
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_shipping_calculations():
    """Test des calculs de livraison"""
    print("🧪 Test des calculs de livraison...")
    
    try:
        from core.models import ShippingSettings
        from decimal import Decimal
        
        # Récupérer les paramètres
        settings = ShippingSettings.get_active_settings()
        print(f"✅ Paramètres récupérés:")
        print(f"   - Frais de livraison: {settings.delivery_fee} FCFA")
        print(f"   - Seuil livraison gratuite: {settings.free_delivery_threshold} FCFA")
        
        # Tests de calcul
        test_cases = [
            (Decimal('15000'), Decimal('1000'), "Commande normale"),
            (Decimal('25000'), Decimal('0'), "Seuil exact"),
            (Decimal('30000'), Decimal('0'), "Au-dessus du seuil"),
            (Decimal('50000'), Decimal('0'), "Commande importante"),
        ]
        
        print("\n📊 Tests de calcul:")
        all_passed = True
        
        for subtotal, expected_shipping, description in test_cases:
            actual_shipping = settings.calculate_shipping_cost(subtotal)
            total = subtotal + actual_shipping
            
            status = "✅" if actual_shipping == expected_shipping else "❌"
            print(f"   {status} {description}:")
            print(f"      Sous-total: {subtotal:,} FCFA")
            print(f"      Frais livraison: {actual_shipping} FCFA (attendu: {expected_shipping} FCFA)")
            print(f"      Total: {total:,} FCFA")
            
            if actual_shipping != expected_shipping:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_template_tags():
    """Test des template tags"""
    print("\n🏷️ Test des template tags...")
    
    try:
        from core.templatetags.shipping_extras import calculate_shipping_cost, is_free_shipping, get_shipping_settings
        from decimal import Decimal
        
        # Test calculate_shipping_cost
        shipping_cost = calculate_shipping_cost(Decimal('15000'))
        print(f"✅ calculate_shipping_cost(15000) = {shipping_cost} FCFA")
        
        # Test is_free_shipping
        is_free = is_free_shipping(Decimal('30000'))
        print(f"✅ is_free_shipping(30000) = {is_free}")
        
        # Test get_shipping_settings
        settings = get_shipping_settings()
        print(f"✅ get_shipping_settings() = {settings.delivery_fee} FCFA (seuil: {settings.free_delivery_threshold} FCFA)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des template tags: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_order_creation():
    """Test de la création de commande avec nouveaux calculs"""
    print("\n📦 Test de la création de commande...")
    
    try:
        from orders.views import order_create
        from core.models import ShippingSettings
        
        # Simuler le calcul dans order_create
        settings = ShippingSettings.get_active_settings()
        
        # Test avec différents sous-totaux
        test_subtotals = [Decimal('15000'), Decimal('25000'), Decimal('30000')]
        
        for subtotal in test_subtotals:
            shipping_cost = settings.calculate_shipping_cost(subtotal)
            total = subtotal + shipping_cost
            
            print(f"✅ Sous-total {subtotal:,} FCFA:")
            print(f"   - Frais livraison: {shipping_cost} FCFA")
            print(f"   - Total commande: {total:,} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de création de commande: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    print("🔧 Test de la correction des incohérences de livraison")
    print("=" * 60)
    
    tests = [
        ("Calculs de livraison", test_shipping_calculations),
        ("Template tags", test_template_tags),
        ("Création de commande", test_order_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"   {status} - {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ La correction des incohérences de livraison est fonctionnelle")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ Des problèmes persistent dans la correction")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
