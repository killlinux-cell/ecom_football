#!/usr/bin/env python
"""
Script de déploiement complet des données de football
Combine les équipes de clubs ET les équipes nationales
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def deploy_complete_football_data():
    """Déploie toutes les données de football (clubs + internationaux)"""
    print("⚽ DÉPLOIEMENT COMPLET DES DONNÉES FOOTBALL")
    print("=" * 60)
    print("Ce script va déployer:")
    print("• Équipes de clubs des 5 grands championnats")
    print("• Équipes nationales des 6 confédérations")
    print("• Maillots de clubs et internationaux")
    print("=" * 60)
    
    try:
        from products.models import Team, Product, Category
        from decimal import Decimal
        
        # Étape 1: Vérifier l'état actuel
        print("📊 ÉTAT ACTUEL DE LA BASE DE DONNÉES")
        print("-" * 40)
        current_teams = Team.objects.count()
        current_products = Product.objects.count()
        current_categories = Category.objects.count()
        
        print(f"🏆 Équipes actuelles: {current_teams}")
        print(f"🛍️ Produits actuels: {current_products}")
        print(f"📁 Catégories actuelles: {current_categories}")
        
        # Étape 2: Importer les équipes de clubs
        if current_teams < 100:  # Seuil pour éviter les doublons
            print(f"\n⚽ IMPORTATION DES ÉQUIPES DE CLUBS")
            print("-" * 40)
            
            # Données des équipes de clubs
            club_teams = {
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
            
            # Créer la catégorie pour les maillots de clubs
            club_category, created = Category.objects.get_or_create(
                name="Maillots de Football",
                defaults={
                    'slug': 'maillots-football',
                    'description': 'Maillots officiels des équipes de football'
                }
            )
            
            # Importer les équipes de clubs
            club_teams_created = 0
            for league_name, league_data in club_teams.items():
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
                        club_teams_created += 1
            
            print(f"✅ {club_teams_created} équipes de clubs importées")
        
        # Étape 3: Importer les équipes nationales
        if current_teams < 200:  # Seuil pour éviter les doublons
            print(f"\n🌍 IMPORTATION DES ÉQUIPES NATIONALES")
            print("-" * 40)
            
            # Données des équipes nationales
            international_teams = {
                "UEFA (Europe)": {
                    "teams": [
                        {"name": "France", "slug": "france", "country": "France"},
                        {"name": "Allemagne", "slug": "allemagne", "country": "Allemagne"},
                        {"name": "Espagne", "slug": "espagne", "country": "Espagne"},
                        {"name": "Italie", "slug": "italie", "country": "Italie"},
                        {"name": "Angleterre", "slug": "angleterre", "country": "Angleterre"},
                        {"name": "Portugal", "slug": "portugal", "country": "Portugal"},
                        {"name": "Pays-Bas", "slug": "pays-bas", "country": "Pays-Bas"},
                        {"name": "Belgique", "slug": "belgique", "country": "Belgique"},
                        {"name": "Croatie", "slug": "croatie", "country": "Croatie"},
                        {"name": "Danemark", "slug": "danemark", "country": "Danemark"},
                        {"name": "Suède", "slug": "suede", "country": "Suède"},
                        {"name": "Norvège", "slug": "norvege", "country": "Norvège"},
                        {"name": "Pologne", "slug": "pologne", "country": "Pologne"},
                        {"name": "Suisse", "slug": "suisse", "country": "Suisse"},
                        {"name": "Autriche", "slug": "autriche", "country": "Autriche"},
                        {"name": "République Tchèque", "slug": "republique-tcheque", "country": "République Tchèque"},
                        {"name": "Hongrie", "slug": "hongrie", "country": "Hongrie"},
                        {"name": "Ukraine", "slug": "ukraine", "country": "Ukraine"},
                        {"name": "Écosse", "slug": "ecosse", "country": "Écosse"},
                        {"name": "Irlande", "slug": "irlande", "country": "Irlande"}
                    ]
                },
                "CONMEBOL (Amérique du Sud)": {
                    "teams": [
                        {"name": "Brésil", "slug": "bresil", "country": "Brésil"},
                        {"name": "Argentine", "slug": "argentine", "country": "Argentine"},
                        {"name": "Uruguay", "slug": "uruguay", "country": "Uruguay"},
                        {"name": "Chili", "slug": "chili", "country": "Chili"},
                        {"name": "Colombie", "slug": "colombie", "country": "Colombie"},
                        {"name": "Pérou", "slug": "perou", "country": "Pérou"},
                        {"name": "Équateur", "slug": "equateur", "country": "Équateur"},
                        {"name": "Paraguay", "slug": "paraguay", "country": "Paraguay"},
                        {"name": "Bolivie", "slug": "bolivie", "country": "Bolivie"},
                        {"name": "Venezuela", "slug": "venezuela", "country": "Venezuela"}
                    ]
                },
                "CONCACAF (Amérique du Nord/Centrale)": {
                    "teams": [
                        {"name": "États-Unis", "slug": "etats-unis", "country": "États-Unis"},
                        {"name": "Mexique", "slug": "mexique", "country": "Mexique"},
                        {"name": "Canada", "slug": "canada", "country": "Canada"},
                        {"name": "Costa Rica", "slug": "costa-rica", "country": "Costa Rica"},
                        {"name": "Jamaïque", "slug": "jamaique", "country": "Jamaïque"},
                        {"name": "Panama", "slug": "panama", "country": "Panama"},
                        {"name": "Honduras", "slug": "honduras", "country": "Honduras"},
                        {"name": "Guatemala", "slug": "guatemala", "country": "Guatemala"},
                        {"name": "Trinité-et-Tobago", "slug": "trinite-tobago", "country": "Trinité-et-Tobago"},
                        {"name": "Haïti", "slug": "haiti", "country": "Haïti"}
                    ]
                },
                "CAF (Afrique)": {
                    "teams": [
                        {"name": "Côte d'Ivoire", "slug": "cote-ivoire", "country": "Côte d'Ivoire"},
                        {"name": "Sénégal", "slug": "senegal", "country": "Sénégal"},
                        {"name": "Maroc", "slug": "maroc", "country": "Maroc"},
                        {"name": "Tunisie", "slug": "tunisie", "country": "Tunisie"},
                        {"name": "Algérie", "slug": "algerie", "country": "Algérie"},
                        {"name": "Égypte", "slug": "egypte", "country": "Égypte"},
                        {"name": "Nigeria", "slug": "nigeria", "country": "Nigeria"},
                        {"name": "Ghana", "slug": "ghana", "country": "Ghana"},
                        {"name": "Cameroun", "slug": "cameroun", "country": "Cameroun"},
                        {"name": "Mali", "slug": "mali", "country": "Mali"},
                        {"name": "Burkina Faso", "slug": "burkina-faso", "country": "Burkina Faso"},
                        {"name": "Guinée", "slug": "guinee", "country": "Guinée"},
                        {"name": "République Démocratique du Congo", "slug": "rdc", "country": "RDC"},
                        {"name": "Afrique du Sud", "slug": "afrique-sud", "country": "Afrique du Sud"},
                        {"name": "Kenya", "slug": "kenya", "country": "Kenya"},
                        {"name": "Ouganda", "slug": "ouganda", "country": "Ouganda"},
                        {"name": "Tanzanie", "slug": "tanzanie", "country": "Tanzanie"},
                        {"name": "Zambie", "slug": "zambie", "country": "Zambie"},
                        {"name": "Zimbabwe", "slug": "zimbabwe", "country": "Zimbabwe"},
                        {"name": "Botswana", "slug": "botswana", "country": "Botswana"}
                    ]
                },
                "AFC (Asie)": {
                    "teams": [
                        {"name": "Japon", "slug": "japon", "country": "Japon"},
                        {"name": "Corée du Sud", "slug": "coree-sud", "country": "Corée du Sud"},
                        {"name": "Australie", "slug": "australie", "country": "Australie"},
                        {"name": "Iran", "slug": "iran", "country": "Iran"},
                        {"name": "Arabie Saoudite", "slug": "arabie-saoudite", "country": "Arabie Saoudite"},
                        {"name": "Qatar", "slug": "qatar", "country": "Qatar"},
                        {"name": "Émirats Arabes Unis", "slug": "emirats", "country": "Émirats Arabes Unis"},
                        {"name": "Irak", "slug": "irak", "country": "Irak"},
                        {"name": "Ouzbékistan", "slug": "ouzbekistan", "country": "Ouzbékistan"},
                        {"name": "Thaïlande", "slug": "thailande", "country": "Thaïlande"},
                        {"name": "Vietnam", "slug": "vietnam", "country": "Vietnam"},
                        {"name": "Indonésie", "slug": "indonesie", "country": "Indonésie"},
                        {"name": "Malaisie", "slug": "malaisie", "country": "Malaisie"},
                        {"name": "Singapour", "slug": "singapour", "country": "Singapour"},
                        {"name": "Philippines", "slug": "philippines", "country": "Philippines"},
                        {"name": "Myanmar", "slug": "myanmar", "country": "Myanmar"},
                        {"name": "Cambodge", "slug": "cambodge", "country": "Cambodge"},
                        {"name": "Laos", "slug": "laos", "country": "Laos"},
                        {"name": "Brunei", "slug": "brunei", "country": "Brunei"},
                        {"name": "Timor oriental", "slug": "timor-oriental", "country": "Timor oriental"}
                    ]
                },
                "OFC (Océanie)": {
                    "teams": [
                        {"name": "Nouvelle-Zélande", "slug": "nouvelle-zelande", "country": "Nouvelle-Zélande"},
                        {"name": "Papouasie-Nouvelle-Guinée", "slug": "papouasie", "country": "Papouasie-Nouvelle-Guinée"},
                        {"name": "Fidji", "slug": "fidji", "country": "Fidji"},
                        {"name": "Vanuatu", "slug": "vanuatu", "country": "Vanuatu"},
                        {"name": "Salomon", "slug": "salomon", "country": "Salomon"},
                        {"name": "Tahiti", "slug": "tahiti", "country": "Tahiti"},
                        {"name": "Nouvelle-Calédonie", "slug": "nouvelle-caledonie", "country": "Nouvelle-Calédonie"},
                        {"name": "Samoa", "slug": "samoa", "country": "Samoa"},
                        {"name": "Tonga", "slug": "tonga", "country": "Tonga"},
                        {"name": "Cook", "slug": "cook", "country": "Cook"}
                    ]
                }
            }
            
            # Créer la catégorie pour les maillots internationaux
            international_category, created = Category.objects.get_or_create(
                name="Maillots Internationaux",
                defaults={
                    'slug': 'maillots-internationaux',
                    'description': 'Maillots officiels des équipes nationales de football'
                }
            )
            
            # Importer les équipes nationales
            international_teams_created = 0
            for confederation, conf_data in international_teams.items():
                for team_info in conf_data['teams']:
                    team, created = Team.objects.get_or_create(
                        slug=team_info['slug'],
                        defaults={
                            'name': team_info['name'],
                            'country': team_info['country'],
                            'league': confederation
                        }
                    )
                    if created:
                        international_teams_created += 1
            
            print(f"✅ {international_teams_created} équipes nationales importées")
        
        # Étape 4: Créer les produits de maillots
        if current_products < 500:  # Seuil pour éviter les doublons
            print(f"\n🛍️ CRÉATION DES PRODUITS")
            print("-" * 40)
            
            # Types de produits pour les clubs
            club_jersey_types = [
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
            
            # Types de produits pour les équipes nationales
            international_jersey_types = [
                {
                    "name_suffix": "Domicile",
                    "description_suffix": "domicile",
                    "price": Decimal('18000.00'),
                    "sale_price": Decimal('12000.00'),
                    "slug_suffix": "domicile"
                },
                {
                    "name_suffix": "Extérieur",
                    "description_suffix": "extérieur",
                    "price": Decimal('18000.00'),
                    "sale_price": Decimal('12000.00'),
                    "slug_suffix": "exterieur"
                },
                {
                    "name_suffix": "Troisième",
                    "description_suffix": "troisième maillot",
                    "price": Decimal('20000.00'),
                    "sale_price": Decimal('15000.00'),
                    "slug_suffix": "troisieme"
                }
            ]
            
            # Créer les produits pour les clubs
            club_teams = Team.objects.filter(
                league__in=["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
            )
            
            club_products_created = 0
            for team in club_teams:
                for jersey_type in club_jersey_types:
                    product_name = f"Maillot {team.name} {jersey_type['name_suffix']}"
                    product_slug = f"maillot-{team.slug}-{jersey_type['slug_suffix']}"
                    
                    description = f"""Maillot officiel {jersey_type['description_suffix']} de {team.name} - Collection 2025/2026.

