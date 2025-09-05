#!/usr/bin/env python
"""
Script pour corriger les incohérences de totaux dans les commandes
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def analyser_commande_CMD202509051142422():
    """Analyser la commande CMD202509051142422"""
    print("🔍 ANALYSE DE LA COMMANDE CMD202509051142422")
    print("=" * 60)
    
    try:
        from orders.models import Order, OrderItem
        
        # Récupérer la commande
        order = Order.objects.filter(order_number='CMD202509051142422').first()
        
        if not order:
            print("❌ Commande CMD202509051142422 non trouvée")
            print("📋 Commandes disponibles:")
            orders = Order.objects.all().order_by('-created_at')[:10]
            for o in orders:
                print(f"   - {o.order_number} ({o.created_at.strftime('%d/%m/%Y %H:%M')})")
            return False
        
        print(f"✅ Commande trouvée:")
        print(f"   - Numéro: {order.order_number}")
        print(f"   - Utilisateur: {order.user.username}")
        print(f"   - Date: {order.created_at}")
        print(f"   - Statut: {order.status}")
        print(f"   - Sous-total: {order.subtotal} FCFA")
        print(f"   - Frais livraison: {order.shipping_cost} FCFA")
        print(f"   - Total: {order.total} FCFA")
        
        # Analyser les articles de la commande
        print(f"\n📦 ARTICLES DE LA COMMANDE:")
        order_items = order.items.all()
        print(f"   Nombre d'articles: {order_items.count()}")
        
        total_calculated = 0
        for item in order_items:
            print(f"\n   📋 Article: {item.product_name}")
            print(f"      - Taille: {item.size}")
            print(f"      - Quantité: {item.quantity}")
            print(f"      - Prix unitaire: {item.price} FCFA")
            print(f"      - Prix total article: {item.total_price} FCFA")
            
            # Vérifier les personnalisations
            try:
                customizations = item.customizations.all()
                if customizations:
                    print(f"      - Personnalisations ({customizations.count()}):")
                    for custom in customizations:
                        print(f"        • {custom.customization.name}: {custom.custom_text} - {custom.price} FCFA")
                else:
                    print(f"      - Aucune personnalisation")
            except:
                print(f"      - Erreur lors de la récupération des personnalisations")
            
            total_calculated += item.total_price
        
        print(f"\n🧮 CALCULS:")
        print(f"   - Total calculé à partir des articles: {total_calculated} FCFA")
        print(f"   - Sous-total enregistré: {order.subtotal} FCFA")
        print(f"   - Différence: {total_calculated - order.subtotal} FCFA")
        
        # Vérifier s'il y a des articles manquants
        if abs(total_calculated - order.subtotal) > 0.01:
            print(f"\n⚠️ INCOHÉRENCE DÉTECTÉE!")
            print(f"   Le sous-total enregistré ({order.subtotal}) ne correspond pas")
            print(f"   au total des articles ({total_calculated})")
            
            # Analyser les possibles causes
            print(f"\n🔍 ANALYSE DES CAUSES POSSIBLES:")
            
            # 1. Vérifier s'il y a des articles supprimés
            print(f"   1. Articles supprimés après création de la commande")
            
            # 2. Vérifier les personnalisations
            try:
                total_customizations = sum(
                    sum(cust.price for cust in item.customizations.all())
                    for item in order_items
                )
                print(f"   2. Total personnalisations: {total_customizations} FCFA")
            except:
                print(f"   2. Erreur lors du calcul des personnalisations")
            
            # 3. Vérifier le prix de base vs prix total
            total_base_price = sum(item.price * item.quantity for item in order_items)
            print(f"   3. Total prix de base: {total_base_price} FCFA")
            print(f"   4. Total avec personnalisations: {total_calculated} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def corriger_commande_CMD202509051142422():
    """Corriger la commande CMD202509051142422"""
    print("\n🔧 CORRECTION DE LA COMMANDE")
    print("=" * 40)
    
    try:
        from orders.models import Order
        from decimal import Decimal
        
        order = Order.objects.filter(order_number='CMD202509051142422').first()
        
        if not order:
            print("❌ Commande non trouvée")
            return False
        
        # Calculer le bon sous-total
        correct_subtotal = sum(item.total_price for item in order.items.all())
        
        print(f"📊 Correction:")
        print(f"   - Ancien sous-total: {order.subtotal} FCFA")
        print(f"   - Nouveau sous-total: {correct_subtotal} FCFA")
        print(f"   - Différence: {correct_subtotal - order.subtotal} FCFA")
        
        # Mettre à jour
        old_subtotal = order.subtotal
        order.subtotal = correct_subtotal
        order.total = correct_subtotal + order.shipping_cost
        order.save()
        
        print(f"✅ Commande corrigée:")
        print(f"   - Sous-total: {order.subtotal} FCFA")
        print(f"   - Total: {order.total} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def analyser_toutes_les_commandes():
    """Analyser toutes les commandes pour détecter les incohérences"""
    print("\n🔍 ANALYSE DE TOUTES LES COMMANDES")
    print("=" * 60)
    
    try:
        from orders.models import Order
        
        orders = Order.objects.all().order_by('-created_at')
        print(f"📊 {orders.count()} commandes trouvées")
        
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
                print(f"   - Date: {order.created_at.strftime('%d/%m/%Y %H:%M')}")
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"   - Total commandes: {orders.count()}")
        print(f"   - Commandes incohérentes: {incohérentes}")
        if orders.count() > 0:
            print(f"   - Pourcentage: {(incohérentes/orders.count()*100):.1f}%")
        
        return incohérentes == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC DES INCOHÉRENCES DE TOTAUX")
    print("=" * 60)
    
    # Analyser la commande spécifique
    success1 = analyser_commande_CMD202509051142422()
    
    # Analyser toutes les commandes
    success2 = analyser_toutes_les_commandes()
    
    # Proposer la correction
    if not success2:
        print("\n💡 CORRECTION RECOMMANDÉE")
        print("=" * 40)
        response = input("Voulez-vous corriger la commande CMD202509051142422? (y/n): ")
        if response.lower() == 'y':
            corriger_commande_CMD202509051142422()
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
