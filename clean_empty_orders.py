#!/usr/bin/env python
"""
Script pour nettoyer les commandes sans articles
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def clean_empty_orders():
    """Supprime les commandes sans articles"""
    print("🧹 NETTOYAGE DES COMMANDES SANS ARTICLES")
    print("=" * 60)
    
    try:
        from orders.models import Order
        
        # Trouver les commandes sans articles
        orders_without_items = Order.objects.filter(items__isnull=True).distinct()
        
        print(f"📊 {orders_without_items.count()} commande(s) sans articles trouvée(s)")
        
        if orders_without_items.count() == 0:
            print("✅ Aucune commande à nettoyer")
            return True
        
        # Afficher les commandes à supprimer
        print("\n🗑️ Commandes à supprimer:")
        for order in orders_without_items:
            print(f"   - {order.order_number} ({order.created_at.strftime('%d/%m/%Y %H:%M')}) - {order.user.username}")
        
        # Demander confirmation
        response = input(f"\nVoulez-vous supprimer ces {orders_without_items.count()} commandes? (y/n): ")
        
        if response.lower() == 'y':
            deleted_count = 0
            for order in orders_without_items:
                print(f"🗑️ Suppression de {order.order_number}...")
                order.delete()
                deleted_count += 1
            
            print(f"\n✅ {deleted_count} commande(s) supprimée(s) avec succès!")
            return True
        else:
            print("❌ Suppression annulée")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {str(e)}")
        return False

def main():
    """Fonction principale"""
    success = clean_empty_orders()
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
