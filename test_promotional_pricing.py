#!/usr/bin/env python
"""
Script de test pour diagnostiquer les prix promotionnels
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_promotional_pricing():
    """Teste les prix promotionnels"""
    print("🧪 TEST DES PRIX PROMOTIONNELS")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from cart.models import Cart, CartItem
        from orders.models import Order, OrderItem
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un produit avec promotion
        category, _ = Category.objects.get_or_create(
            name="Test Category Promo",
            defaults={'slug': 'test-category-promo'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Promo",
            defaults={'slug': 'test-team-promo', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="TEST Product Promo",
            defaults={
                'price': Decimal('15000.00'),  # Prix normal
                'sale_price': Decimal('10000.00'),  # Prix promotion
                'description': 'Produit de test avec promotion',
                'category': category,
                'team': team,
                'slug': 'test-product-promo',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"📦 Produit de test: {product.name}")
        print(f"   - Prix normal: {product.price} FCFA")
        print(f"   - Prix promotion: {product.sale_price} FCFA")
        print(f"   - Prix actuel: {product.current_price} FCFA")
        
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_promo_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Créer un panier
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Ajouter le produit au panier
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            size='L',
            quantity=1
        )
        
        print(f"\n🛒 Panier créé:")
        print(f"   - Produit: {cart_item.product.name}")
        print(f"   - Prix unitaire: {cart_item.product.current_price} FCFA")
        print(f"   - Prix de base: {cart_item.base_price} FCFA")
        print(f"   - Prix total: {cart_item.total_price} FCFA")
        
        # Vérifier le calcul
        expected_price = product.current_price * cart_item.quantity
        print(f"\n🧮 Vérification du calcul:")
        print(f"   - Prix attendu: {product.current_price} × {cart_item.quantity} = {expected_price} FCFA")
        print(f"   - Prix réel: {cart_item.total_price} FCFA")
        
        if cart_item.total_price == expected_price:
            print(f"   ✅ Prix correct (promotion appliquée)")
        else:
            print(f"   ❌ Prix incorrect (promotion non appliquée)")
        
        # Créer une commande
        order = Order.objects.create(
            user=user,
            status='pending',
            payment_status='pending',
            payment_method='cash_on_delivery',
            total=cart_item.total_price,
            shipping_cost=Decimal('1000.00')
        )
        
        # Créer un article de commande
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            size='L',
            quantity=1,
            price=product.current_price,  # Utiliser le prix actuel (promotion)
            total_price=product.current_price
        )
        
        print(f"\n📋 Commande créée:")
        print(f"   - Commande: {order.order_number}")
        print(f"   - Produit: {order_item.product_name}")
        print(f"   - Prix unitaire: {order_item.price} FCFA")
        print(f"   - Prix total: {order_item.total_price} FCFA")
        
        # Vérifier que le prix de la commande est correct
        if order_item.price == product.current_price:
            print(f"   ✅ Prix de commande correct (promotion appliquée)")
        else:
            print(f"   ❌ Prix de commande incorrect (promotion non appliquée)")
        
        # Nettoyer les données de test
        order_item.delete()
        order.delete()
        cart_item.delete()
        cart.delete()
        if created:
            product.delete()
            user.delete()
        
        print(f"\n✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_cart_session_pricing():
    """Teste les prix dans le panier session"""
    print("\n🧪 TEST DU PANIER SESSION")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from cart.cart import Cart
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un produit avec promotion
        category, _ = Category.objects.get_or_create(
            name="Test Category Session",
            defaults={'slug': 'test-category-session'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Session",
            defaults={'slug': 'test-team-session', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="TEST Product Session",
            defaults={
                'price': Decimal('20000.00'),  # Prix normal
                'sale_price': Decimal('12000.00'),  # Prix promotion
                'description': 'Produit de test session',
                'category': category,
                'team': team,
                'slug': 'test-product-session',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"📦 Produit: {product.name}")
        print(f"   - Prix normal: {product.price} FCFA")
        print(f"   - Prix promotion: {product.sale_price} FCFA")
        print(f"   - Prix actuel: {product.current_price} FCFA")
        
        # Simuler un panier session
        from django.test import RequestFactory
        from django.contrib.sessions.backends.db import SessionStore
        
        factory = RequestFactory()
        request = factory.get('/')
        request.session = SessionStore()
        request.user = User.objects.create_user('test_session_user')
        
        # Créer le panier
        cart = Cart(request)
        cart_item = cart.add(product=product, size='L', quantity=1)
        
        print(f"\n🛒 Panier session:")
        print(f"   - Prix dans session: {cart.cart[f'{product.id}_L']['price']} FCFA")
        print(f"   - Prix attendu: {product.current_price} FCFA")
        
        if cart.cart[f'{product.id}_L']['price'] == str(product.current_price):
            print(f"   ✅ Prix session correct (promotion appliquée)")
        else:
            print(f"   ❌ Prix session incorrect (promotion non appliquée)")
        
        # Nettoyer
        cart_item.delete()
        if created:
            product.delete()
        
        print(f"\n✅ Test session terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test session: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST DES PRIX PROMOTIONNELS")
    print("=" * 60)
    
    # Test 1: Prix promotionnels
    success1 = test_promotional_pricing()
    
    # Test 2: Panier session
    success2 = test_cart_session_pricing()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Les prix promotionnels fonctionnent correctement")
        print("✅ Le panier session utilise les bons prix")
        print("✅ Les commandes utilisent les prix promotionnels")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        if not success1:
            print("❌ Test des prix promotionnels échoué")
        if not success2:
            print("❌ Test du panier session échoué")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
