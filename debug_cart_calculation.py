#!/usr/bin/env python
"""
Script pour diagnostiquer le calcul du panier
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def debug_cart_calculation():
    """Diagnostique le calcul du panier"""
    print("🔍 DIAGNOSTIC DU CALCUL DU PANIER")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        from products.models import Product
        from django.contrib.auth.models import User
        
        # Trouver un utilisateur avec un panier
        users_with_carts = User.objects.filter(cart__items__isnull=False).distinct()
        
        if not users_with_carts.exists():
            print("❌ Aucun utilisateur avec un panier trouvé")
            return False
        
        for user in users_with_carts:
            print(f"\n👤 Utilisateur: {user.username}")
            
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                continue
            
            print(f"🛒 Panier ID: {cart.id}")
            print(f"   - Articles: {cart.items.count()}")
            
            total_calculated = 0
            
            for item in cart.items.all():
                print(f"\n   📦 Article: {item.product.name}")
                print(f"      - Prix unitaire: {item.product.price} FCFA")
                print(f"      - Quantité: {item.quantity}")
                print(f"      - Prix de base: {item.base_price} FCFA")
                print(f"      - Prix personnalisations: {item.customization_price} FCFA")
                print(f"      - Prix total: {item.total_price} FCFA")
                
                # Vérifier le calcul
                expected_base = item.product.price * item.quantity
                expected_total = expected_base + item.customization_price
                
                print(f"      - Prix de base attendu: {expected_base} FCFA")
                print(f"      - Prix total attendu: {expected_total} FCFA")
                
                if item.base_price == expected_base:
                    print(f"      ✅ Prix de base correct")
                else:
                    print(f"      ❌ Prix de base incorrect (différence: {item.base_price - expected_base} FCFA)")
                
                if item.total_price == expected_total:
                    print(f"      ✅ Prix total correct")
                else:
                    print(f"      ❌ Prix total incorrect (différence: {item.total_price - expected_total} FCFA)")
                
                total_calculated += item.total_price
            
            print(f"\n   💰 Total calculé: {total_calculated} FCFA")
            
            # Vérifier le total du panier
            cart_total = cart.get_total_price()
            print(f"   💰 Total du panier: {cart_total} FCFA")
            
            if total_calculated == cart_total:
                print(f"   ✅ Total cohérent")
            else:
                print(f"   ❌ Total incohérent (différence: {total_calculated - cart_total} FCFA)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {str(e)}")
        return False

def fix_cart_calculations():
    """Corrige les calculs du panier"""
    print("\n🔧 CORRECTION DES CALCULS DU PANIER")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        
        carts = Cart.objects.all()
        print(f"📊 {carts.count()} panier(s) trouvé(s)")
        
        corrected_count = 0
        
        for cart in carts:
            for item in cart.items.all():
                # Recalculer le prix de base
                expected_base = item.product.price * item.quantity
                expected_total = expected_base + item.customization_price
                
                if item.total_price != expected_total:
                    print(f"🔧 Correction: {item.product.name}")
                    print(f"   - Ancien total: {item.total_price} FCFA")
                    print(f"   - Nouveau total: {expected_total} FCFA")
                    
                    # Forcer la sauvegarde pour recalculer
                    item.save()
                    corrected_count += 1
        
        print(f"\n📊 {corrected_count} article(s) corrigé(s)")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC ET CORRECTION DU CALCUL DU PANIER")
    print("=" * 60)
    
    # Diagnostiquer
    success1 = debug_cart_calculation()
    
    # Corriger si nécessaire
    if success1:
        success2 = fix_cart_calculations()
        
        if success2:
            print("\n🎉 DIAGNOSTIC ET CORRECTION TERMINÉS!")
            print("✅ Les calculs du panier ont été vérifiés et corrigés")
        else:
            print("\n💥 CORRECTION ÉCHOUÉE!")
            print("❌ Des problèmes persistent")
    else:
        print("\n💥 DIAGNOSTIC ÉCHOUÉ!")
        print("❌ Impossible de diagnostiquer le problème")
    
    return success1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
