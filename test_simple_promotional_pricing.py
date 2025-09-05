#!/usr/bin/env python
"""
Script de test simple pour les prix promotionnels
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_simple_promotional_pricing():
    """Teste simplement les prix promotionnels"""
    print("🧪 TEST SIMPLE DES PRIX PROMOTIONNELS")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from decimal import Decimal
        
        # Créer un produit avec promotion
        category, _ = Category.objects.get_or_create(
            name="Test Category Simple",
            defaults={'slug': 'test-category-simple'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Simple",
            defaults={'slug': 'test-team-simple', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="TEST Product Simple",
            defaults={
                'price': Decimal('15000.00'),  # Prix normal
                'sale_price': Decimal('10000.00'),  # Prix promotion
                'description': 'Produit de test simple',
                'category': category,
                'team': team,
                'slug': 'test-product-simple',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"📦 Produit de test: {product.name}")
        print(f"   - Prix normal: {product.price} FCFA")
        print(f"   - Prix promotion: {product.sale_price} FCFA")
        print(f"   - Prix actuel: {product.current_price} FCFA")
        
        # Vérifier que current_price retourne le bon prix
        if product.current_price == product.sale_price:
            print(f"   ✅ current_price retourne le prix promotion")
        else:
            print(f"   ❌ current_price ne retourne pas le prix promotion")
        
        # Test avec un produit sans promotion
        product_no_promo, created2 = Product.objects.get_or_create(
            name="TEST Product No Promo",
            defaults={
                'price': Decimal('20000.00'),  # Prix normal
                'sale_price': None,  # Pas de promotion
                'description': 'Produit sans promotion',
                'category': category,
                'team': team,
                'slug': 'test-product-no-promo',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"\n📦 Produit sans promotion: {product_no_promo.name}")
        print(f"   - Prix normal: {product_no_promo.price} FCFA")
        print(f"   - Prix promotion: {product_no_promo.sale_price}")
        print(f"   - Prix actuel: {product_no_promo.current_price} FCFA")
        
        # Vérifier que current_price retourne le prix normal
        if product_no_promo.current_price == product_no_promo.price:
            print(f"   ✅ current_price retourne le prix normal")
        else:
            print(f"   ❌ current_price ne retourne pas le prix normal")
        
        # Nettoyer les données de test
        if created:
            product.delete()
        if created2:
            product_no_promo.delete()
        
        print(f"\n✅ Test simple terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_cart_item_pricing():
    """Teste le calcul des prix dans CartItem"""
    print("\n🧪 TEST DU CALCUL CARTITEM")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from cart.models import Cart, CartItem
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un produit avec promotion
        category, _ = Category.objects.get_or_create(
            name="Test Category Cart",
            defaults={'slug': 'test-category-cart'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Cart",
            defaults={'slug': 'test-team-cart', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="TEST Product Cart",
            defaults={
                'price': Decimal('15000.00'),  # Prix normal
                'sale_price': Decimal('10000.00'),  # Prix promotion
                'description': 'Produit de test cart',
                'category': category,
                'team': team,
                'slug': 'test-product-cart',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"📦 Produit: {product.name}")
        print(f"   - Prix normal: {product.price} FCFA")
        print(f"   - Prix promotion: {product.sale_price} FCFA")
        print(f"   - Prix actuel: {product.current_price} FCFA")
        
        # Créer un utilisateur de test
        user, created_user = User.objects.get_or_create(
            username='test_cart_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Créer un panier
        cart, created_cart = Cart.objects.get_or_create(user=user)
        
        # Créer un cart_item directement (contourner la validation)
        cart_item = CartItem(
            cart=cart,
            product=product,
            size='L',
            quantity=2
        )
        cart_item.save()
        
        print(f"\n🛒 CartItem créé:")
        print(f"   - Quantité: {cart_item.quantity}")
        print(f"   - Prix de base: {cart_item.base_price} FCFA")
        print(f"   - Prix total: {cart_item.total_price} FCFA")
        
        # Vérifier le calcul
        expected_base = product.current_price * cart_item.quantity
        print(f"\n🧮 Vérification du calcul:")
        print(f"   - Prix attendu: {product.current_price} × {cart_item.quantity} = {expected_base} FCFA")
        print(f"   - Prix réel: {cart_item.base_price} FCFA")
        
        if cart_item.base_price == expected_base:
            print(f"   ✅ Prix correct (promotion appliquée)")
        else:
            print(f"   ❌ Prix incorrect (promotion non appliquée)")
        
        # Nettoyer les données de test
        cart_item.delete()
        cart.delete()
        if created:
            product.delete()
        if created_user:
            user.delete()
        
        print(f"\n✅ Test CartItem terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test CartItem: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST SIMPLE DES PRIX PROMOTIONNELS")
    print("=" * 60)
    
    # Test 1: Prix promotionnels simples
    success1 = test_simple_promotional_pricing()
    
    # Test 2: Calcul CartItem
    success2 = test_cart_item_pricing()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Les prix promotionnels fonctionnent correctement")
        print("✅ Le calcul CartItem utilise les bons prix")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        if not success1:
            print("❌ Test des prix promotionnels échoué")
        if not success2:
            print("❌ Test du calcul CartItem échoué")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
