#!/usr/bin/env python
"""
Test de la correction des incohérences de totaux
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_order_validation():
    """Test de la validation des totaux de commande"""
    print("🧪 Test de la validation des totaux de commande...")
    
    try:
        from orders.models import Order
        
        # Tester la validation sur toutes les commandes
        orders = Order.objects.all()
        valid_count = 0
        invalid_count = 0
        
        for order in orders:
            if order.validate_totals():
                valid_count += 1
            else:
                invalid_count += 1
                print(f"❌ Commande {order.order_number} invalide")
        
        print(f"✅ Commandes valides: {valid_count}")
        print(f"❌ Commandes invalides: {invalid_count}")
        
        return invalid_count == 0
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_recalculate_totals():
    """Test de la méthode recalculate_totals"""
    print("\n🧪 Test de la méthode recalculate_totals...")
    
    try:
        from orders.models import Order
        
        # Prendre une commande d'exemple
        order = Order.objects.first()
        if not order:
            print("❌ Aucune commande trouvée")
            return False
        
        print(f"📋 Test sur la commande {order.order_number}")
        print(f"   - Sous-total avant: {order.subtotal} FCFA")
        print(f"   - Total avant: {order.total} FCFA")
        
        # Recalculer
        result = order.recalculate_totals()
        
        print(f"   - Sous-total après: {order.subtotal} FCFA")
        print(f"   - Total après: {order.total} FCFA")
        print(f"   - Résultat: {result}")
        
        # Vérifier la cohérence
        is_valid = order.validate_totals()
        print(f"   - Validation: {'✅ Valide' if is_valid else '❌ Invalide'}")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_command_creation_validation():
    """Test de la validation lors de la création de commande"""
    print("\n🧪 Test de la validation lors de la création de commande...")
    
    try:
        from orders.models import Order
        from django.contrib.auth.models import User
        
        # Vérifier qu'il n'y a plus de commandes avec 0 articles
        orders_without_items = Order.objects.filter(items__isnull=True).distinct()
        
        if orders_without_items.exists():
            print(f"❌ {orders_without_items.count()} commande(s) sans articles trouvée(s)")
            for order in orders_without_items:
                print(f"   - {order.order_number}")
            return False
        else:
            print("✅ Aucune commande sans articles")
            return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    print("🔧 TEST DE LA CORRECTION DES INCOHÉRENCES DE TOTAUX")
    print("=" * 60)
    
    tests = [
        ("Validation des totaux", test_order_validation),
        ("Recalcul des totaux", test_recalculate_totals),
        ("Validation création commande", test_command_creation_validation),
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
        print("✅ La correction des incohérences de totaux est fonctionnelle")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ Des problèmes persistent dans la correction")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
