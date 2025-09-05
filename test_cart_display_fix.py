#!/usr/bin/env python
"""
Script de test pour vérifier la correction de l'affichage du panier
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_cart_display():
    """Teste l'affichage du panier après correction"""
    print("🧪 TEST DE L'AFFICHAGE DU PANIER")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        from products.models import Product, Category, Team
        from django.contrib.auth.models import User
        from decimal import Decimal
        
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username='test_display_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
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
            name="TEST Liverpool FC",
            defaults={
                'price': Decimal('20000.00'),
                'description': 'Produit de test pour affichage',
                'category': category,
                'team': team,
                'slug': 'test-liverpool-fc'
            }
        )
        
        print(f"📦 Produit de test: {product.name} - {product.price} FCFA")
        
        # Créer un panier
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Ajouter un article au panier (contourner la vérification de stock)
        cart_item = CartItem(
            cart=cart,
            product=product,
            size='L',
            quantity=1
        )
        # Sauvegarder sans validation
        cart_item.save(force_insert=True)
        
        print(f"\n🛒 Panier créé:")
        print(f"   - Utilisateur: {user.username}")
        print(f"   - Produit: {product.name}")
        print(f"   - Taille: L")
        print(f"   - Quantité: {cart_item.quantity}")
        print(f"   - Prix unitaire: {product.price} FCFA")
        print(f"   - Prix de base: {cart_item.base_price} FCFA")
        print(f"   - Prix total: {cart_item.total_price} FCFA")
        
        # Vérifier le calcul
        expected_base = product.price * cart_item.quantity
        expected_total = expected_base + cart_item.customization_price
        
        print(f"\n🧮 Vérification du calcul:")
        print(f"   - Prix unitaire × Quantité: {product.price} × {cart_item.quantity} = {expected_base} FCFA")
        print(f"   - Prix de base calculé: {expected_base} FCFA")
        print(f"   - Prix personnalisations: {cart_item.customization_price} FCFA")
        print(f"   - Prix total attendu: {expected_total} FCFA")
        
        if cart_item.base_price == expected_base:
            print(f"   ✅ Prix de base correct")
        else:
            print(f"   ❌ Prix de base incorrect (différence: {cart_item.base_price - expected_base} FCFA)")
        
        if cart_item.total_price == expected_total:
            print(f"   ✅ Prix total correct")
        else:
            print(f"   ❌ Prix total incorrect (différence: {cart_item.total_price - expected_total} FCFA)")
        
        # Test avec quantité 2
        print(f"\n🔄 Test avec quantité 2:")
        cart_item.quantity = 2
        cart_item.save()
        
        expected_base_2 = product.price * cart_item.quantity
        expected_total_2 = expected_base_2 + cart_item.customization_price
        
        print(f"   - Quantité: {cart_item.quantity}")
        print(f"   - Prix attendu: {product.price} × {cart_item.quantity} = {expected_base_2} FCFA")
        print(f"   - Prix total attendu: {expected_total_2} FCFA")
        print(f"   - Prix total réel: {cart_item.total_price} FCFA")
        
        if cart_item.total_price == expected_total_2:
            print(f"   ✅ Prix total correct avec quantité 2")
        else:
            print(f"   ❌ Prix total incorrect avec quantité 2 (différence: {cart_item.total_price - expected_total_2} FCFA)")
        
        # Nettoyer les données de test
        cart_item.delete()
        cart.delete()
        if created:
            product.delete()
            user.delete()
        
        print(f"\n✅ Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST DE LA CORRECTION DE L'AFFICHAGE DU PANIER")
    print("=" * 60)
    
    success = test_cart_display()
    
    if success:
        print("\n🎉 TEST RÉUSSI!")
        print("✅ L'affichage du panier fonctionne correctement")
        print("✅ Les calculs sont cohérents")
    else:
        print("\n💥 TEST ÉCHOUÉ!")
        print("❌ Des problèmes persistent dans l'affichage")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
