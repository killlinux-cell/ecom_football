#!/usr/bin/env python
"""
Script pour corriger les prix doublés dans les commandes
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_doubled_prices():
    """Corrige les prix doublés dans les commandes"""
    print("🔧 CORRECTION DES PRIX DOUBLÉS")
    print("=" * 60)
    
    try:
        from orders.models import Order, OrderItem
        from decimal import Decimal
        
        # Trouver les commandes avec des prix potentiellement doublés
        orders = Order.objects.all()
        print(f"📊 {orders.count()} commande(s) à vérifier")
        
        corrected_count = 0
        
        for order in orders:
            print(f"\n📋 Commande {order.order_number}:")
            print(f"   - Sous-total: {order.subtotal} FCFA")
            print(f"   - Total: {order.total} FCFA")
            
            order_corrected = False
            
            for item in order.items.all():
                # Calculer le prix attendu (prix unitaire × quantité)
                expected_price = item.price * item.quantity
                
                print(f"\n   📦 Article: {item.product_name}")
                print(f"      - Prix unitaire: {item.price} FCFA")
                print(f"      - Quantité: {item.quantity}")
                print(f"      - Prix attendu: {expected_price} FCFA")
                print(f"      - Prix actuel: {item.total_price} FCFA")
                
                # Vérifier si le prix est doublé
                if item.total_price == expected_price * 2:
                    print(f"      ⚠️ PRIX DOUBLÉ DÉTECTÉ!")
                    
                    # Corriger le prix
                    item.total_price = expected_price
                    item.save()
                    
                    print(f"      ✅ Prix corrigé: {item.total_price} FCFA")
                    order_corrected = True
                    corrected_count += 1
                elif item.total_price == expected_price:
                    print(f"      ✅ Prix correct")
                else:
                    # Vérifier s'il y a des personnalisations
                    customizations = item.customizations.all()
                    if customizations:
                        customization_price = sum(cust.price for cust in customizations)
                        expected_with_custom = expected_price + customization_price
                        print(f"      - Personnalisations: {customization_price} FCFA")
                        print(f"      - Prix attendu avec personnalisations: {expected_with_custom} FCFA")
                        
                        if item.total_price == expected_with_custom:
                            print(f"      ✅ Prix correct avec personnalisations")
                        else:
                            print(f"      ⚠️ Prix incohérent (différence: {item.total_price - expected_with_custom} FCFA)")
                    else:
                        print(f"      ⚠️ Prix incohérent (différence: {item.total_price - expected_price} FCFA)")
            
            # Recalculer le sous-total de la commande si nécessaire
            if order_corrected:
                print(f"\n   🔄 Recalcul du sous-total...")
                new_subtotal = sum(item.total_price for item in order.items.all())
                order.subtotal = new_subtotal
                order.total = new_subtotal + order.shipping_cost
                order.save()
                
                print(f"   ✅ Nouveau sous-total: {order.subtotal} FCFA")
                print(f"   ✅ Nouveau total: {order.total} FCFA")
        
        print(f"\n📊 RÉSUMÉ DE LA CORRECTION:")
        print(f"   - Commandes vérifiées: {orders.count()}")
        print(f"   - Articles corrigés: {corrected_count}")
        
        if corrected_count > 0:
            print(f"\n🎉 CORRECTION TERMINÉE!")
            print(f"✅ {corrected_count} article(s) corrigé(s)")
        else:
            print(f"\n✅ Aucun prix doublé détecté")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def test_price_calculation():
    """Teste le calcul des prix"""
    print("\n🧪 TEST DU CALCUL DES PRIX")
    print("=" * 60)
    
    try:
        from orders.models import OrderItem
        from decimal import Decimal
        
        # Tester avec un article d'exemple
        items = OrderItem.objects.all()[:5]  # Prendre 5 articles pour test
        
        for item in items:
            print(f"\n📦 Test: {item.product_name}")
            print(f"   - Prix unitaire: {item.price} FCFA")
            print(f"   - Quantité: {item.quantity}")
            print(f"   - Prix attendu: {item.price * item.quantity} FCFA")
            print(f"   - Prix actuel: {item.total_price} FCFA")
            
            # Vérifier la cohérence
            expected = item.price * item.quantity
            if abs(item.total_price - expected) < 0.01:
                print(f"   ✅ Prix cohérent")
            else:
                print(f"   ❌ Prix incohérent (différence: {item.total_price - expected} FCFA)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION DES PRIX DOUBLÉS")
    print("=" * 60)
    
    # Corriger les prix doublés
    success1 = fix_doubled_prices()
    
    # Tester le calcul des prix
    success2 = test_price_calculation()
    
    if success1 and success2:
        print("\n🎉 CORRECTION TERMINÉE!")
        print("✅ Les prix doublés ont été corrigés")
        print("✅ Les calculs sont maintenant cohérents")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ Des problèmes persistent")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
