#!/usr/bin/env python
"""
Script de test pour le paiement à la livraison
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_cash_on_delivery():
    """Teste le système de paiement à la livraison"""
    print("🧪 TEST DU PAIEMENT À LA LIVRAISON")
    print("=" * 60)
    
    try:
        from orders.models import Order, OrderItem, Address
        from products.models import Product, Category, Team
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_cash_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Créer une adresse de test
        address, created = Address.objects.get_or_create(
            user=user,
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'phone': '+225123456789',
                'email': 'test@example.com',
                'address': '123 Test Street',
                'city': 'Abidjan',
                'postal_code': '12345',
                'country': 'Côte d\'Ivoire'
            }
        )
        
        # Créer un produit de test
        category, _ = Category.objects.get_or_create(
            name="Test Category",
            defaults={'slug': 'test-category'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team",
            defaults={'slug': 'test-team', 'country': 'Test'}
        )
        
        product, created = Product.objects.get_or_create(
            name="Test Product Cash",
            defaults={
                'price': Decimal('10000.00'),
                'description': 'Produit de test pour paiement à la livraison',
                'category': category,
                'team': team,
                'slug': 'test-product-cash'
            }
        )
        
        print(f"📦 Produit de test: {product.name} - {product.price} FCFA")
        
        # Créer une commande avec paiement à la livraison
        order = Order.objects.create(
            user=user,
            shipping_address=address,
            payment_method='cash_on_delivery',
            payment_status='cash_on_delivery',
            subtotal=Decimal('10000.00'),
            shipping_cost=Decimal('1000.00'),
            total=Decimal('11000.00'),
            notes='Test paiement à la livraison'
        )
        
        # Créer un article de commande
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            size='L',
            quantity=1,
            price=product.price,
            total_price=product.price
        )
        
        print(f"\n📋 Commande créée:")
        print(f"   - Numéro: {order.order_number}")
        print(f"   - Méthode de paiement: {order.get_payment_method_display()}")
        print(f"   - Statut de paiement: {order.get_payment_status_display()}")
        print(f"   - Total: {order.total} FCFA")
        
        # Vérifier que la commande est en attente de paiement
        if order.payment_status == 'cash_on_delivery':
            print(f"   ✅ Statut correct: Paiement à la livraison")
        else:
            print(f"   ❌ Statut incorrect: {order.payment_status}")
        
        # Simuler le paiement reçu (par l'admin)
        print(f"\n💰 Simulation du paiement reçu...")
        order.payment_status = 'paid'
        order.save()
        
        print(f"   - Nouveau statut: {order.get_payment_status_display()}")
        
        if order.payment_status == 'paid':
            print(f"   ✅ Paiement marqué comme reçu")
        else:
            print(f"   ❌ Erreur lors du marquage du paiement")
        
        # Nettoyer les données de test
        order_item.delete()
        order.delete()
        if created:
            product.delete()
            address.delete()
            user.delete()
        
        print(f"\n✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_payment_methods():
    """Teste les différentes méthodes de paiement"""
    print("\n🧪 TEST DES MÉTHODES DE PAIEMENT")
    print("=" * 60)
    
    try:
        from orders.models import Order
        
        # Vérifier les choix disponibles
        payment_methods = Order.PAYMENT_METHOD_CHOICES
        payment_statuses = Order.PAYMENT_STATUS_CHOICES
        
        print(f"📋 Méthodes de paiement disponibles:")
        for method, display in payment_methods:
            print(f"   - {method}: {display}")
        
        print(f"\n📋 Statuts de paiement disponibles:")
        for status, display in payment_statuses:
            print(f"   - {status}: {display}")
        
        # Vérifier que le paiement à la livraison est disponible
        if ('cash_on_delivery', 'Paiement à la livraison') in payment_methods:
            print(f"\n✅ Paiement à la livraison disponible")
        else:
            print(f"\n❌ Paiement à la livraison non disponible")
            return False
        
        if ('cash_on_delivery', 'Paiement à la livraison') in payment_statuses:
            print(f"✅ Statut 'cash_on_delivery' disponible")
        else:
            print(f"❌ Statut 'cash_on_delivery' non disponible")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST DU SYSTÈME DE PAIEMENT À LA LIVRAISON")
    print("=" * 60)
    
    tests = [
        ("Test des méthodes de paiement", test_payment_methods),
        ("Test du paiement à la livraison", test_cash_on_delivery),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"   {status} - {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ Le système de paiement à la livraison fonctionne")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ Des problèmes persistent")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
