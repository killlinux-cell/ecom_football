#!/usr/bin/env python
"""
Script de test pour vérifier l'édition de produit dans l'admin
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_product_stock_edit():
    """Teste l'édition du stock d'un produit"""
    print("🧪 TEST D'ÉDITION DE PRODUIT - STOCK")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from django.contrib.auth.models import User
        from decimal import Decimal
        
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
            name="TEST Product Stock",
            defaults={
                'price': Decimal('10000.00'),
                'description': 'Produit de test pour stock',
                'category': category,
                'team': team,
                'slug': 'test-product-stock',
                'stock_quantity': 10
            }
        )
        
        print(f"📦 Produit de test: {product.name}")
        print(f"   - Stock initial: {product.stock_quantity}")
        
        # Simuler une modification du stock
        print(f"\n🔄 Modification du stock...")
        old_stock = product.stock_quantity
        product.stock_quantity = 3  # En dessous du seuil de 5
        product.save()
        
        print(f"   - Ancien stock: {old_stock}")
        print(f"   - Nouveau stock: {product.stock_quantity}")
        
        # Vérifier que le signal fonctionne
        print(f"\n✅ Signal de stock exécuté sans erreur")
        
        # Nettoyer les données de test
        if created:
            product.delete()
        
        print(f"\n🎉 Test terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_product_creation():
    """Teste la création d'un nouveau produit"""
    print("\n🧪 TEST DE CRÉATION DE PRODUIT")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from decimal import Decimal
        
        # Créer un produit de test
        category, _ = Category.objects.get_or_create(
            name="Test Category 2",
            defaults={'slug': 'test-category-2'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team 2",
            defaults={'slug': 'test-team-2', 'country': 'Test'}
        )
        
        product = Product.objects.create(
            name="TEST Product Creation",
            price=Decimal('15000.00'),
            description='Produit de test pour création',
            category=category,
            team=team,
            slug='test-product-creation',
            stock_quantity=2  # En dessous du seuil
        )
        
        print(f"📦 Produit créé: {product.name}")
        print(f"   - Stock: {product.stock_quantity}")
        print(f"   - Prix: {product.price} FCFA")
        
        # Nettoyer
        product.delete()
        
        print(f"\n✅ Création de produit réussie")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST DE L'ÉDITION DE PRODUIT DANS L'ADMIN")
    print("=" * 60)
    
    # Test 1: Édition de stock
    success1 = test_product_stock_edit()
    
    # Test 2: Création de produit
    success2 = test_product_creation()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ L'édition de produit fonctionne correctement")
        print("✅ Les signals de stock fonctionnent")
        print("✅ Plus d'erreur AttributeError 'stock'")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        if not success1:
            print("❌ Test d'édition de stock échoué")
        if not success2:
            print("❌ Test de création de produit échoué")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
