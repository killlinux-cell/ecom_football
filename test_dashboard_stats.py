#!/usr/bin/env python
"""
Script de test pour vérifier les statistiques du dashboard des paiements
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from orders.models import Order
from payments.models import Payment
from django.utils import timezone

def test_payment_statistics():
    """Test des statistiques des paiements"""
    print("🧪 Test des statistiques des paiements...")
    
    import time
    timestamp = str(int(time.time()))
    
    # Créer un utilisateur admin
    admin_user = User.objects.create_user(
        username=f'admin_stats_test_{timestamp}',
        email=f'admin{timestamp}@stats.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    
    # Créer un utilisateur client
    client_user = User.objects.create_user(
        username=f'client_stats_test_{timestamp}',
        email=f'client{timestamp}@stats.com',
        password='testpass123'
    )
    
    # Créer des commandes et paiements de test
    orders = []
    payments = []
    
    # Paiement en attente
    order1 = Order.objects.create(
        user=client_user,
        order_number=f'STATS001_{timestamp}',
        status='pending',
        payment_status='pending',
        subtotal=5000,
        shipping_cost=500,
        total=5500
    )
    payment1 = Payment.objects.create(
        order=order1,
        payment_id=f'PAY_STATS001_{timestamp}',
        amount=5500,
        status='pending',
        payment_method='wave_direct',
        customer_name='Test Client 1',
        customer_email=f'client{timestamp}@stats.com',
        customer_phone='0575984322'
    )
    orders.append(order1)
    payments.append(payment1)
    
    # Paiement complété
    order2 = Order.objects.create(
        user=client_user,
        order_number=f'STATS002_{timestamp}',
        status='processing',
        payment_status='paid',
        subtotal=10000,
        shipping_cost=1000,
        total=11000
    )
    payment2 = Payment.objects.create(
        order=order2,
        payment_id=f'PAY_STATS002_{timestamp}',
        amount=11000,
        status='completed',
        payment_method='wave_direct',
        customer_name='Test Client 2',
        customer_email=f'client{timestamp}@stats.com',
        customer_phone='0575984322',
        completed_at=timezone.now()
    )
    orders.append(order2)
    payments.append(payment2)
    
    # Paiement échoué
    order3 = Order.objects.create(
        user=client_user,
        order_number=f'STATS003_{timestamp}',
        status='pending',
        payment_status='failed',
        subtotal=7500,
        shipping_cost=750,
        total=8250
    )
    payment3 = Payment.objects.create(
        order=order3,
        payment_id=f'PAY_STATS003_{timestamp}',
        amount=8250,
        status='failed',
        payment_method='wave_direct',
        customer_name='Test Client 3',
        customer_email=f'client{timestamp}@stats.com',
        customer_phone='0575984322'
    )
    orders.append(order3)
    payments.append(payment3)
    
    print(f"✅ {len(orders)} commandes créées")
    print(f"✅ {len(payments)} paiements créés")
    
    # Tester l'accès au dashboard des paiements
    client = Client()
    client.force_login(admin_user)
    
    response = client.get('/dashboard/payments/')
    
    print(f"📊 Code de réponse: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Dashboard des paiements accessible")
        
        # Vérifier que les statistiques sont dans le contexte
        if hasattr(response, 'context') and response.context:
            context = response.context
            
            print(f"📊 Total paiements: {context.get('total_payments', 'N/A')}")
            print(f"📊 Paiements en attente: {context.get('pending_payments_count', 'N/A')}")
            print(f"📊 Paiements complétés: {context.get('completed_payments_count', 'N/A')}")
            print(f"📊 Paiements échoués: {context.get('failed_payments_count', 'N/A')}")
            print(f"📊 Montant total: {context.get('total_amount', 'N/A')} FCFA")
            print(f"📊 Wave en attente: {context.get('wave_pending_count', 'N/A')}")
            
            # Vérifications
            test_success = True
            
            if context.get('total_payments', 0) < 3:
                print("❌ ERREUR: Le total des paiements ne correspond pas")
                test_success = False
            else:
                print("✅ Total des paiements correct")
            
            if context.get('pending_payments_count', 0) < 1:
                print("❌ ERREUR: Le nombre de paiements en attente ne correspond pas")
                test_success = False
            else:
                print("✅ Paiements en attente correct")
            
            if context.get('completed_payments_count', 0) < 1:
                print("❌ ERREUR: Le nombre de paiements complétés ne correspond pas")
                test_success = False
            else:
                print("✅ Paiements complétés correct")
            
            if context.get('failed_payments_count', 0) < 1:
                print("❌ ERREUR: Le nombre de paiements échoués ne correspond pas")
                test_success = False
            else:
                print("✅ Paiements échoués correct")
            
            if context.get('total_amount', 0) < 11000:
                print("❌ ERREUR: Le montant total ne correspond pas")
                test_success = False
            else:
                print("✅ Montant total correct")
        else:
            print("❌ ERREUR: Pas de contexte disponible")
            test_success = False
        
    else:
        print("❌ ERREUR: Impossible d'accéder au dashboard des paiements")
        test_success = False
    
    # Nettoyage
    for order in orders:
        order.delete()
    for payment in payments:
        payment.delete()
    admin_user.delete()
    client_user.delete()
    
    if test_success:
        print("🎉 Test des statistiques des paiements: SUCCÈS")
    else:
        print("💥 Test des statistiques des paiements: ÉCHEC")
    
    return test_success

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage du test des statistiques du dashboard")
    print("=" * 60)
    
    try:
        result = test_payment_statistics()
        
        print("\n" + "=" * 60)
        print("📊 RÉSULTATS FINAUX")
        print("=" * 60)
        
        if result:
            print("🎉 TEST RÉUSSI!")
            print("✅ Les statistiques du dashboard des paiements fonctionnent correctement")
        else:
            print("💥 TEST ÉCHOUÉ")
            print("❌ Vérifiez les erreurs ci-dessus")
        
        return result
        
    except Exception as e:
        print(f"💥 Erreur lors du test: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
