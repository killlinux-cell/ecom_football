#!/usr/bin/env python
"""
Script d'importation des équipes de football des 5 grands championnats européens
- Ligue 1 (France)
- La Liga (Espagne) 
- Bundesliga (Allemagne)
- Serie A (Italie)
- Premier League (Angleterre)
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def import_football_teams():
    """Importe toutes les équipes des 5 grands championnats"""
    print("⚽ IMPORTATION DES ÉQUIPES DE FOOTBALL")
    print("=" * 60)
    
    try:
        from products.models import Team, Category
        from django.utils.text import slugify
        
        # Créer la catégorie "Maillots de Football" si elle n'existe pas
        category, created = Category.objects.get_or_create(
            name="Maillots de Football",
            defaults={
                'slug': 'maillots-football',
                'description': 'Maillots officiels des équipes de football'
            }
        )
        
        if created:
            print(f"✅ Catégorie créée: {category.name}")
        else:
            print(f"📁 Catégorie existante: {category.name}")
        
        # Données des équipes par championnat
        teams_data = {
            "Ligue 1": {
                "country": "France",
                "teams": [
                    {"name": "Paris Saint-Germain", "slug": "psg"},
                    {"name": "Olympique de Marseille", "slug": "om"},
                    {"name": "AS Monaco", "slug": "monaco"},
                    {"name": "Olympique Lyonnais", "slug": "ol"},
                    {"name": "RC Lens", "slug": "lens"},
                    {"name": "Stade Rennais", "slug": "rennes"},
                    {"name": "OGC Nice", "slug": "nice"},
                    {"name": "LOSC Lille", "slug": "lille"},
                    {"name": "FC Nantes", "slug": "nantes"},
                    {"name": "Montpellier HSC", "slug": "montpellier"},
                    {"name": "Toulouse FC", "slug": "toulouse"},
                    {"name": "Stade de Reims", "slug": "reims"},
                    {"name": "RC Strasbourg", "slug": "strasbourg"},
                    {"name": "FC Lorient", "slug": "lorient"},
                    {"name": "Clermont Foot", "slug": "clermont"},
                    {"name": "Le Havre AC", "slug": "le-havre"},
                    {"name": "FC Metz", "slug": "metz"},
                    {"name": "Stade Brestois", "slug": "brest"},
                    {"name": "RC Strasbourg", "slug": "strasbourg"},
                    {"name": "FC Nantes", "slug": "nantes"}
                ]
            },
            "La Liga": {
                "country": "Espagne",
                "teams": [
                    {"name": "Real Madrid", "slug": "real-madrid"},
                    {"name": "FC Barcelona", "slug": "barcelona"},
                    {"name": "Atletico Madrid", "slug": "atletico-madrid"},
                    {"name": "Real Sociedad", "slug": "real-sociedad"},
                    {"name": "Villarreal CF", "slug": "villarreal"},
                    {"name": "Real Betis", "slug": "real-betis"},
                    {"name": "Sevilla FC", "slug": "sevilla"},
                    {"name": "Athletic Bilbao", "slug": "athletic-bilbao"},
                    {"name": "Valencia CF", "slug": "valencia"},
                    {"name": "Getafe CF", "slug": "getafe"},
                    {"name": "CA Osasuna", "slug": "osasuna"},
                    {"name": "Girona FC", "slug": "girona"},
                    {"name": "UD Las Palmas", "slug": "las-palmas"},
                    {"name": "Rayo Vallecano", "slug": "rayo-vallecano"},
                    {"name": "Real Mallorca", "slug": "mallorca"},
                    {"name": "Cadiz CF", "slug": "cadiz"},
                    {"name": "Celta Vigo", "slug": "celta-vigo"},
                    {"name": "Alaves", "slug": "alaves"},
                    {"name": "Granada CF", "slug": "granada"},
                    {"name": "UD Almeria", "slug": "almeria"}
                ]
            },
            "Bundesliga": {
                "country": "Allemagne",
                "teams": [
                    {"name": "Bayern Munich", "slug": "bayern-munich"},
                    {"name": "Borussia Dortmund", "slug": "borussia-dortmund"},
                    {"name": "RB Leipzig", "slug": "rb-leipzig"},
                    {"name": "Bayer Leverkusen", "slug": "bayer-leverkusen"},
                    {"name": "Eintracht Frankfurt", "slug": "eintracht-frankfurt"},
                    {"name": "VfL Wolfsburg", "slug": "wolfsburg"},
                    {"name": "SC Freiburg", "slug": "freiburg"},
                    {"name": "1. FC Union Berlin", "slug": "union-berlin"},
                    {"name": "Borussia Monchengladbach", "slug": "monchengladbach"},
                    {"name": "VfB Stuttgart", "slug": "stuttgart"},
                    {"name": "1. FC Koln", "slug": "koln"},
                    {"name": "TSG Hoffenheim", "slug": "hoffenheim"},
                    {"name": "Werder Bremen", "slug": "werder-bremen"},
                    {"name": "1. FSV Mainz 05", "slug": "mainz"},
                    {"name": "FC Augsburg", "slug": "augsburg"},
                    {"name": "VfL Bochum", "slug": "bochum"},
                    {"name": "1. FC Heidenheim", "slug": "heidenheim"},
                    {"name": "SV Darmstadt 98", "slug": "darmstadt"}
                ]
            },
            "Serie A": {
                "country": "Italie",
                "teams": [
                    {"name": "Juventus", "slug": "juventus"},
                    {"name": "AC Milan", "slug": "ac-milan"},
                    {"name": "Inter Milan", "slug": "inter-milan"},
                    {"name": "Napoli", "slug": "napoli"},
                    {"name": "AS Roma", "slug": "as-roma"},
                    {"name": "Atalanta", "slug": "atalanta"},
                    {"name": "Lazio", "slug": "lazio"},
                    {"name": "Fiorentina", "slug": "fiorentina"},
                    {"name": "Bologna", "slug": "bologna"},
                    {"name": "Torino", "slug": "torino"},
                    {"name": "Genoa", "slug": "genoa"},
                    {"name": "Monza", "slug": "monza"},
                    {"name": "Lecce", "slug": "lecce"},
                    {"name": "Sassuolo", "slug": "sassuolo"},
                    {"name": "Udinese", "slug": "udinese"},
                    {"name": "Cagliari", "slug": "cagliari"},
                    {"name": "Verona", "slug": "verona"},
                    {"name": "Empoli", "slug": "empoli"},
                    {"name": "Frosinone", "slug": "frosinone"},
                    {"name": "Salernitana", "slug": "salernitana"}
                ]
            },
            "Premier League": {
                "country": "Angleterre",
                "teams": [
                    {"name": "Manchester City", "slug": "manchester-city"},
                    {"name": "Arsenal", "slug": "arsenal"},
                    {"name": "Liverpool", "slug": "liverpool"},
                    {"name": "Manchester United", "slug": "manchester-united"},
                    {"name": "Newcastle United", "slug": "newcastle"},
                    {"name": "Tottenham Hotspur", "slug": "tottenham"},
                    {"name": "Brighton & Hove Albion", "slug": "brighton"},
                    {"name": "Aston Villa", "slug": "aston-villa"},
                    {"name": "West Ham United", "slug": "west-ham"},
                    {"name": "Chelsea", "slug": "chelsea"},
                    {"name": "Fulham", "slug": "fulham"},
                    {"name": "Brentford", "slug": "brentford"},
                    {"name": "Crystal Palace", "slug": "crystal-palace"},
                    {"name": "Wolverhampton Wanderers", "slug": "wolves"},
                    {"name": "Everton", "slug": "everton"},
                    {"name": "Nottingham Forest", "slug": "nottingham-forest"},
                    {"name": "Luton Town", "slug": "luton-town"},
                    {"name": "Burnley", "slug": "burnley"},
                    {"name": "Sheffield United", "slug": "sheffield-united"},
                    {"name": "Bournemouth", "slug": "bournemouth"}
                ]
            }
        }
        
        total_created = 0
        total_updated = 0
        
        # Parcourir chaque championnat
        for league_name, league_data in teams_data.items():
            print(f"\n🏆 {league_name} ({league_data['country']})")
            print("-" * 40)
            
            for team_info in league_data['teams']:
                team_name = team_info['name']
                team_slug = team_info['slug']
                
                # Créer ou mettre à jour l'équipe
                team, created = Team.objects.get_or_create(
                    slug=team_slug,
                    defaults={
                        'name': team_name,
                        'country': league_data['country'],
                        'league': league_name
                    }
                )
                
                if created:
                    print(f"  ✅ Créée: {team_name}")
                    total_created += 1
                else:
                    # Mettre à jour les informations si nécessaire
                    updated = False
                    if team.name != team_name:
                        team.name = team_name
                        updated = True
                    if team.country != league_data['country']:
                        team.country = league_data['country']
                        updated = True
                    if team.league != league_name:
                        team.league = league_name
                        updated = True
                    
                    if updated:
                        team.save()
                        print(f"  🔄 Mise à jour: {team_name}")
                        total_updated += 1
                    else:
                        print(f"  📁 Existe déjà: {team_name}")
        
        print(f"\n📊 RÉSUMÉ DE L'IMPORTATION")
        print("=" * 40)
        print(f"✅ Équipes créées: {total_created}")
        print(f"🔄 Équipes mises à jour: {total_updated}")
        print(f"📁 Équipes existantes: {Team.objects.count() - total_created - total_updated}")
        print(f"🏆 Total d'équipes: {Team.objects.count()}")
        
        # Afficher les statistiques par championnat
        print(f"\n📈 STATISTIQUES PAR CHAMPIONNAT")
        print("=" * 40)
        for league_name in teams_data.keys():
            count = Team.objects.filter(league=league_name).count()
            print(f"🏆 {league_name}: {count} équipes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'importation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_products():
    """Crée des produits d'exemple pour quelques équipes populaires"""
    print(f"\n🛍️ CRÉATION DE PRODUITS D'EXEMPLE")
    print("=" * 60)
    
    try:
        from products.models import Product, Team, Category
        from decimal import Decimal
        
        # Récupérer la catégorie
        category = Category.objects.get(name="Maillots de Football")
        
        # Équipes populaires pour créer des produits
        popular_teams = [
            "psg", "real-madrid", "barcelona", "bayern-munich", 
            "juventus", "manchester-city", "arsenal", "liverpool"
        ]
        
        products_created = 0
        
        for team_slug in popular_teams:
            try:
                team = Team.objects.get(slug=team_slug)
                
                # Créer un produit d'exemple
                product, created = Product.objects.get_or_create(
                    slug=f"maillot-{team_slug}-domicile",
                    defaults={
                        'name': f"Maillot {team.name} Domicile",
                        'description': f"Maillot officiel domicile de {team.name} - Collection 2024/2025. Matériau de haute qualité, respirant et confortable.",
                        'price': Decimal('15000.00'),
                        'sale_price': Decimal('12000.00'),
                        'category': category,
                        'team': team,
                        'stock_quantity': 50,
                        'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                        'is_featured': True,
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"  ✅ Produit créé: {product.name}")
                    products_created += 1
                else:
                    print(f"  📁 Produit existant: {product.name}")
                    
            except Team.DoesNotExist:
                print(f"  ❌ Équipe non trouvée: {team_slug}")
                continue
        
        print(f"\n📊 PRODUITS CRÉÉS: {products_created}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des produits: {str(e)}")
        return False

def show_import_summary():
    """Affiche un résumé de l'importation"""
    print(f"\n📋 RÉSUMÉ FINAL")
    print("=" * 60)
    
    try:
        from products.models import Team, Product, Category
        
        # Statistiques générales
        total_teams = Team.objects.count()
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        
        print(f"🏆 Équipes totales: {total_teams}")
        print(f"🛍️ Produits totales: {total_products}")
        print(f"📁 Catégories totales: {total_categories}")
        
        # Top 10 des équipes
        print(f"\n🌟 TOP 10 ÉQUIPES (par nombre de produits)")
        print("-" * 40)
        from django.db.models import Count
        teams_with_products = Team.objects.annotate(
            product_count=Count('products')
        ).order_by('-product_count')[:10]
        
        for team in teams_with_products:
            print(f"  {team.name}: {team.product_count} produits")
        
        # Statistiques par championnat
        print(f"\n🏆 STATISTIQUES PAR CHAMPIONNAT")
        print("-" * 40)
        leagues = ["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
        for league in leagues:
            count = Team.objects.filter(league=league).count()
            print(f"  {league}: {count} équipes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage du résumé: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("⚽ IMPORTATION DES ÉQUIPES DE FOOTBALL")
    print("=" * 60)
    print("Ce script va importer toutes les équipes des 5 grands championnats:")
    print("🏆 Ligue 1 (France)")
    print("🏆 La Liga (Espagne)")
    print("🏆 Bundesliga (Allemagne)")
    print("🏆 Serie A (Italie)")
    print("🏆 Premier League (Angleterre)")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Importation annulée")
        return False
    
    # Étape 1: Importer les équipes
    success1 = import_football_teams()
    
    if not success1:
        print("❌ Échec de l'importation des équipes")
        return False
    
    # Étape 2: Créer des produits d'exemple
    response = input("\nVoulez-vous créer des produits d'exemple ? (o/n): ").lower().strip()
    if response in ['o', 'oui', 'y', 'yes']:
        success2 = create_sample_products()
        if not success2:
            print("⚠️ Erreur lors de la création des produits d'exemple")
    
    # Étape 3: Afficher le résumé
    show_import_summary()
    
    print(f"\n🎉 IMPORTATION TERMINÉE!")
    print("=" * 60)
    print("✅ Toutes les équipes ont été importées")
    print("✅ Vous pouvez maintenant ajouter les images des équipes")
    print("✅ Les produits d'exemple ont été créés")
    print("✅ Votre site est prêt pour les maillots de football!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
