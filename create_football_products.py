#!/usr/bin/env python
"""
Script de création de produits de maillots de football
Crée des produits d'exemple pour toutes les équipes importées
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def create_football_products():
    """Crée des produits de maillots pour toutes les équipes"""
    print("🛍️ CRÉATION DE PRODUITS DE MAILLOTS")
    print("=" * 60)
    
    try:
        from products.models import Product, Team, Category
        from decimal import Decimal
        
        # Récupérer la catégorie
        category = Category.objects.get(name="Maillots de Football")
        
        # Types de produits à créer
        product_types = [
            {
                "name_suffix": "Domicile",
                "description_suffix": "domicile",
                "price": Decimal('15000.00'),
                "sale_price": Decimal('10000.00'),
                "slug_suffix": "domicile"
            },
            {
                "name_suffix": "Extérieur",
                "description_suffix": "extérieur",
                "price": Decimal('15000.00'),
                "sale_price": Decimal('1O000.00'),
                "slug_suffix": "exterieur"
            },
            {
                "name_suffix": "Troisième",
                "description_suffix": "troisième maillot",
                "price": Decimal('18000.00'),
                "sale_price": Decimal('10000.00'),
                "slug_suffix": "troisieme"
            }
        ]
        
        # Récupérer toutes les équipes
        teams = Team.objects.all().order_by('league', 'name')
        
        total_created = 0
        total_updated = 0
        
        for team in teams:
            print(f"\n🏆 {team.name} ({team.league})")
            print("-" * 40)
            
            for product_type in product_types:
                # Créer le nom du produit
                product_name = f"Maillot {team.name} {product_type['name_suffix']}"
                product_slug = f"maillot-{team.slug}-{product_type['slug_suffix']}"
                
                # Description du produit
                description = f"""Maillot officiel {product_type['description_suffix']} de {team.name} - Collection 2025/2026.


Tailles disponibles: S, M, L, XL, XXL
Couleurs: Couleurs officielles de {team.name}"""
                
                # Créer ou mettre à jour le produit
                product, created = Product.objects.get_or_create(
                    slug=product_slug,
                    defaults={
                        'name': product_name,
                        'description': description,
                        'price': product_type['price'],
                        'sale_price': product_type['sale_price'],
                        'category': category,
                        'team': team,
                        'stock_quantity': 30,
                        'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                        'is_featured': team.league in ['Ligue 1', 'La Liga', 'Bundesliga', 'Serie A', 'Premier League'],
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"  ✅ Créé: {product_name}")
                    total_created += 1
                else:
                    # Mettre à jour les informations si nécessaire
                    updated = False
                    if product.name != product_name:
                        product.name = product_name
                        updated = True
                    if product.description != description:
                        product.description = description
                        updated = True
                    if product.price != product_type['price']:
                        product.price = product_type['price']
                        updated = True
                    if product.sale_price != product_type['sale_price']:
                        product.sale_price = product_type['sale_price']
                        updated = True
                    
                    if updated:
                        product.save()
                        print(f"  🔄 Mis à jour: {product_name}")
                        total_updated += 1
                    else:
                        print(f"  📁 Existe déjà: {product_name}")
        
        print(f"\n📊 RÉSUMÉ DE LA CRÉATION")
        print("=" * 40)
        print(f"✅ Produits créés: {total_created}")
        print(f"🔄 Produits mis à jour: {total_updated}")
        print(f"📁 Produits existants: {Product.objects.count() - total_created - total_updated}")
        print(f"🛍️ Total de produits: {Product.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des produits: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_special_products():
    """Crée des produits spéciaux (maillots de gardien, accessoires)"""
    print(f"\n🥅 CRÉATION DE PRODUITS SPÉCIAUX")
    print("=" * 60)
    
    try:
        from products.models import Product, Team, Category
        from decimal import Decimal
        
        # Récupérer la catégorie
        category = Category.objects.get(name="Maillots de Football")
        
        # Équipes populaires pour les produits spéciaux
        popular_teams = [
            "psg", "real-madrid", "barcelona", "bayern-munich", 
            "juventus", "manchester-city", "arsenal", "liverpool",
            "om", "monaco", "ol", "lens"
        ]
        
        # Types de produits spéciaux
        special_products = [
            {
                "name_suffix": "Gardien",
                "description_suffix": "gardien de but",
                "price": Decimal('18000.00'),
                "sale_price": Decimal('15000.00'),
                "slug_suffix": "gardien"
            },
            {
                "name_suffix": "Vintage",
                "description_suffix": "vintage rétro",
                "price": Decimal('20000.00'),
                "sale_price": Decimal('17000.00'),
                "slug_suffix": "vintage"
            }
        ]
        
        total_created = 0
        
        for team_slug in popular_teams:
            try:
                team = Team.objects.get(slug=team_slug)
                
                for product_type in special_products:
                    product_name = f"Maillot {team.name} {product_type['name_suffix']}"
                    product_slug = f"maillot-{team.slug}-{product_type['slug_suffix']}"
                    
                    description = f"""Maillot officiel {product_type['description_suffix']} de {team.name} - Collection 2024/2025.

