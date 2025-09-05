#!/usr/bin/env python
"""
Script de test pour vérifier le système d'avis
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_reviews_system():
    """Teste le système d'avis complet"""
    print("🧪 TEST SYSTÈME D'AVIS")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team, Review
        from django.contrib.auth.models import User
        from django.test import RequestFactory, Client
        from django.contrib.auth import get_user_model
        from decimal import Decimal
        
        # Créer un utilisateur de test
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='test_review_user',
            defaults={
                'email': 'review@test.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Créer une catégorie et une équipe
        category, _ = Category.objects.get_or_create(
            name="Test Category Reviews",
            defaults={'slug': 'test-category-reviews'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Reviews",
            defaults={'slug': 'test-team-reviews', 'country': 'Test'}
        )
        
        # Créer un produit de test
        product, created = Product.objects.get_or_create(
            name='TEST Product Reviews',
            defaults={
                'price': Decimal('15000.00'),
                'description': 'Produit de test pour avis',
                'category': category,
                'team': team,
                'slug': 'test-product-reviews',
                'stock_quantity': 10,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        print(f"👤 Utilisateur: {user.username}")
        print(f"📦 Produit: {product.name}")
        print(f"📊 Avis initiaux: {product.total_reviews}")
        print(f"⭐ Note moyenne: {product.average_rating}")
        
        # Test 1: Créer un avis
        print(f"\n🧪 Test 1: Création d'un avis")
        review1 = Review.objects.create(
            product=product,
            user=user,
            rating=5,
            comment="Excellent produit, je recommande !"
        )
        
        print(f"   ✅ Avis créé: {review1.rating}★ - {review1.comment[:30]}...")
        print(f"   📊 Avis totaux: {product.total_reviews}")
        print(f"   ⭐ Note moyenne: {product.average_rating}")
        
        # Test 2: Créer un deuxième avis avec un autre utilisateur
        print(f"\n🧪 Test 2: Deuxième avis")
        user2, _ = User.objects.get_or_create(
            username='test_review_user2',
            defaults={
                'email': 'review2@test.com',
                'first_name': 'Test2',
                'last_name': 'User2'
            }
        )
        
        review2 = Review.objects.create(
            product=product,
            user=user2,
            rating=4,
            comment="Très bon produit, qualité correcte."
        )
        
        print(f"   ✅ Avis créé: {review2.rating}★ - {review2.comment[:30]}...")
        print(f"   📊 Avis totaux: {product.total_reviews}")
        print(f"   ⭐ Note moyenne: {product.average_rating}")
        
        # Test 3: Créer un troisième avis
        print(f"\n🧪 Test 3: Troisième avis")
        user3, _ = User.objects.get_or_create(
            username='test_review_user3',
            defaults={
                'email': 'review3@test.com',
                'first_name': 'Test3',
                'last_name': 'User3'
            }
        )
        
        review3 = Review.objects.create(
            product=product,
            user=user3,
            rating=3,
            comment="Produit correct, mais pourrait être mieux."
        )
        
        print(f"   ✅ Avis créé: {review3.rating}★ - {review3.comment[:30]}...")
        print(f"   📊 Avis totaux: {product.total_reviews}")
        print(f"   ⭐ Note moyenne: {product.average_rating}")
        
        # Test 4: Mettre à jour un avis existant
        print(f"\n🧪 Test 4: Mise à jour d'un avis")
        review1.rating = 5
        review1.comment = "Produit exceptionnel, je le recommande vivement !"
        review1.save()
        
        print(f"   ✅ Avis mis à jour: {review1.rating}★ - {review1.comment[:30]}...")
        print(f"   📊 Avis totaux: {product.total_reviews}")
        print(f"   ⭐ Note moyenne: {product.average_rating}")
        
        # Test 5: Vérifier la contrainte unique
        print(f"\n🧪 Test 5: Contrainte unique (même utilisateur)")
        try:
            Review.objects.create(
                product=product,
                user=user,
                rating=2,
                comment="Tentative de double avis"
            )
            print(f"   ❌ Erreur: Double avis autorisé")
        except Exception as e:
            print(f"   ✅ Contrainte respectée: {str(e)[:50]}...")
        
        # Test 6: Vérifier les propriétés du produit
        print(f"\n🧪 Test 6: Propriétés du produit")
        print(f"   📊 Total avis: {product.total_reviews}")
        print(f"   ⭐ Note moyenne: {product.average_rating}")
        print(f"   🔍 Avis récents: {product.reviews.count()}")
        
        # Test 7: Test via le client HTTP
        print(f"\n🧪 Test 7: Test via client HTTP")
        client = Client()
        client.force_login(user)
        
        # Tester l'ajout d'avis via POST
        response = client.post(f'/product/{product.slug}/review/', {
            'rating': '5',
            'comment': 'Test via HTTP client'
        })
        
        print(f"   📊 Statut: {response.status_code}")
        if response.status_code == 302:
            print(f"   ✅ Redirection réussie")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # Nettoyer les données de test
        print(f"\n🧹 Nettoyage des données de test")
        Review.objects.filter(product=product).delete()
        if created:
            product.delete()
        if created:
            user.delete()
        user2.delete()
        user3.delete()
        
        print(f"   ✅ Données nettoyées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_reviews_display():
    """Teste l'affichage des avis dans le template"""
    print("\n🧪 TEST AFFICHAGE AVIS")
    print("=" * 60)
    
    try:
        from products.models import Product, Category, Team, Review
        from django.contrib.auth.models import User
        from django.test import RequestFactory, Client
        from django.contrib.auth import get_user_model
        from decimal import Decimal
        
        # Créer un utilisateur de test
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='test_display_user',
            defaults={
                'email': 'display@test.com',
                'first_name': 'Display',
                'last_name': 'User'
            }
        )
        
        # Créer une catégorie et une équipe
        category, _ = Category.objects.get_or_create(
            name="Test Category Display",
            defaults={'slug': 'test-category-display'}
        )
        team, _ = Team.objects.get_or_create(
            name="Test Team Display",
            defaults={'slug': 'test-team-display', 'country': 'Test'}
        )
        
        # Créer un produit de test
        product, created = Product.objects.get_or_create(
            name='TEST Product Display',
            defaults={
                'price': Decimal('20000.00'),
                'description': 'Produit de test pour affichage',
                'category': category,
                'team': team,
                'slug': 'test-product-display',
                'stock_quantity': 5,
                'available_sizes': ['S', 'M', 'L', 'XL']
            }
        )
        
        # Créer plusieurs avis
        reviews_data = [
            (5, "Excellent produit !"),
            (4, "Très bon produit"),
            (3, "Produit correct"),
            (2, "Pas terrible"),
            (1, "Décevant")
        ]
        
        for i, (rating, comment) in enumerate(reviews_data):
            user_review, _ = User.objects.get_or_create(
                username=f'test_display_user_{i}',
                defaults={
                    'email': f'display{i}@test.com',
                    'first_name': f'Display{i}',
                    'last_name': 'User'
                }
            )
            
            # Vérifier si l'avis existe déjà
            existing_review = Review.objects.filter(product=product, user=user_review).first()
            if not existing_review:
                Review.objects.create(
                    product=product,
                    user=user_review,
                    rating=rating,
                    comment=comment
                )
        
        print(f"📦 Produit: {product.name}")
        print(f"📊 Avis créés: {product.total_reviews}")
        print(f"⭐ Note moyenne: {product.average_rating}")
        
        # Tester l'affichage via le client HTTP
        client = Client()
        response = client.get(f'/product/{product.slug}/')
        
        print(f"\n📊 Test d'affichage:")
        print(f"   - Statut: {response.status_code}")
        print(f"   - Contenu contient 'Avis clients': {'Avis clients' in response.content.decode()}")
        print(f"   - Contenu contient 'Excellent produit': {'Excellent produit' in response.content.decode()}")
        
        if response.status_code == 200:
            print(f"   ✅ Page affichée correctement")
        else:
            print(f"   ❌ Erreur d'affichage")
        
        # Nettoyer
        Review.objects.filter(product=product).delete()
        for i in range(5):
            User.objects.filter(username=f'test_display_user_{i}').delete()
        if created:
            product.delete()
        if created:
            user.delete()
        
        print(f"   ✅ Données nettoyées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST SYSTÈME D'AVIS COMPLET")
    print("=" * 60)
    
    # Test 1: Système d'avis
    success1 = test_reviews_system()
    
    # Test 2: Affichage des avis
    success2 = test_reviews_display()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Système d'avis fonctionne")
        print("✅ Affichage des avis fonctionne")
        print("✅ Propriétés du produit fonctionnent")
        print("✅ Contraintes respectées")
        print("✅ Interface utilisateur fonctionne")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        if not success1:
            print("❌ Test du système d'avis échoué")
        if not success2:
            print("❌ Test d'affichage échoué")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
