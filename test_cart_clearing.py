#!/usr/bin/env python
"""
Script de test pour vérifier le vidage des paniers
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_cart_clearing():
    """Teste le vidage des paniers"""
    print("🧪 TEST DU VIDAGE DES PANIERS")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from cart.models import Cart, CartItem
        from cart.cart import Cart as CartSession
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un produit de test
        category, _ = Category.objects.get_or_create(
            name="Test Category Clear",
            defaults={'slug': 'test-category-clear'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Clear",
            defaults={'slug': 'test-team-clear', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="TEST Product Clear",
            defaults={
                'price': Decimal('10000.00'),
                'description': 'Produit de test pour vidage',
                'category': category,
                'team': team,
                'slug': 'test-product-clear',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"📦 Produit de test: {product.name} - {product.price} FCFA")
        
        # Créer un utilisateur de test
        user, created_user = User.objects.get_or_create(
            username='test_clear_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Créer un panier en base de données
        cart, created_cart = Cart.objects.get_or_create(user=user)
        
        # Ajouter un article au panier
        cart_item, created_item = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size='L',
            defaults={'quantity': 2}
        )
        
        print(f"\n🛒 Panier créé:")
        print(f"   - Utilisateur: {user.username}")
        print(f"   - Articles: {cart.items.count()}")
        print(f"   - Total: {cart.total_price} FCFA")
        
        # Vérifier que le panier a des articles
        if cart.items.count() > 0:
            print(f"   ✅ Panier a des articles avant vidage")
        else:
            print(f"   ❌ Panier vide avant vidage")
            return False
        
        # Simuler le vidage du panier (comme dans orders/views.py)
        from django.test import RequestFactory
        from django.contrib.sessions.backends.db import SessionStore
        
        factory = RequestFactory()
        request = factory.get('/')
        request.session = SessionStore()
        request.user = user
        
        # Créer le panier session
        cart_session = CartSession(request)
        
        # Vider le panier
        cart_session.clear()
        
        # Vérifier que le panier est vide
        cart.refresh_from_db()
        
        print(f"\n🧹 Après vidage:")
        print(f"   - Articles: {cart.items.count()}")
        print(f"   - Total: {cart.total_price} FCFA")
        
        if cart.items.count() == 0:
            print(f"   ✅ Panier vidé avec succès")
        else:
            print(f"   ❌ Panier non vidé")
            return False
        
        # Nettoyer les données de test
        if created:
            product.delete()
        if created_user:
            user.delete()
        
        print(f"\n✅ Test de vidage terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_cart_clearing_after_order():
    """Teste le vidage du panier après une commande"""
    print("\n🧪 TEST DU VIDAGE APRÈS COMMANDE")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from cart.models import Cart, CartItem
        from orders.models import Order, OrderItem
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un produit de test
        category, _ = Category.objects.get_or_create(
            name="Test Category Order Clear",
            defaults={'slug': 'test-category-order-clear'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Order Clear",
            defaults={'slug': 'test-team-order-clear', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="TEST Product Order Clear",
            defaults={
                'price': Decimal('15000.00'),
                'description': 'Produit de test pour commande',
                'category': category,
                'team': team,
                'slug': 'test-product-order-clear',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"📦 Produit de test: {product.name} - {product.price} FCFA")
        
        # Créer un utilisateur de test
        user, created_user = User.objects.get_or_create(
            username='test_order_clear_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Créer un panier
        cart, created_cart = Cart.objects.get_or_create(user=user)
        
        # Ajouter un article au panier
        cart_item, created_item = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size='L',
            defaults={'quantity': 1}
        )
        
        print(f"\n🛒 Panier avant commande:")
        print(f"   - Articles: {cart.items.count()}")
        print(f"   - Total: {cart.total_price} FCFA")
        
        # Créer une commande
        order = Order.objects.create(
            user=user,
            status='pending',
            payment_status='pending',
            payment_method='cash_on_delivery',
            subtotal=cart_item.total_price,
            shipping_cost=Decimal('1000.00'),
            total=cart_item.total_price + Decimal('1000.00')
        )
        
        # Créer un article de commande
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            size='L',
            quantity=cart_item.quantity,
            price=product.current_price,
            total_price=product.current_price * cart_item.quantity
        )
        
        print(f"\n📋 Commande créée:")
        print(f"   - Commande: {order.order_number}")
        print(f"   - Total: {order.total} FCFA")
        
        # Simuler le vidage du panier après commande
        from django.test import RequestFactory
        from django.contrib.sessions.backends.db import SessionStore
        from cart.cart import Cart as CartSession
        
        factory = RequestFactory()
        request = factory.get('/')
        request.session = SessionStore()
        request.user = user
        
        cart_session = CartSession(request)
        cart_session.clear()
        
        # Vérifier que le panier est vide
        cart.refresh_from_db()
        
        print(f"\n🧹 Après vidage du panier:")
        print(f"   - Articles: {cart.items.count()}")
        print(f"   - Total: {cart.total_price} FCFA")
        
        if cart.items.count() == 0:
            print(f"   ✅ Panier vidé après commande")
        else:
            print(f"   ❌ Panier non vidé après commande")
            return False
        
        # Nettoyer les données de test
        order_item.delete()
        order.delete()
        if created:
            product.delete()
        if created_user:
            user.delete()
        
        print(f"\n✅ Test de vidage après commande terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST DU VIDAGE DES PANIERS")
    print("=" * 60)
    
    # Test 1: Vidage simple
    success1 = test_cart_clearing()
    
    # Test 2: Vidage après commande
    success2 = test_cart_clearing_after_order()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Le vidage des paniers fonctionne correctement")
        print("✅ Les paniers se vident après les commandes")
        print("✅ Plus de problème de calculs incohérents")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        if not success1:
            print("❌ Test de vidage simple échoué")
        if not success2:
            print("❌ Test de vidage après commande échoué")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
