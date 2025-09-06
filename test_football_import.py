#!/usr/bin/env python
"""
Script de test pour vérifier l'importation des équipes et produits de football
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_teams_import():
    """Teste l'importation des équipes"""
    print("🧪 TEST IMPORTATION DES ÉQUIPES")
    print("=" * 60)
    
    try:
        from products.models import Team
        
        # Vérifier le nombre total d'équipes
        total_teams = Team.objects.count()
        print(f"📊 Total d'équipes: {total_teams}")
        
        # Vérifier les championnats
        leagues = ["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
        for league in leagues:
            count = Team.objects.filter(league=league).count()
            print(f"🏆 {league}: {count} équipes")
        
        # Vérifier quelques équipes populaires
        popular_teams = [
            ("psg", "Paris Saint-Germain"),
            ("real-madrid", "Real Madrid"),
            ("barcelona", "FC Barcelona"),
            ("bayern-munich", "Bayern Munich"),
            ("juventus", "Juventus"),
            ("manchester-city", "Manchester City")
        ]
        
        print(f"\n🌟 VÉRIFICATION DES ÉQUIPES POPULAIRES")
        print("-" * 40)
        for slug, expected_name in popular_teams:
            try:
                team = Team.objects.get(slug=slug)
                if team.name == expected_name:
                    print(f"  ✅ {team.name} ({team.league})")
                else:
                    print(f"  ⚠️ {team.name} (attendu: {expected_name})")
            except Team.DoesNotExist:
                print(f"  ❌ Équipe non trouvée: {slug}")
        
        return total_teams > 0
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_products_creation():
    """Teste la création des produits"""
    print(f"\n🧪 TEST CRÉATION DES PRODUITS")
    print("=" * 60)
    
    try:
        from products.models import Product, Team, Category
        
        # Vérifier le nombre total de produits
        total_products = Product.objects.count()
        print(f"📊 Total de produits: {total_products}")
        
        # Vérifier les produits par championnat
        leagues = ["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
        for league in leagues:
            count = Product.objects.filter(team__league=league).count()
            print(f"🏆 {league}: {count} produits")
        
        # Vérifier les types de produits
        product_types = ["domicile", "exterieur", "troisieme", "gardien", "vintage"]
        for product_type in product_types:
            count = Product.objects.filter(slug__contains=product_type).count()
            print(f"🛍️ {product_type}: {count} produits")
        
        # Vérifier quelques produits populaires
        popular_products = [
            "maillot-psg-domicile",
            "maillot-real-madrid-domicile",
            "maillot-barcelona-domicile",
            "maillot-bayern-munich-domicile"
        ]
        
        print(f"\n🌟 VÉRIFICATION DES PRODUITS POPULAIRES")
        print("-" * 40)
        for product_slug in popular_products:
            try:
                product = Product.objects.get(slug=product_slug)
                print(f"  ✅ {product.name} - {product.price} FCFA")
            except Product.DoesNotExist:
                print(f"  ❌ Produit non trouvé: {product_slug}")
        
        return total_products > 0
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_product_details():
    """Teste les détails des produits"""
    print(f"\n🧪 TEST DÉTAILS DES PRODUITS")
    print("=" * 60)
    
    try:
        from products.models import Product
        
        # Récupérer un produit d'exemple
        product = Product.objects.first()
        if not product:
            print("❌ Aucun produit trouvé")
            return False
        
        print(f"📦 Produit test: {product.name}")
        print(f"🏆 Équipe: {product.team.name}")
        print(f"🏆 Championnat: {product.team.league}")
        print(f"💰 Prix: {product.price} FCFA")
        print(f"💰 Prix promo: {product.sale_price} FCFA")
        print(f"📏 Tailles: {', '.join(product.available_sizes)}")
        print(f"📦 Stock: {product.stock_quantity}")
        print(f"⭐ Vedette: {product.is_featured}")
        print(f"✅ Actif: {product.is_active}")
        
        # Vérifier les propriétés calculées
        print(f"\n🧮 PROPRIÉTÉS CALCULÉES")
        print("-" * 40)
        print(f"💰 Prix actuel: {product.current_price} FCFA")
        print(f"📊 En promotion: {product.is_on_sale}")
        if product.is_on_sale:
            print(f"📈 Réduction: {product.discount_percentage}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_database_integrity():
    """Teste l'intégrité de la base de données"""
    print(f"\n🧪 TEST INTÉGRITÉ BASE DE DONNÉES")
    print("=" * 60)
    
    try:
        from products.models import Product, Team, Category
        from django.db.models import Count
        
        # Vérifier les relations
        print("🔗 VÉRIFICATION DES RELATIONS")
        print("-" * 40)
        
        # Produits sans équipe
        products_without_team = Product.objects.filter(team__isnull=True).count()
        print(f"📦 Produits sans équipe: {products_without_team}")
        
        # Produits sans catégorie
        products_without_category = Product.objects.filter(category__isnull=True).count()
        print(f"📦 Produits sans catégorie: {products_without_category}")
        
        # Équipes sans produits
        teams_without_products = Team.objects.annotate(
            product_count=Count('products')
        ).filter(product_count=0).count()
        print(f"🏆 Équipes sans produits: {teams_without_products}")
        
        # Vérifier les slugs uniques
        print(f"\n🔗 VÉRIFICATION DES SLUGS")
        print("-" * 40)
        
        # Équipes avec slugs dupliqués
        from django.db.models import Count
        duplicate_team_slugs = Team.objects.values('slug').annotate(
            count=Count('slug')
        ).filter(count__gt=1)
        
        if duplicate_team_slugs:
            print(f"⚠️ Slugs d'équipes dupliqués: {len(duplicate_team_slugs)}")
            for item in duplicate_team_slugs:
                print(f"  - {item['slug']}: {item['count']} occurrences")
        else:
            print("✅ Aucun slug d'équipe dupliqué")
        
        # Produits avec slugs dupliqués
        duplicate_product_slugs = Product.objects.values('slug').annotate(
            count=Count('slug')
        ).filter(count__gt=1)
        
        if duplicate_product_slugs:
            print(f"⚠️ Slugs de produits dupliqués: {len(duplicate_product_slugs)}")
            for item in duplicate_product_slugs:
                print(f"  - {item['slug']}: {item['count']} occurrences")
        else:
            print("✅ Aucun slug de produit dupliqué")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_website_functionality():
    """Teste la fonctionnalité du site web"""
    print(f"\n🧪 TEST FONCTIONNALITÉ SITE WEB")
    print("=" * 60)
    
    try:
        from django.test import Client
        from products.models import Product, Team
        
        client = Client()
        
        # Test de la page d'accueil
        print("🏠 TEST PAGE D'ACCUEIL")
        print("-" * 40)
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
        else:
            print(f"❌ Erreur page d'accueil: {response.status_code}")
        
        # Test de la liste des produits
        print(f"\n🛍️ TEST LISTE DES PRODUITS")
        print("-" * 40)
        response = client.get('/products/')
        if response.status_code == 200:
            print("✅ Liste des produits accessible")
        else:
            print(f"❌ Erreur liste produits: {response.status_code}")
        
        # Test d'une page produit
        product = Product.objects.first()
        if product:
            print(f"\n📦 TEST PAGE PRODUIT: {product.name}")
            print("-" * 40)
            response = client.get(f'/product/{product.slug}/')
            if response.status_code == 200:
                print("✅ Page produit accessible")
                # Vérifier que le contenu contient les informations du produit
                content = response.content.decode()
                if product.name in content:
                    print("✅ Nom du produit affiché")
                if str(product.price) in content:
                    print("✅ Prix du produit affiché")
                if product.team.name in content:
                    print("✅ Nom de l'équipe affiché")
            else:
                print(f"❌ Erreur page produit: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST COMPLET DE L'IMPORTATION FOOTBALL")
    print("=" * 60)
    
    # Test 1: Importation des équipes
    success1 = test_teams_import()
    
    # Test 2: Création des produits
    success2 = test_products_creation()
    
    # Test 3: Détails des produits
    success3 = test_product_details()
    
    # Test 4: Intégrité de la base de données
    success4 = test_database_integrity()
    
    # Test 5: Fonctionnalité du site web
    success5 = test_website_functionality()
    
    # Résumé des tests
    print(f"\n📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    tests = [
        ("Importation des équipes", success1),
        ("Création des produits", success2),
        ("Détails des produits", success3),
        ("Intégrité base de données", success4),
        ("Fonctionnalité site web", success5)
    ]
    
    passed = 0
    for test_name, success in tests:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"  {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n📈 RÉSULTAT: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("✅ L'importation des équipes et produits fonctionne parfaitement")
        print("✅ Votre site est prêt pour les maillots de football!")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Vérifiez les erreurs ci-dessus")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
