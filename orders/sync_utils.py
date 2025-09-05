"""
Utilitaires de synchronisation entre Order et Payment
"""

from django.utils import timezone
from django.db import transaction
from orders.models import Order
from payments.models import Payment, PaymentLog


def sync_order_payment_status(order, new_payment_status, updated_by=None):
    """
    Synchronise le statut de paiement entre Order et Payment
    
    Args:
        order: Instance de Order
        new_payment_status: Nouveau statut de paiement ('pending', 'paid', 'failed', 'refunded')
        updated_by: Utilisateur qui a effectué la mise à jour (optionnel)
    """
    try:
        payment = Payment.objects.get(order=order)
        old_payment_status = payment.status
        
        # CORRECTION: Vérifier que le montant du paiement correspond au total de la commande
        if payment.amount != order.total:
            PaymentLog.objects.create(
                payment=payment,
                event='amount_mismatch_detected',
                message=f'Incohérence de montant détectée: Paiement={payment.amount}, Commande={order.total}',
                data={
                    'payment_amount': float(payment.amount),
                    'order_total': float(order.total),
                    'difference': float(order.total - payment.amount)
                }
            )
            
            # Corriger le montant du paiement
            payment.amount = order.total
            payment.save()
            
            PaymentLog.objects.create(
                payment=payment,
                event='amount_corrected',
                message=f'Montant du paiement corrigé: {payment.amount} FCFA',
                data={
                    'corrected_amount': float(payment.amount),
                    'order_total': float(order.total)
                }
            )
        
        # Mapping des statuts Order -> Payment
        status_mapping = {
            'pending': 'pending',
            'paid': 'completed',
            'failed': 'failed',
            'refunded': 'cancelled'  # On considère remboursé = annulé pour Payment
        }
        
        new_payment_status_mapped = status_mapping.get(new_payment_status, 'pending')
        
        # Mettre à jour le statut du paiement
        payment.status = new_payment_status_mapped
        
        # Mettre à jour les dates selon le statut
        if new_payment_status == 'paid' and old_payment_status != 'completed':
            payment.completed_at = timezone.now()
        elif new_payment_status in ['failed', 'refunded']:
            payment.completed_at = None
        
        payment.save()
        
        # Créer un log de synchronisation
        PaymentLog.objects.create(
            payment=payment,
            event='status_synchronized',
            message=f'Statut synchronisé: {old_payment_status} -> {new_payment_status_mapped} (Order: {new_payment_status})',
            data={
                'updated_by': updated_by.username if updated_by else 'system',
                'order_payment_status': new_payment_status,
                'payment_status': new_payment_status_mapped,
                'old_payment_status': old_payment_status
            }
        )
        
        return True
        
    except Payment.DoesNotExist:
        # Pas de paiement associé, c'est normal pour certaines commandes
        return False
    except Exception as e:
        # Log l'erreur mais ne pas faire échouer la transaction
        print(f"Erreur lors de la synchronisation du paiement pour la commande {order.id}: {e}")
        return False


def sync_payment_order_status(payment, new_payment_status, updated_by=None):
    """
    Synchronise le statut de paiement de Payment vers Order
    
    Args:
        payment: Instance de Payment
        new_payment_status: Nouveau statut de paiement ('pending', 'completed', 'failed', 'cancelled')
        updated_by: Utilisateur qui a effectué la mise à jour (optionnel)
    """
    try:
        order = payment.order
        old_order_payment_status = order.payment_status
        
        # Mapping des statuts Payment -> Order
        status_mapping = {
            'pending': 'pending',
            'completed': 'paid',
            'failed': 'failed',
            'cancelled': 'refunded'  # On considère annulé = remboursé pour Order
        }
        
        new_order_payment_status = status_mapping.get(new_payment_status, 'pending')
        
        # Mettre à jour le statut de paiement de la commande
        order.payment_status = new_order_payment_status
        
        # Mettre à jour les dates selon le statut
        if new_payment_status == 'completed' and old_order_payment_status != 'paid':
            order.paid_at = timezone.now()
        elif new_payment_status in ['failed', 'cancelled']:
            order.paid_at = None
        
        order.save()
        
        # Créer un log de synchronisation
        PaymentLog.objects.create(
            payment=payment,
            event='status_synchronized_reverse',
            message=f'Statut synchronisé (Payment->Order): {new_payment_status} -> {new_order_payment_status}',
            data={
                'updated_by': updated_by.username if updated_by else 'system',
                'payment_status': new_payment_status,
                'order_payment_status': new_order_payment_status,
                'old_order_payment_status': old_order_payment_status
            }
        )
        
        return True
        
    except Exception as e:
        # Log l'erreur mais ne pas faire échouer la transaction
        print(f"Erreur lors de la synchronisation de la commande pour le paiement {payment.id}: {e}")
        return False