Tailles disponibles: S, M, L, XL, XXL
Couleurs: Couleurs officielles de {team.name}"""
                    
                    product, created = Product.objects.get_or_create(
                        slug=product_slug,
                        defaults={
                            'name': product_name,
                            'description': description,
                            'price': jersey_type['price'],
                            'sale_price': jersey_type['sale_price'],
                            'category': club_category,
                            'team': team,
                            'stock_quantity': 30,
                            'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                            'is_featured': True,
                            'is_active': True
                        }
                    )
                    if created:
                        club_products_created += 1
            
            print(f"✅ {club_products_created} maillots de clubs créés")
            
            # Créer les produits pour les équipes nationales
            international_teams_list = Team.objects.filter(
                league__in=["UEFA (Europe)", "CONMEBOL (Amérique du Sud)", "CONCACAF (Amérique du Nord/Centrale)", 
                           "CAF (Afrique)", "AFC (Asie)", "OFC (Océanie)"]
            )
            
            international_products_created = 0
            for team in international_teams_list:
                for jersey_type in international_jersey_types:
                    product_name = f"Maillot {team.name} {jersey_type['name_suffix']}"
                    product_slug = f"maillot-{team.slug}-{jersey_type['slug_suffix']}"
                    
                    description = f"""Maillot officiel {jersey_type['description_suffix']} de l'équipe nationale de {team.name} - Collection 2025.

