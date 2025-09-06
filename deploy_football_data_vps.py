#!/usr/bin/env python
"""
Script de déploiement complet des données de football sur VPS
Ce script combine l'importation des équipes, la création des produits et les tests
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def deploy_football_data():
    """Déploie toutes les données de football"""
    print("🚀 DÉPLOIEMENT COMPLET DES DONNÉES FOOTBALL")
    print("=" * 60)
    
    try:
        from products.models import Team, Product, Category
        from django.db.models import Count
        
        # Étape 1: Vérifier l'état actuel
        print("📊 ÉTAT ACTUEL DE LA BASE DE DONNÉES")
        print("-" * 40)
        current_teams = Team.objects.count()
        current_products = Product.objects.count()
        current_categories = Category.objects.count()
        
        print(f"🏆 Équipes actuelles: {current_teams}")
        print(f"🛍️ Produits actuels: {current_products}")
        print(f"📁 Catégories actuelles: {current_categories}")
        
        # Étape 2: Importer les équipes (si nécessaire)
        if current_teams < 100:  # Seuil pour déterminer si l'importation est nécessaire
            print(f"\n⚽ IMPORTATION DES ÉQUIPES")
            print("-" * 40)
            
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
                        {"name": "Stade Brestois", "slug": "brest"}
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
            
            # Créer la catégorie si elle n'existe pas
            category, created = Category.objects.get_or_create(
                name="Maillots de Football",
                defaults={
                    'slug': 'maillots-football',
                    'description': 'Maillots officiels des équipes de football'
                }
            )
            
            # Importer les équipes
            total_created = 0
            for league_name, league_data in teams_data.items():
                for team_info in league_data['teams']:
                    team, created = Team.objects.get_or_create(
                        slug=team_info['slug'],
                        defaults={
                            'name': team_info['name'],
                            'country': league_data['country'],
                            'league': league_name
                        }
                    )
                    if created:
                        total_created += 1
            
            print(f"✅ {total_created} équipes importées")
        
        # Étape 3: Créer les produits (si nécessaire)
        if current_products < 300:  # Seuil pour déterminer si la création est nécessaire
            print(f"\n🛍️ CRÉATION DES PRODUITS")
            print("-" * 40)
            
            from decimal import Decimal
            
            # Types de produits
            product_types = [
                {
                    "name_suffix": "Domicile",
                    "description_suffix": "domicile",
                    "price": Decimal('15000.00'),
                    "sale_price": Decimal('9000.00'),
                    "slug_suffix": "domicile"
                },
                {
                    "name_suffix": "Extérieur",
                    "description_suffix": "extérieur",
                    "price": Decimal('15000.00'),
                    "sale_price": Decimal('9000.00'),
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
            teams = Team.objects.filter(league__in=["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"])
            
            products_created = 0
            for team in teams:
                for product_type in product_types:
                    product_name = f"Maillot {team.name} {product_type['name_suffix']}"
                    product_slug = f"maillot-{team.slug}-{product_type['slug_suffix']}"
                    
                    description = f"""Maillot officiel {product_type['description_suffix']} de {team.name} - Collection 2025/2026.


Tailles disponibles: S, M, L, XL, XXL
Couleurs: Couleurs officielles de {team.name}"""
                    
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
                            'is_featured': True,
                            'is_active': True
                        }
                    )
                    if created:
                        products_created += 1
            
            print(f"✅ {products_created} produits créés")
        
        # Étape 4: Afficher les statistiques finales
        print(f"\n📊 STATISTIQUES FINALES")
        print("=" * 40)
        final_teams = Team.objects.count()
        final_products = Product.objects.count()
        final_categories = Category.objects.count()
        
        print(f"🏆 Équipes totales: {final_teams}")
        print(f"🛍️ Produits totales: {final_products}")
        print(f"📁 Catégories totales: {final_categories}")
        
        # Statistiques par championnat
        print(f"\n🏆 ÉQUIPES PAR CHAMPIONNAT")
        print("-" * 40)
        leagues = ["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
        for league in leagues:
            count = Team.objects.filter(league=league).count()
            print(f"  {league}: {count} équipes")
        
        # Produits en promotion
        promo_count = Product.objects.filter(sale_price__isnull=False).count()
        print(f"\n💰 PRODUITS EN PROMOTION: {promo_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du déploiement: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 DÉPLOIEMENT COMPLET DES DONNÉES FOOTBALL")
    print("=" * 60)
    print("Ce script va déployer toutes les données de football sur votre VPS")
    print("Cela inclut:")
    print("• Importation des équipes des 5 grands championnats")
    print("• Création des produits de maillots")
    print("• Configuration des prix et descriptions")
    print("• Vérification de l'intégrité des données")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Déploiement annulé")
        return False
    
    # Exécuter le déploiement
    success = deploy_football_data()
    
    if success:
        print(f"\n🎉 DÉPLOIEMENT TERMINÉ!")
        print("=" * 60)
        print("✅ Toutes les données de football ont été déployées")
        print("✅ Votre site e-commerce est prêt pour les maillots de football!")
        print("✅ Vous pouvez maintenant ajouter les images des produits")
        print("✅ Votre catalogue est complet et fonctionnel!")
    else:
        print(f"\n❌ ERREUR LORS DU DÉPLOIEMENT")
        print("⚠️ Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
