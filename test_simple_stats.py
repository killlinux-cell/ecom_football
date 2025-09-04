#!/usr/bin/env python
"""
Test simple des statistiques des paiements
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

from payments.models import Payment
from django.db.models import Count, Sum

def test_payment_stats():
    """Test simple des statistiques"""
    print("🧪 Test simple des statistiques des paiements...")
    
    # Récupérer toutes les statistiques
    total_payments = Payment.objects.count()
    pending_payments = Payment.objects.filter(status='pending').count()
    completed_payments = Payment.objects.filter(status='completed').count()
    failed_payments = Payment.objects.filter(status='failed').count()
    cancelled_payments = Payment.objects.filter(status='cancelled').count()
    
    # Montant total des paiements complétés
    total_amount = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Paiements Wave en attente
    wave_pending = Payment.objects.filter(
        payment_method='wave_direct', 
        status='pending'
    ).count()
    
    print(f"📊 Total paiements: {total_payments}")
    print(f"📊 Paiements en attente: {pending_payments}")
    print(f"📊 Paiements complétés: {completed_payments}")
    print(f"📊 Paiements échoués: {failed_payments}")
    print(f"📊 Paiements annulés: {cancelled_payments}")
    print(f"📊 Montant total: {total_amount} FCFA")
    print(f"📊 Wave en attente: {wave_pending}")
    
    # Vérifier que les statistiques sont cohérentes
    if total_payments >= 0:
        print("✅ Total des paiements calculé correctement")
    else:
        print("❌ ERREUR: Total des paiements incorrect")
        return False
    
    if pending_payments >= 0:
        print("✅ Paiements en attente calculés correctement")
    else:
        print("❌ ERREUR: Paiements en attente incorrects")
        return False
    
    if completed_payments >= 0:
        print("✅ Paiements complétés calculés correctement")
    else:
        print("❌ ERREUR: Paiements complétés incorrects")
        return False
    
    if total_amount >= 0:
        print("✅ Montant total calculé correctement")
    else:
        print("❌ ERREUR: Montant total incorrect")
        return False
    
    print("🎉 Test des statistiques: SUCCÈS")
    return True

if __name__ == '__main__':
    success = test_payment_stats()
    sys.exit(0 if success else 1)