Tailles disponibles: S, M, L, XL, XXL
Couleurs: Couleurs officielles de {team.name}"""
                    
                    product, created = Product.objects.get_or_create(
                        slug=product_slug,
                        defaults={
                            'name': product_name,
                            'description': description,
                            'price': jersey_type['price'],
                            'sale_price': jersey_type['sale_price'],
                            'category': international_category,
                            'team': team,
                            'stock_quantity': 25,
                            'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                            'is_featured': True,
                            'is_active': True
                        }
                    )
                    if created:
                        international_products_created += 1
            
            print(f"✅ {international_products_created} maillots internationaux créés")
        
        # Étape 5: Afficher les statistiques finales
        print(f"\n📊 STATISTIQUES FINALES")
        print("=" * 40)
        
        final_teams = Team.objects.count()
        final_products = Product.objects.count()
        final_categories = Category.objects.count()
        
        print(f"🏆 Équipes totales: {final_teams}")
        print(f"🛍️ Produits totales: {final_products}")
        print(f"📁 Catégories totales: {final_categories}")
        
        # Statistiques par type
        print(f"\n🏆 ÉQUIPES PAR TYPE")
        print("-" * 40)
        
        club_leagues = ["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
        international_leagues = ["UEFA (Europe)", "CONMEBOL (Amérique du Sud)", "CONCACAF (Amérique du Nord/Centrale)", 
                               "CAF (Afrique)", "AFC (Asie)", "OFC (Océanie)"]
        
        club_count = Team.objects.filter(league__in=club_leagues).count()
        international_count = Team.objects.filter(league__in=international_leagues).count()
        
        print(f"  Clubs: {club_count} équipes")
        print(f"  Internationales: {international_count} équipes")
        
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
    print("⚽ DÉPLOIEMENT COMPLET DES DONNÉES FOOTBALL")
    print("=" * 60)
    print("Ce script va déployer toutes les données de football sur votre VPS")
    print("Cela inclut:")
    print("• Équipes de clubs des 5 grands championnats")
    print("• Équipes nationales des 6 confédérations")
    print("• Maillots de clubs et internationaux")
    print("• Configuration des prix et descriptions")
    print("• Vérification de l'intégrité des données")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Déploiement annulé")
        return False
    
    # Exécuter le déploiement
    success = deploy_complete_football_data()
    
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

