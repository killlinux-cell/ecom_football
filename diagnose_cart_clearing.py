#!/usr/bin/env python
"""
Script pour diagnostiquer le problème de vidage des paniers
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def diagnose_cart_clearing():
    """Diagnostique le problème de vidage des paniers"""
    print("🔍 DIAGNOSTIC DU VIDAGE DES PANIERS")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        from orders.models import Order
        from django.contrib.auth.models import User
        
        # Vérifier les paniers avec des articles
        carts_with_items = Cart.objects.filter(items__isnull=False).distinct()
        print(f"📊 {carts_with_items.count()} panier(s) avec des articles")
        
        for cart in carts_with_items:
            print(f"\n🛒 Panier ID: {cart.id}")
            print(f"   - Utilisateur: {cart.user.username if cart.user else 'Session'}")
            print(f"   - Articles: {cart.items.count()}")
            
            # Vérifier si l'utilisateur a des commandes récentes
            if cart.user:
                recent_orders = Order.objects.filter(
                    user=cart.user
                ).order_by('-created_at')[:3]
                
                print(f"   - Commandes récentes: {recent_orders.count()}")
                for order in recent_orders:
                    print(f"     * {order.order_number} - {order.created_at.strftime('%d/%m/%Y %H:%M')}")
            
            # Afficher les articles du panier
            for item in cart.items.all():
                print(f"   📦 {item.product.name} - {item.quantity}x - {item.total_price} FCFA")
        
        # Vérifier les paniers orphelins (sans utilisateur)
        orphaned_carts = Cart.objects.filter(user__isnull=True, session_key__isnull=True)
        print(f"\n👻 {orphaned_carts.count()} panier(s) orphelin(s)")
        
        # Vérifier les articles de panier sans panier parent
        orphaned_items = CartItem.objects.filter(cart__isnull=True)
        print(f"👻 {orphaned_items.count()} article(s) orphelin(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {str(e)}")
        return False

def fix_cart_clearing():
    """Corrige le problème de vidage des paniers"""
    print("\n🔧 CORRECTION DU VIDAGE DES PANIERS")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        from orders.models import Order
        from django.contrib.auth.models import User
        from django.utils import timezone
        from datetime import timedelta
        
        # Nettoyer les paniers avec des commandes récentes
        cleaned_count = 0
        
        for cart in Cart.objects.filter(items__isnull=False):
            if cart.user:
                # Vérifier si l'utilisateur a des commandes récentes
                recent_orders = Order.objects.filter(
                    user=cart.user,
                    created_at__gte=timezone.now() - timedelta(days=7)
                ).exists()
                
                if recent_orders:
                    print(f"🧹 Nettoyage du panier {cart.id} (utilisateur: {cart.user.username})")
                    cart.items.all().delete()
                    cleaned_count += 1
        
        print(f"\n📊 {cleaned_count} panier(s) nettoyé(s)")
        
        # Nettoyer les paniers orphelins
        orphaned_carts = Cart.objects.filter(user__isnull=True, session_key__isnull=True)
        orphaned_count = orphaned_carts.count()
        orphaned_carts.delete()
        print(f"👻 {orphaned_count} panier(s) orphelin(s) supprimé(s)")
        
        # Nettoyer les articles orphelins
        orphaned_items = CartItem.objects.filter(cart__isnull=True)
        orphaned_items_count = orphaned_items.count()
        orphaned_items.delete()
        print(f"👻 {orphaned_items_count} article(s) orphelin(s) supprimé(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC ET CORRECTION DU VIDAGE DES PANIERS")
    print("=" * 60)
    
    # Diagnostiquer
    success1 = diagnose_cart_clearing()
    
    if success1:
        print(f"\n❓ Voulez-vous nettoyer les paniers orphelins? (y/n)")
        response = input()
        
        if response.lower() == 'y':
            success2 = fix_cart_clearing()
            
            if success2:
                print("\n🎉 NETTOYAGE TERMINÉ!")
                print("✅ Les paniers orphelins ont été nettoyés")
            else:
                print("\n💥 NETTOYAGE ÉCHOUÉ!")
        else:
            print("\n✅ Diagnostic terminé sans nettoyage")
    else:
        print("\n💥 DIAGNOSTIC ÉCHOUÉ!")
    
    return success1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
