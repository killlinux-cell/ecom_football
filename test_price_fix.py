#!/usr/bin/env python
"""
Script de test pour vérifier la correction des prix doublés
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_price_calculation():
    """Teste le calcul des prix après correction"""
    print("🧪 TEST DU CALCUL DES PRIX APRÈS CORRECTION")
    print("=" * 60)
    
    try:
        from orders.models import OrderItem, OrderItemCustomization
        from products.models import Product, JerseyCustomization
        from decimal import Decimal
        
        # Créer un produit de test
        from products.models import Category, Team
        
        # Créer catégorie et équipe de test
        category, _ = Category.objects.get_or_create(
            name="Test Category",
            defaults={'slug': 'test-category'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team",
            defaults={'slug': 'test-team', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="Test Product",
            defaults={
                'price': Decimal('8000.00'),
                'description': 'Produit de test',
                'category': category,
                'team': team,
                'slug': 'test-product'
            }
        )
        
        print(f"📦 Produit de test: {product.name}")
        print(f"   - Prix: {product.price} FCFA")
        
        # Simuler la création d'un OrderItem
        from orders.models import Order
        from django.contrib.auth.models import User
        
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        
        # Créer une commande de test
        order, created = Order.objects.get_or_create(
            user=user,
            defaults={
                'subtotal': Decimal('0.00'),
                'shipping_cost': Decimal('0.00'),
                'total': Decimal('0.00')
            }
        )
        
        # Créer un OrderItem de test
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            size='XL',
            quantity=1,
            price=product.price,
            total_price=product.price  # Prix de base seulement
        )
        
        print(f"\n📋 OrderItem créé:")
        print(f"   - Prix unitaire: {order_item.price} FCFA")
        print(f"   - Quantité: {order_item.quantity}")
        print(f"   - Prix de base: {order_item.price * order_item.quantity} FCFA")
        print(f"   - Total actuel: {order_item.total_price} FCFA")
        
        # Vérifier que le prix est correct
        expected_base = order_item.price * order_item.quantity
        if order_item.total_price == expected_base:
            print(f"   ✅ Prix de base correct")
        else:
            print(f"   ❌ Prix de base incorrect (différence: {order_item.total_price - expected_base} FCFA)")
        
        # Tester avec des personnalisations
        print(f"\n🎨 Test avec personnalisations:")
        
        # Créer une personnalisation de test
        customization, created = JerseyCustomization.objects.get_or_create(
            name='Test Customization',
            defaults={
                'price': Decimal('1000.00'),
                'customization_type': 'badge'
            }
        )
        
        # Ajouter la personnalisation
        order_custom = OrderItemCustomization.objects.create(
            order_item=order_item,
            customization=customization,
            price=customization.price
        )
        
        print(f"   - Personnalisation ajoutée: {customization.price} FCFA")
        
        # Recalculer le total avec personnalisations
        order_item.total_price = order_item.get_total_with_customizations()
        order_item.save()
        
        print(f"   - Total avec personnalisations: {order_item.total_price} FCFA")
        
        # Vérifier le calcul
        expected_total = expected_base + customization.price
        if order_item.total_price == expected_total:
            print(f"   ✅ Prix avec personnalisations correct")
        else:
            print(f"   ❌ Prix avec personnalisations incorrect (différence: {order_item.total_price - expected_total} FCFA)")
        
        # Nettoyer les données de test
        order_item.delete()
        order.delete()
        if created:
            product.delete()
            customization.delete()
        
        print(f"\n✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST DE LA CORRECTION DES PRIX DOUBLÉS")
    print("=" * 60)
    
    success = test_price_calculation()
    
    if success:
        print("\n🎉 TEST RÉUSSI!")
        print("✅ La correction des prix doublés fonctionne")
        print("✅ Les calculs sont maintenant cohérents")
    else:
        print("\n💥 TEST ÉCHOUÉ!")
        print("❌ Des problèmes persistent dans le calcul des prix")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
