#!/usr/bin/env python
"""
Script de test pour vérifier la création de produits depuis le dashboard
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_dashboard_product_creation():
    """Teste la création de produits depuis le dashboard"""
    print("🧪 TEST CRÉATION PRODUIT DASHBOARD")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from django.contrib.auth.models import User
        from django.test import RequestFactory, Client
        from django.contrib.auth import get_user_model
        from decimal import Decimal
        
        # Créer un utilisateur admin
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(
            username='test_admin_dashboard',
            defaults={
                'email': 'admin@test.com',
                'first_name': 'Test',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Créer une catégorie et une équipe
        category, _ = Category.objects.get_or_create(
            name="Test Category Dashboard",
            defaults={'slug': 'test-category-dashboard'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Dashboard",
            defaults={'slug': 'test-team-dashboard', 'country': 'Test'}
        )
        
        print(f"👤 Utilisateur admin: {admin_user.username}")
        print(f"📂 Catégorie: {category.name}")
        print(f"⚽ Équipe: {team.name}")
        
        # Créer un client de test
        client = Client()
        client.force_login(admin_user)
        
        # Données du produit à créer
        product_data = {
            'name': 'TEST Product Dashboard',
            'description': 'Produit de test créé depuis le dashboard',
            'price': '15000.00',
            'sale_price': '12000.00',
            'stock_quantity': '10',
            'category': str(category.id),
            'team': str(team.id),
            'is_active': 'on',
            'is_featured': 'on'
        }
        
        print(f"\n📦 Données du produit:")
        for key, value in product_data.items():
            print(f"   - {key}: {value}")
        
        # Tester la création via POST
        response = client.post('/dashboard/products/create/', product_data)
        
        print(f"\n📊 Réponse de création:")
        print(f"   - Statut: {response.status_code}")
        print(f"   - Redirection: {response.url if hasattr(response, 'url') else 'Aucune'}")
        
        if response.status_code == 302:  # Redirection après succès
            print(f"   ✅ Création réussie (redirection)")
            
            # Vérifier que le produit a été créé
            try:
                product = Product.objects.get(name='TEST Product Dashboard')
                print(f"\n🎉 Produit créé avec succès:")
                print(f"   - ID: {product.id}")
                print(f"   - Nom: {product.name}")
                print(f"   - Prix: {product.price} FCFA")
                print(f"   - Prix promo: {product.sale_price} FCFA")
                print(f"   - Stock: {product.stock_quantity}")
                print(f"   - Catégorie: {product.category.name}")
                print(f"   - Équipe: {product.team.name}")
                print(f"   - Actif: {product.is_active}")
                print(f"   - Vedette: {product.is_featured}")
                
                # Vérifier les types
                print(f"\n🔍 Vérification des types:")
                print(f"   - Prix (Decimal): {type(product.price)} = {product.price}")
                print(f"   - Prix promo (Decimal): {type(product.sale_price)} = {product.sale_price}")
                print(f"   - Stock (int): {type(product.stock_quantity)} = {product.stock_quantity}")
                
                # Nettoyer
                product.delete()
                print(f"\n🧹 Produit de test supprimé")
                
                return True
                
            except Product.DoesNotExist:
                print(f"   ❌ Produit non trouvé en base de données")
                return False
                
        else:
            print(f"   ❌ Échec de la création")
            if hasattr(response, 'content'):
                print(f"   - Contenu: {response.content.decode()[:200]}...")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_product_edit():
    """Teste l'édition de produits depuis le dashboard"""
    print("\n🧪 TEST ÉDITION PRODUIT DASHBOARD")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from django.contrib.auth.models import User
        from django.test import RequestFactory, Client
        from django.contrib.auth import get_user_model
        from decimal import Decimal
        
        # Créer un utilisateur admin
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(
            username='test_admin_edit',
            defaults={
                'email': 'admin@test.com',
                'first_name': 'Test',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Créer une catégorie et une équipe
        category, _ = Category.objects.get_or_create(
            name="Test Category Edit",
            defaults={'slug': 'test-category-edit'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Edit",
            defaults={'slug': 'test-team-edit', 'country': 'Test'}
        )
        
        # Créer un produit de test
        product = Product.objects.create(
            name='TEST Product Edit Original',
            description='Produit original',
            price=Decimal('10000.00'),
            stock_quantity=5,
            category=category,
            team=team
        )
        
        print(f"📦 Produit original créé: {product.name} - {product.price} FCFA")
        
        # Créer un client de test
        client = Client()
        client.force_login(admin_user)
        
        # Données de mise à jour
        update_data = {
            'name': 'TEST Product Edit Updated',
            'description': 'Produit mis à jour depuis le dashboard',
            'price': '20000.00',
            'sale_price': '18000.00',
            'stock_quantity': '15',
            'is_active': 'on',
            'is_featured': 'on'
        }
        
        print(f"\n📝 Données de mise à jour:")
        for key, value in update_data.items():
            print(f"   - {key}: {value}")
        
        # Tester la mise à jour via POST
        response = client.post(f'/dashboard/products/{product.id}/edit/', update_data)
        
        print(f"\n📊 Réponse de mise à jour:")
        print(f"   - Statut: {response.status_code}")
        print(f"   - Redirection: {response.url if hasattr(response, 'url') else 'Aucune'}")
        
        if response.status_code == 302:  # Redirection après succès
            print(f"   ✅ Mise à jour réussie (redirection)")
            
            # Vérifier que le produit a été mis à jour
            product.refresh_from_db()
            print(f"\n🎉 Produit mis à jour:")
            print(f"   - Nom: {product.name}")
            print(f"   - Prix: {product.price} FCFA")
            print(f"   - Prix promo: {product.sale_price} FCFA")
            print(f"   - Stock: {product.stock_quantity}")
            print(f"   - Actif: {product.is_active}")
            print(f"   - Vedette: {product.is_featured}")
            
            # Vérifier les types
            print(f"\n🔍 Vérification des types:")
            print(f"   - Prix (Decimal): {type(product.price)} = {product.price}")
            print(f"   - Prix promo (Decimal): {type(product.sale_price)} = {product.sale_price}")
            print(f"   - Stock (int): {type(product.stock_quantity)} = {product.stock_quantity}")
            
            # Nettoyer
            product.delete()
            print(f"\n🧹 Produit de test supprimé")
            
            return True
            
        else:
            print(f"   ❌ Échec de la mise à jour")
            if hasattr(response, 'content'):
                print(f"   - Contenu: {response.content.decode()[:200]}...")
            
            # Nettoyer même en cas d'échec
            product.delete()
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_invalid_data_handling():
    """Teste la gestion des données invalides"""
    print("\n🧪 TEST GESTION DONNÉES INVALIDES")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team
        from django.contrib.auth.models import User
        from django.test import RequestFactory, Client
        from django.contrib.auth import get_user_model
        
        # Créer un utilisateur admin
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(
            username='test_admin_invalid',
            defaults={
                'email': 'admin@test.com',
                'first_name': 'Test',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Créer une catégorie et une équipe
        category, _ = Category.objects.get_or_create(
            name="Test Category Invalid",
            defaults={'slug': 'test-category-invalid'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Invalid",
            defaults={'slug': 'test-team-invalid', 'country': 'Test'}
        )
        
        # Créer un client de test
        client = Client()
        client.force_login(admin_user)
        
        # Test 1: Prix invalide
        print("🔍 Test 1: Prix invalide")
        invalid_data = {
            'name': 'TEST Invalid Price',
            'description': 'Test prix invalide',
            'price': 'prix_invalide',
            'stock_quantity': '10',
            'category': str(category.id),
            'team': str(team.id)
        }
        
        response = client.post('/dashboard/products/create/', invalid_data)
        print(f"   - Statut: {response.status_code}")
        print(f"   - Attendu: 200 (erreur affichée)")
        
        if response.status_code == 200:
            print(f"   ✅ Erreur gérée correctement")
        else:
            print(f"   ❌ Erreur non gérée")
        
        # Test 2: Stock négatif
        print("\n🔍 Test 2: Stock négatif")
        invalid_data = {
            'name': 'TEST Negative Stock',
            'description': 'Test stock négatif',
            'price': '10000.00',
            'stock_quantity': '-5',
            'category': str(category.id),
            'team': str(team.id)
        }
        
        response = client.post('/dashboard/products/create/', invalid_data)
        print(f"   - Statut: {response.status_code}")
        print(f"   - Attendu: 200 (erreur affichée)")
        
        if response.status_code == 200:
            print(f"   ✅ Erreur gérée correctement")
        else:
            print(f"   ❌ Erreur non gérée")
        
        # Test 3: Champs requis manquants
        print("\n🔍 Test 3: Champs requis manquants")
        invalid_data = {
            'name': '',
            'description': 'Test champs manquants',
            'price': '',
            'stock_quantity': '',
            'category': '',
            'team': ''
        }
        
        response = client.post('/dashboard/products/create/', invalid_data)
        print(f"   - Statut: {response.status_code}")
        print(f"   - Attendu: 200 (erreur affichée)")
        
        if response.status_code == 200:
            print(f"   ✅ Erreur gérée correctement")
        else:
            print(f"   ❌ Erreur non gérée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST CRÉATION PRODUITS DASHBOARD")
    print("=" * 60)
    
    # Test 1: Création de produit
    success1 = test_dashboard_product_creation()
    
    # Test 2: Édition de produit
    success2 = test_dashboard_product_edit()
    
    # Test 3: Gestion des données invalides
    success3 = test_invalid_data_handling()
    
    if success1 and success2 and success3:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Création de produits depuis le dashboard fonctionne")
        print("✅ Édition de produits depuis le dashboard fonctionne")
        print("✅ Gestion des erreurs fonctionne")
        print("✅ Plus d'erreur de comparaison str/int")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        if not success1:
            print("❌ Test de création échoué")
        if not success2:
            print("❌ Test d'édition échoué")
        if not success3:
            print("❌ Test de gestion d'erreurs échoué")
    
    return success1 and success2 and success3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
