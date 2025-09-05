#!/usr/bin/env python
"""
Test des corrections de calcul des montants
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

from orders.models import Order
from payments.models import Payment
from orders.sync_utils import get_status_consistency_report, fix_amount_inconsistencies

def test_calculation_fixes():
    """Test des corrections de calcul"""
    print("🧪 Test des corrections de calcul des montants...")
    
    # 1. Vérifier les incohérences existantes
    print("\n1. Vérification des incohérences existantes...")
    inconsistencies = get_status_consistency_report()
    
    if inconsistencies:
        print(f"⚠️ {len(inconsistencies)} incohérence(s) trouvée(s):")
        for inconsistency in inconsistencies:
            if inconsistency['inconsistency_type'] == 'amount_mismatch':
                print(f"💰 Commande {inconsistency['order_number']}:")
                print(f"   Order: {inconsistency['order_total']} FCFA")
                print(f"   Payment: {inconsistency['payment_amount']} FCFA")
                print(f"   Différence: {inconsistency['difference']} FCFA")
            elif inconsistency['inconsistency_type'] == 'status_mismatch':
                print(f"📋 Commande {inconsistency['order_number']}:")
                print(f"   Order Status: {inconsistency['order_payment_status']}")
                print(f"   Payment Status: {inconsistency['payment_status']}")
                print(f"   Attendu: {inconsistency['expected_payment_status']}")
    else:
        print("✅ Aucune incohérence trouvée!")
    
    # 2. Corriger les incohérences de montants
    print("\n2. Correction des incohérences de montants...")
    fixed_count = fix_amount_inconsistencies()
    print(f"🎉 {fixed_count} incohérence(s) de montant corrigée(s)")
    
    # 3. Vérifier que les corrections ont fonctionné
    print("\n3. Vérification post-correction...")
    inconsistencies_after = get_status_consistency_report()
    
    amount_inconsistencies = [i for i in inconsistencies_after if i['inconsistency_type'] == 'amount_mismatch']
    
    if amount_inconsistencies:
        print(f"❌ {len(amount_inconsistencies)} incohérence(s) de montant restante(s):")
        for inconsistency in amount_inconsistencies:
            print(f"💰 Commande {inconsistency['order_number']}: {inconsistency['difference']} FCFA")
    else:
        print("✅ Toutes les incohérences de montant ont été corrigées!")
    
    # 4. Statistiques générales
    print("\n4. Statistiques générales...")
    total_orders = Order.objects.count()
    orders_with_payments = Order.objects.filter(payment__isnull=False).count()
    total_payments = Payment.objects.count()
    
    print(f"📊 Total commandes: {total_orders}")
    print(f"📊 Commandes avec paiements: {orders_with_payments}")
    print(f"📊 Total paiements: {total_payments}")
    
    # 5. Vérifier la cohérence des montants
    print("\n5. Vérification de la cohérence des montants...")
    orders_with_payments = Order.objects.filter(payment__isnull=False).select_related('payment')
    
    consistent_count = 0
    inconsistent_count = 0
    
    for order in orders_with_payments:
        payment = order.payment
        if payment.amount == order.total:
            consistent_count += 1
        else:
            inconsistent_count += 1
            print(f"❌ Incohérence: Commande {order.order_number} - Order: {order.total}, Payment: {payment.amount}")
    
    print(f"✅ Montants cohérents: {consistent_count}")
    print(f"❌ Montants incohérents: {inconsistent_count}")
    
    if inconsistent_count == 0:
        print("\n🎉 SUCCÈS: Tous les montants sont cohérents!")
        return True
    else:
        print(f"\n⚠️ ATTENTION: {inconsistent_count} incohérence(s) de montant détectée(s)")
        return False

if __name__ == "__main__":
    success = test_calculation_fixes()
    sys.exit(0 if success else 1)
