#!/usr/bin/env python
"""
Script de test pour vérifier la synchronisation entre Order et Payment
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from orders.models import Order
from payments.models import Payment, PaymentLog
from orders.sync_utils import (
    sync_order_payment_status, 
    sync_payment_order_status, 
    cancel_order_and_payment,
    validate_payment_and_order,
    get_status_consistency_report
)
from django.utils import timezone

def test_sync_order_to_payment():
    """Test de synchronisation Order -> Payment"""
    print("🧪 Test de synchronisation Order -> Payment...")
    
    # Créer un utilisateur admin
    admin_user = User.objects.create_user(
        username='admin_sync_test',
        email='admin@sync.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    
    # Créer un utilisateur client
    client_user = User.objects.create_user(
        username='client_sync_test',
        email='client@sync.com',
        password='testpass123'
    )
    
    # Créer une commande
    order = Order.objects.create(
        user=client_user,
        order_number='SYNC001',
        status='pending',
        payment_status='pending',
        subtotal=10000,
        shipping_cost=1000,
        total=11000
    )
    
    # Créer un paiement
    payment = Payment.objects.create(
        order=order,
        payment_id='PAY_SYNC001',
        amount=11000,
        status='pending',
        payment_method='wave_direct',
        customer_name='Test Client',
        customer_email='client@sync.com',
        customer_phone='0575984322'
    )
    
    print(f"✅ Commande créée: {order.order_number}")
    print(f"✅ Paiement créé: {payment.id}")
    print(f"📊 Statut initial - Order: {order.payment_status}, Payment: {payment.status}")
    
    # Tester la synchronisation Order -> Payment
    success = sync_order_payment_status(order, 'paid', updated_by=admin_user)
    
    # Vérifier les résultats
    order.refresh_from_db()
    payment.refresh_from_db()
    
    print(f"📊 Statut après sync - Order: {order.payment_status}, Payment: {payment.status}")
    
    # Vérifications
    test_success = True
    
    if not success:
        print("❌ ERREUR: La synchronisation a échoué")
        test_success = False
    else:
        print("✅ La synchronisation a réussi")
    
    if payment.status != 'completed':
        print("❌ ERREUR: Le statut du paiement n'a pas été mis à jour vers 'completed'")
        test_success = False
    else:
        print("✅ Le statut du paiement a été mis à jour vers 'completed'")
    
    if not payment.completed_at:
        print("❌ ERREUR: La date de completion n'a pas été définie")
        test_success = False
    else:
        print("✅ La date de completion a été définie")
    
    # Nettoyage
    order.delete()
    admin_user.delete()
    client_user.delete()
    
    if test_success:
        print("🎉 Test de synchronisation Order -> Payment: SUCCÈS")
    else:
        print("💥 Test de synchronisation Order -> Payment: ÉCHEC")
    
    return test_success

def test_sync_payment_to_order():
    """Test de synchronisation Payment -> Order"""
    print("\n🧪 Test de synchronisation Payment -> Order...")
    
    # Créer un utilisateur admin
    admin_user = User.objects.create_user(
        username='admin_sync_test2',
        email='admin2@sync.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    
    # Créer un utilisateur client
    client_user = User.objects.create_user(
        username='client_sync_test2',
        email='client2@sync.com',
        password='testpass123'
    )
    
    # Créer une commande
    order = Order.objects.create(
        user=client_user,
        order_number='SYNC002',
        status='pending',
        payment_status='pending',
        subtotal=10000,
        shipping_cost=1000,
        total=11000
    )
    
    # Créer un paiement
    payment = Payment.objects.create(
        order=order,
        payment_id='PAY_SYNC002',
        amount=11000,
        status='pending',
        payment_method='wave_direct',
        customer_name='Test Client 2',
        customer_email='client2@sync.com',
        customer_phone='0575984322'
    )
    
    print(f"✅ Commande créée: {order.order_number}")
    print(f"✅ Paiement créé: {payment.id}")
    print(f"📊 Statut initial - Order: {order.payment_status}, Payment: {payment.status}")
    
    # Tester la synchronisation Payment -> Order
    success = sync_payment_order_status(payment, 'completed', updated_by=admin_user)
    
    # Vérifier les résultats
    order.refresh_from_db()
    payment.refresh_from_db()
    
    print(f"📊 Statut après sync - Order: {order.payment_status}, Payment: {payment.status}")
    
    # Vérifications
    test_success = True
    
    if not success:
        print("❌ ERREUR: La synchronisation a échoué")
        test_success = False
    else:
        print("✅ La synchronisation a réussi")
    
    if order.payment_status != 'paid':
        print("❌ ERREUR: Le statut de la commande n'a pas été mis à jour vers 'paid'")
        test_success = False
    else:
        print("✅ Le statut de la commande a été mis à jour vers 'paid'")
    
    if not order.paid_at:
        print("❌ ERREUR: La date de paiement n'a pas été définie")
        test_success = False
    else:
        print("✅ La date de paiement a été définie")
    
    # Nettoyage
    order.delete()
    admin_user.delete()
    client_user.delete()
    
    if test_success:
        print("🎉 Test de synchronisation Payment -> Order: SUCCÈS")
    else:
        print("💥 Test de synchronisation Payment -> Order: ÉCHEC")
    
    return test_success

def test_cancel_order_and_payment():
    """Test d'annulation de commande et paiement"""
    print("\n🧪 Test d'annulation de commande et paiement...")
    
    # Créer un utilisateur admin
    admin_user = User.objects.create_user(
        username='admin_cancel_test',
        email='admin@cancel.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    
    # Créer un utilisateur client
    client_user = User.objects.create_user(
        username='client_cancel_test',
        email='client@cancel.com',
        password='testpass123'
    )
    
    # Créer une commande
    order = Order.objects.create(
        user=client_user,
        order_number='CANCEL001',
        status='processing',
        payment_status='paid',
        subtotal=10000,
        shipping_cost=1000,
        total=11000
    )
    
    # Créer un paiement
    payment = Payment.objects.create(
        order=order,
        payment_id='PAY_CANCEL001',
        amount=11000,
        status='completed',
        payment_method='wave_direct',
        customer_name='Test Client Cancel',
        customer_email='client@cancel.com',
        customer_phone='0575984322'
    )
    
    print(f"✅ Commande créée: {order.order_number}")
    print(f"✅ Paiement créé: {payment.id}")
    print(f"📊 Statut initial - Order: {order.status}/{order.payment_status}, Payment: {payment.status}")
    
    # Tester l'annulation
    cancel_order_and_payment(order, updated_by=admin_user)
    
    # Vérifier les résultats
    order.refresh_from_db()
    payment.refresh_from_db()
    
    print(f"📊 Statut après annulation - Order: {order.status}/{order.payment_status}, Payment: {payment.status}")
    
    # Vérifications
    test_success = True
    
    if order.status != 'cancelled':
        print("❌ ERREUR: Le statut de la commande n'a pas été mis à jour vers 'cancelled'")
        test_success = False
    else:
        print("✅ Le statut de la commande a été mis à jour vers 'cancelled'")
    
    if order.payment_status != 'refunded':
        print("❌ ERREUR: Le statut de paiement de la commande n'a pas été mis à jour vers 'refunded'")
        test_success = False
    else:
        print("✅ Le statut de paiement de la commande a été mis à jour vers 'refunded'")
    
    if payment.status != 'cancelled':
        print("❌ ERREUR: Le statut du paiement n'a pas été mis à jour vers 'cancelled'")
        test_success = False
    else:
        print("✅ Le statut du paiement a été mis à jour vers 'cancelled'")
    
    # Nettoyage
    order.delete()
    admin_user.delete()
    client_user.delete()
    
    if test_success:
        print("🎉 Test d'annulation: SUCCÈS")
    else:
        print("💥 Test d'annulation: ÉCHEC")
    
    return test_success

def test_consistency_report():
    """Test du rapport de cohérence"""
    print("\n🧪 Test du rapport de cohérence...")
    
    # Créer des données de test avec incohérence
    admin_user = User.objects.create_user(
        username='admin_report_test',
        email='admin@report.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    
    client_user = User.objects.create_user(
        username='client_report_test',
        email='client@report.com',
        password='testpass123'
    )
    
    # Créer une commande avec incohérence
    order = Order.objects.create(
        user=client_user,
        order_number='REPORT001',
        status='pending',
        payment_status='paid',  # Incohérence: commande payée
        subtotal=10000,
        shipping_cost=1000,
        total=11000
    )
    
    # Créer un paiement avec statut différent
    payment = Payment.objects.create(
        order=order,
        payment_id='PAY_REPORT001',
        amount=11000,
        status='pending',  # Incohérence: paiement en attente
        payment_method='wave_direct',
        customer_name='Test Client Report',
        customer_email='client@report.com',
        customer_phone='0575984322'
    )
    
    print(f"✅ Commande créée avec incohérence: {order.order_number}")
    print(f"📊 Incohérence - Order: {order.payment_status}, Payment: {payment.status}")
    
    # Tester le rapport de cohérence
    inconsistencies = get_status_consistency_report()
    
    print(f"📊 Incohérences détectées: {len(inconsistencies)}")
    
    # Vérifications
    test_success = True
    
    if len(inconsistencies) == 0:
        print("❌ ERREUR: Aucune incohérence détectée alors qu'il devrait y en avoir une")
        test_success = False
    else:
        print("✅ Incohérence détectée correctement")
        
        # Vérifier les détails de l'incohérence
        inconsistency = inconsistencies[0]
        if inconsistency['order_id'] != order.id:
            print("❌ ERREUR: Mauvais ID de commande dans le rapport")
            test_success = False
        else:
            print("✅ Détails de l'incohérence corrects")
    
    # Nettoyage
    order.delete()
    admin_user.delete()
    client_user.delete()
    
    if test_success:
        print("🎉 Test du rapport de cohérence: SUCCÈS")
    else:
        print("💥 Test du rapport de cohérence: ÉCHEC")
    
    return test_success

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de synchronisation Order/Payment")
    print("=" * 60)
    
    tests = [
        test_sync_order_to_payment,
        test_sync_payment_to_order,
        test_cancel_order_and_payment,
        test_consistency_report,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"💥 Erreur lors du test {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS FINAUX")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests réussis: {passed}/{total}")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ La synchronisation Order/Payment fonctionne parfaitement")
    else:
        print("💥 CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Vérifiez les erreurs ci-dessus")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
