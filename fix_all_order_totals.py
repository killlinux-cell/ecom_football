#!/usr/bin/env python
"""
Script pour corriger toutes les incohérences de totaux dans les commandes
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def corriger_toutes_les_commandes():
    """Corriger toutes les commandes avec des incohérences"""
    print("🔧 CORRECTION DE TOUTES LES COMMANDES INCOHÉRENTES")
    print("=" * 60)
    
    try:
        from orders.models import Order
        from decimal import Decimal
        
        orders = Order.objects.all()
        print(f"📊 {orders.count()} commandes à vérifier")
        
        corrigées = 0
        incohérentes = 0
        
        for order in orders:
            # Calculer le total à partir des articles
            total_articles = sum(item.total_price for item in order.items.all())
            
            # Vérifier l'incohérence
            if abs(total_articles - order.subtotal) > 0.01:  # Tolérance de 1 centime
                incohérentes += 1
                print(f"\n⚠️ Commande {order.order_number}:")
                print(f"   - Sous-total enregistré: {order.subtotal} FCFA")
                print(f"   - Total articles: {total_articles} FCFA")
                print(f"   - Différence: {total_articles - order.subtotal} FCFA")
                
                # Corriger la commande
                old_subtotal = order.subtotal
                old_total = order.total
                
                order.subtotal = total_articles
                order.total = total_articles + order.shipping_cost
                order.save()
                
                print(f"   ✅ Corrigée:")
                print(f"      - Nouveau sous-total: {order.subtotal} FCFA")
                print(f"      - Nouveau total: {order.total} FCFA")
                
                corrigées += 1
        
        print(f"\n📊 RÉSUMÉ DE LA CORRECTION:")
        print(f"   - Commandes vérifiées: {orders.count()}")
        print(f"   - Commandes incohérentes: {incohérentes}")
        print(f"   - Commandes corrigées: {corrigées}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def analyser_commande_exemple():
    """Analyser une commande d'exemple pour comprendre le problème"""
    print("\n🔍 ANALYSE D'UNE COMMANDE D'EXEMPLE")
    print("=" * 60)
    
    try:
        from orders.models import Order
        
        # Prendre la première commande incohérente
        orders = Order.objects.all()
        for order in orders:
            total_articles = sum(item.total_price for item in order.items.all())
            if abs(total_articles - order.subtotal) > 0.01:
                print(f"📋 Commande analysée: {order.order_number}")
                print(f"   - Date: {order.created_at}")
                print(f"   - Utilisateur: {order.user.username}")
                print(f"   - Sous-total: {order.subtotal} FCFA")
                print(f"   - Total articles: {total_articles} FCFA")
                print(f"   - Nombre d'articles: {order.items.count()}")
                
                # Analyser les articles
                if order.items.count() == 0:
                    print(f"   ⚠️ PROBLÈME: Aucun article dans la commande!")
                    print(f"      Cela suggère que les articles ont été supprimés")
                    print(f"      après la création de la commande.")
                else:
                    print(f"   📦 Articles présents:")
                    for item in order.items.all():
                        print(f"      - {item.product_name}: {item.total_price} FCFA")
                
                break
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        return False

def prévenir_le_problème():
    """Suggérer des solutions pour prévenir le problème"""
    print("\n💡 SOLUTIONS POUR PRÉVENIR LE PROBLÈME")
    print("=" * 60)
    
    print("🔧 Solutions recommandées:")
    print("   1. Vérification des totaux lors de la création de commande")
    print("   2. Recalcul automatique des totaux si articles supprimés")
    print("   3. Validation des données avant sauvegarde")
    print("   4. Logs des modifications de commandes")
    
    print("\n📋 Modifications de code suggérées:")
    print("   1. Dans orders/views.py - Vérifier la cohérence avant sauvegarde")
    print("   2. Dans orders/models.py - Ajouter une méthode de validation")
    print("   3. Créer une commande de maintenance pour recalculer les totaux")
    
    return True

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC ET CORRECTION DES INCOHÉRENCES DE TOTAUX")
    print("=" * 70)
    
    # Analyser une commande d'exemple
    analyser_commande_exemple()
    
    # Corriger toutes les commandes
    print("\n" + "="*70)
    response = input("Voulez-vous corriger toutes les commandes incohérentes? (y/n): ")
    if response.lower() == 'y':
        corriger_toutes_les_commandes()
    
    # Suggérer des solutions
    prévenir_le_problème()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
