#!/usr/bin/env python
"""
Script de test pour vérifier les corrections mobile et paiement
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
from django.utils import timezone

def test_payment_status_update():
    """Test de la mise à jour automatique du statut de paiement"""
    print("🧪 Test de la mise à jour automatique du statut de paiement...")
    
    # Créer un utilisateur admin
    admin_user = User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    
    # Créer un utilisateur client
    client_user = User.objects.create_user(
        username='client_test',
        email='client@test.com',
        password='testpass123'
    )
    
    # Créer une commande
    order = Order.objects.create(
        user=client_user,
        order_number='TEST001',
        status='pending',
        payment_status='pending',
        subtotal=10000,
        shipping_cost=1000,
        total=11000
    )
    
    # Créer un paiement Wave
    payment = Payment.objects.create(
        order=order,
        payment_method='wave_direct',
        amount=11000,
        status='pending',
        wave_transaction_id='WAVE123456',
        customer_phone='0575984322'
    )
    
    print(f"✅ Commande créée: {order.order_number}")
    print(f"✅ Paiement créé: {payment.id}")
    print(f"📊 Statut initial - Commande: {order.payment_status}, Paiement: {payment.status}")
    
    # Simuler la mise à jour par l'admin
    client = Client()
    client.force_login(admin_user)
    
    # Mettre à jour le statut de paiement via le dashboard
    response = client.post(
        reverse('dashboard:order_detail', args=[order.id]),
        {
            'status': 'processing',
            'payment_status': 'paid',
            'notes': 'Test de mise à jour automatique'
        }
    )
    
    # Vérifier les résultats
    order.refresh_from_db()
    payment.refresh_from_db()
    
    print(f"📊 Statut après mise à jour - Commande: {order.payment_status}, Paiement: {payment.status}")
    
    # Vérifications
    success = True
    
    if order.payment_status != 'paid':
        print("❌ ERREUR: Le statut de la commande n'a pas été mis à jour")
        success = False
    else:
        print("✅ Le statut de la commande a été mis à jour correctement")
    
    if payment.status != 'completed':
        print("❌ ERREUR: Le statut du paiement n'a pas été mis à jour automatiquement")
        success = False
    else:
        print("✅ Le statut du paiement a été mis à jour automatiquement")
    
    if not payment.completed_at:
        print("❌ ERREUR: La date de completion du paiement n'a pas été définie")
        success = False
    else:
        print("✅ La date de completion du paiement a été définie")
    
    # Vérifier le log
    logs = PaymentLog.objects.filter(payment=payment, event='payment_status_updated_by_admin')
    if not logs.exists():
        print("❌ ERREUR: Aucun log de mise à jour n'a été créé")
        success = False
    else:
        print("✅ Un log de mise à jour a été créé")
    
    # Nettoyage
    order.delete()
    admin_user.delete()
    client_user.delete()
    
    if success:
        print("🎉 Test de mise à jour automatique du statut de paiement: SUCCÈS")
    else:
        print("💥 Test de mise à jour automatique du statut de paiement: ÉCHEC")
    
    return success

def test_mobile_css_files():
    """Test de l'existence des fichiers CSS mobile"""
    print("\n🧪 Test de l'existence des fichiers CSS mobile...")
    
    css_files = [
        'static/css/mobile.css',
        'static/css/mobile-fixes.css'
    ]
    
    success = True
    
    for css_file in css_files:
        if os.path.exists(css_file):
            print(f"✅ Fichier trouvé: {css_file}")
        else:
            print(f"❌ Fichier manquant: {css_file}")
            success = False
    
    if success:
        print("🎉 Test des fichiers CSS mobile: SUCCÈS")
    else:
        print("💥 Test des fichiers CSS mobile: ÉCHEC")
    
    return success

def test_template_includes():
    """Test de l'inclusion des CSS dans les templates"""
    print("\n🧪 Test de l'inclusion des CSS dans les templates...")
    
    try:
        with open('templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        success = True
        
        if 'mobile.css' in content:
            print("✅ mobile.css inclus dans base.html")
        else:
            print("❌ mobile.css non inclus dans base.html")
            success = False
        
        if 'mobile-fixes.css' in content:
            print("✅ mobile-fixes.css inclus dans base.html")
        else:
            print("❌ mobile-fixes.css non inclus dans base.html")
            success = False
        
        if success:
            print("🎉 Test d'inclusion des CSS: SUCCÈS")
        else:
            print("💥 Test d'inclusion des CSS: ÉCHEC")
        
        return success
        
    except FileNotFoundError:
        print("❌ Fichier templates/base.html non trouvé")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de correction mobile et paiement")
    print("=" * 60)
    
    tests = [
        test_mobile_css_files,
        test_template_includes,
        test_payment_status_update,
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
        print("✅ Les corrections mobile et paiement sont fonctionnelles")
    else:
        print("💥 CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Vérifiez les erreurs ci-dessus")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