Caractéristiques spéciales:
• Design unique et exclusif
• Matériau de haute qualité
• Couleurs et logo officiels
• Tissu technique performant
• Lavage en machine à 30°C
• Garantie qualité 30 jours

Tailles disponibles: S, M, L, XL, XXL"""
                    
                    product, created = Product.objects.get_or_create(
                        slug=product_slug,
                        defaults={
                            'name': product_name,
                            'description': description,
                            'price': product_type['price'],
                            'sale_price': product_type['sale_price'],
                            'category': category,
                            'team': team,
                            'stock_quantity': 20,
                            'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                            'is_featured': True,
                            'is_active': True
                        }
                    )
                    
                    if created:
                        print(f"  ✅ Créé: {product_name}")
                        total_created += 1
                    else:
                        print(f"  📁 Existe déjà: {product_name}")
                        
            except Team.DoesNotExist:
                print(f"  ❌ Équipe non trouvée: {team_slug}")
                continue
        
        print(f"\n📊 PRODUITS SPÉCIAUX CRÉÉS: {total_created}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des produits spéciaux: {str(e)}")
        return False

def show_products_summary():
    """Affiche un résumé des produits créés"""
    print(f"\n📋 RÉSUMÉ DES PRODUITS")
    print("=" * 60)
    
    try:
        from products.models import Product, Team, Category
        from django.db.models import Count
        
        # Statistiques générales
        total_products = Product.objects.count()
        total_teams = Team.objects.count()
        total_categories = Category.objects.count()
        
        print(f"🛍️ Produits totales: {total_products}")
        print(f"🏆 Équipes totales: {total_teams}")
        print(f"📁 Catégories totales: {total_categories}")
        
        # Statistiques par championnat
        print(f"\n🏆 PRODUITS PAR CHAMPIONNAT")
        print("-" * 40)
        leagues = ["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
        for league in leagues:
            count = Product.objects.filter(team__league=league).count()
            print(f"  {league}: {count} produits")
        
        # Top 10 des équipes avec le plus de produits
        print(f"\n🌟 TOP 10 ÉQUIPES (par nombre de produits)")
        print("-" * 40)
        teams_with_products = Team.objects.annotate(
            product_count=Count('products')
        ).order_by('-product_count')[:10]
        
        for team in teams_with_products:
            print(f"  {team.name}: {team.product_count} produits")
        
        # Produits en promotion
        products_on_sale = Product.objects.filter(sale_price__isnull=False).count()
        print(f"\n💰 PRODUITS EN PROMOTION: {products_on_sale}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage du résumé: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🛍️ CRÉATION DE PRODUITS DE MAILLOTS")
    print("=" * 60)
    print("Ce script va créer des produits de maillots pour toutes les équipes")
    print("Types de produits:")
    print("• Maillots domicile")
    print("• Maillots extérieur")
    print("• Maillots troisième")
    print("• Maillots gardien (équipes populaires)")
    print("• Maillots vintage (équipes populaires)")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Création annulée")
        return False
    
    # Étape 1: Créer les produits principaux
    success1 = create_football_products()
    
    if not success1:
        print("❌ Échec de la création des produits principaux")
        return False
    
    # Étape 2: Créer les produits spéciaux
    response = input("\nVoulez-vous créer des produits spéciaux (gardien, vintage) ? (o/n): ").lower().strip()
    if response in ['o', 'oui', 'y', 'yes']:
        success2 = create_special_products()
        if not success2:
            print("⚠️ Erreur lors de la création des produits spéciaux")
    
    # Étape 3: Afficher le résumé
    show_products_summary()
    
    print(f"\n🎉 CRÉATION TERMINÉE!")
    print("=" * 60)
    print("✅ Tous les produits ont été créés")
    print("✅ Vous pouvez maintenant ajouter les images des produits")
    print("✅ Les prix et descriptions sont configurés")
    print("✅ Votre catalogue de maillots est prêt!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