def cancel_order_and_payment(order, updated_by=None):
    """
    Annule une commande et son paiement associé
    
    Args:
        order: Instance de Order
        updated_by: Utilisateur qui a effectué l'annulation (optionnel)
    """
    with transaction.atomic():
        # Annuler la commande
        order.status = 'cancelled'
        order.payment_status = 'refunded'
        order.save()
        
        # Annuler le paiement associé s'il existe
        try:
            payment = Payment.objects.get(order=order)
            payment.status = 'cancelled'
            payment.save()
            
            # Log de l'annulation
            PaymentLog.objects.create(
                payment=payment,
                event='order_and_payment_cancelled',
                message=f'Commande et paiement annulés par {updated_by.username if updated_by else "system"}',
                data={
                    'updated_by': updated_by.username if updated_by else 'system',
                    'order_id': order.id,
                    'payment_id': payment.id
                }
            )
            
        except Payment.DoesNotExist:
            # Pas de paiement associé, c'est normal
            pass


def validate_payment_and_order(payment, updated_by=None):
    """
    Valide un paiement et met à jour la commande associée
    
    Args:
        payment: Instance de Payment
        updated_by: Utilisateur qui a effectué la validation (optionnel)
    """
    with transaction.atomic():
        # Valider le paiement
        payment.status = 'completed'
        payment.completed_at = timezone.now()
        payment.save()
        
        # Mettre à jour la commande
        order = payment.order
        order.payment_status = 'paid'
        order.paid_at = timezone.now()
        order.save()
        
        # Log de la validation
        PaymentLog.objects.create(
            payment=payment,
            event='payment_and_order_validated',
            message=f'Paiement et commande validés par {updated_by.username if updated_by else "system"}',
            data={
                'updated_by': updated_by.username if updated_by else 'system',
                'order_id': order.id,
                'payment_id': payment.id
            }
        )


def get_status_consistency_report():
    """
    Génère un rapport des incohérences entre Order et Payment
    """
    inconsistencies = []
    
    # Récupérer toutes les commandes avec paiements
    orders_with_payments = Order.objects.filter(payment__isnull=False).select_related('payment')
    
    for order in orders_with_payments:
        payment = order.payment
        
        # Vérifier la cohérence des statuts
        expected_payment_status = None
        if order.payment_status == 'pending':
            expected_payment_status = 'pending'
        elif order.payment_status == 'paid':
            expected_payment_status = 'completed'
        elif order.payment_status == 'failed':
            expected_payment_status = 'failed'
        elif order.payment_status == 'refunded':
            expected_payment_status = 'cancelled'
        
        if expected_payment_status and payment.status != expected_payment_status:
            inconsistencies.append({
                'order_id': order.id,
                'order_number': order.order_number,
                'order_payment_status': order.payment_status,
                'payment_status': payment.status,
                'expected_payment_status': expected_payment_status,
                'inconsistency_type': 'status_mismatch'
            })
        
        # NOUVEAU: Vérifier la cohérence des montants
        if payment.amount != order.total:
            inconsistencies.append({
                'order_id': order.id,
                'order_number': order.order_number,
                'order_total': float(order.total),
                'payment_amount': float(payment.amount),
                'difference': float(order.total - payment.amount),
                'inconsistency_type': 'amount_mismatch'
            })
    
    return inconsistencies


def fix_amount_inconsistencies():
    """
    Corrige automatiquement les incohérences de montants entre Order et Payment
    """
    fixed_count = 0
    
    # Récupérer toutes les commandes avec paiements
    orders_with_payments = Order.objects.filter(payment__isnull=False).select_related('payment')
    
    for order in orders_with_payments:
        payment = order.payment
        
        # Vérifier et corriger les incohérences de montant
        if payment.amount != order.total:
            old_amount = payment.amount
            payment.amount = order.total
            payment.save()
            
            # Log de la correction
            PaymentLog.objects.create(
                payment=payment,
                event='amount_auto_corrected',
                message=f'Montant automatiquement corrigé: {old_amount} -> {order.total} FCFA',
                data={
                    'old_amount': float(old_amount),
                    'new_amount': float(order.total),
                    'order_total': float(order.total),
                    'difference': float(order.total - old_amount)
                }
            )
            
            fixed_count += 1
    
    return fixed_count
