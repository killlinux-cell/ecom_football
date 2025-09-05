#!/usr/bin/env python
"""
Script pour corriger l'incohérence entre quantité affichée et quantité en base
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_cart_quantity_mismatch():
    """Corrige l'incohérence entre quantité affichée et quantité en base"""
    print("🔧 CORRECTION DE L'INCOHÉRENCE DE QUANTITÉ")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        from django.contrib.auth.models import User
        
        # Trouver tous les paniers avec des incohérences
        users_with_carts = User.objects.filter(cart__items__isnull=False).distinct()
        
        print(f"📊 {users_with_carts.count()} utilisateur(s) avec panier(s)")
        
        for user in users_with_carts:
            print(f"\n👤 Utilisateur: {user.username}")
            
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                continue
            
            print(f"🛒 Panier ID: {cart.id}")
            
            for item in cart.items.all():
                print(f"\n   📦 Article: {item.product.name}")
                print(f"      - Quantité en base: {item.quantity}")
                print(f"      - Prix unitaire: {item.product.price} FCFA")
                print(f"      - Prix total: {item.total_price} FCFA")
                
                # Calculer la quantité attendue
                expected_quantity = int(item.total_price / item.product.price)
                print(f"      - Quantité attendue: {expected_quantity}")
                
                if item.quantity != expected_quantity:
                    print(f"      ⚠️ INCOHÉRENCE DÉTECTÉE!")
                    print(f"         Quantité affichée: {item.quantity}")
                    print(f"         Quantité réelle: {expected_quantity}")
                    
                    # Corriger la quantité
                    item.quantity = expected_quantity
                    item.save()
                    
                    print(f"      ✅ Quantité corrigée: {item.quantity}")
                else:
                    print(f"      ✅ Quantité cohérente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def clear_all_carts():
    """Vide tous les paniers pour repartir à zéro"""
    print("\n🧹 VIDAGE DE TOUS LES PANIERS")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        
        # Compter les articles
        total_items = CartItem.objects.count()
        print(f"📊 {total_items} article(s) dans les paniers")
        
        if total_items > 0:
            # Vider tous les paniers
            CartItem.objects.all().delete()
            print(f"✅ {total_items} article(s) supprimé(s)")
        else:
            print("✅ Aucun article à supprimer")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du vidage: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION DE L'INCOHÉRENCE DE QUANTITÉ")
    print("=" * 60)
    
    # Corriger les incohérences
    success1 = fix_cart_quantity_mismatch()
    
    # Optionnel: vider tous les paniers
    print(f"\n❓ Voulez-vous vider tous les paniers pour repartir à zéro? (y/n)")
    response = input()
    
    if response.lower() == 'y':
        success2 = clear_all_carts()
        
        if success1 and success2:
            print("\n🎉 CORRECTION TERMINÉE!")
            print("✅ Les incohérences ont été corrigées")
            print("✅ Tous les paniers ont été vidés")
        else:
            print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
    else:
        if success1:
            print("\n🎉 CORRECTION TERMINÉE!")
            print("✅ Les incohérences ont été corrigées")
        else:
            print("\n💥 CORRECTION ÉCHOUÉE!")
    
    return success1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
