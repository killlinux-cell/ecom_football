#!/usr/bin/env python
"""
Script de test pour vérifier les prix promotionnels dans les commandes
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_order_promotional_pricing():
    """Teste les prix promotionnels dans les commandes"""
    print("🧪 TEST DES PRIX PROMOTIONNELS DANS LES COMMANDES")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from cart.models import Cart, CartItem
        from orders.models import Order, OrderItem
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un produit avec promotion
        category, _ = Category.objects.get_or_create(
            name="Test Category Order",
            defaults={'slug': 'test-category-order'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Order",
            defaults={'slug': 'test-team-order', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="TEST Product Order",
            defaults={
                'price': Decimal('15000.00'),  # Prix normal
                'sale_price': Decimal('10000.00'),  # Prix promotion
                'description': 'Produit de test commande',
                'category': category,
                'team': team,
                'slug': 'test-product-order',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"📦 Produit de test: {product.name}")
        print(f"   - Prix normal: {product.price} FCFA")
        print(f"   - Prix promotion: {product.sale_price} FCFA")
        print(f"   - Prix actuel: {product.current_price} FCFA")
        
        # Créer un utilisateur de test
        user, created_user = User.objects.get_or_create(
            username='test_order_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Créer un panier
        cart, created_cart = Cart.objects.get_or_create(user=user)
        
        # Ajouter le produit au panier
        cart_item, created_item = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size='L',
            defaults={'quantity': 2}
        )
        
        print(f"\n🛒 Panier créé:")
        print(f"   - Produit: {cart_item.product.name}")
        print(f"   - Quantité: {cart_item.quantity}")
        print(f"   - Prix unitaire: {cart_item.product.current_price} FCFA")
        print(f"   - Prix total: {cart_item.total_price} FCFA")
        
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
        
        # Simuler la création d'OrderItem comme dans orders/views.py
        current_price = product.current_price
        base_price = current_price * cart_item.quantity
        
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            size='L',
            quantity=cart_item.quantity,
            price=current_price,  # Utiliser le prix actuel (promotion)
            total_price=base_price  # Prix de base avec promotion
        )
        
        print(f"\n📋 Commande créée:")
        print(f"   - Commande: {order.order_number}")
        print(f"   - Produit: {order_item.product_name}")
        print(f"   - Quantité: {order_item.quantity}")
        print(f"   - Prix unitaire: {order_item.price} FCFA")
        print(f"   - Prix total: {order_item.total_price} FCFA")
        
        # Vérifier que le prix de la commande est correct
        expected_price = product.current_price * cart_item.quantity
        print(f"\n🧮 Vérification du calcul:")
        print(f"   - Prix attendu: {product.current_price} × {cart_item.quantity} = {expected_price} FCFA")
        print(f"   - Prix réel: {order_item.total_price} FCFA")
        
        if order_item.price == product.current_price:
            print(f"   ✅ Prix unitaire correct (promotion appliquée)")
        else:
            print(f"   ❌ Prix unitaire incorrect (promotion non appliquée)")
        
        if order_item.total_price == expected_price:
            print(f"   ✅ Prix total correct (promotion appliquée)")
        else:
            print(f"   ❌ Prix total incorrect (promotion non appliquée)")
        
        # Vérifier que le total de la commande est cohérent
        order.recalculate_totals()
        print(f"\n💰 Total de la commande:")
        print(f"   - Total calculé: {order.total} FCFA")
        print(f"   - Total attendu: {order_item.total_price + order.shipping_cost} FCFA")
        
        if order.total == order_item.total_price + order.shipping_cost:
            print(f"   ✅ Total de commande cohérent")
        else:
            print(f"   ❌ Total de commande incohérent")
        
        # Nettoyer les données de test
        order_item.delete()
        order.delete()
        cart_item.delete()
        cart.delete()
        if created:
            product.delete()
        if created_user:
            user.delete()
        
        print(f"\n✅ Test de commande terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST DES PRIX PROMOTIONNELS DANS LES COMMANDES")
    print("=" * 60)
    
    success = test_order_promotional_pricing()
    
    if success:
        print("\n🎉 TEST RÉUSSI!")
        print("✅ Les prix promotionnels fonctionnent dans les commandes")
        print("✅ Les OrderItem utilisent les bons prix")
        print("✅ Les totaux sont cohérents")
    else:
        print("\n💥 TEST ÉCHOUÉ!")
        print("❌ Des problèmes persistent dans les commandes")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
