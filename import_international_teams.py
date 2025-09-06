#!/usr/bin/env python
"""
Script d'importation des équipes nationales de football
Importe les équipes des principales compétitions internationales
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def import_international_teams():
    """Importe les équipes nationales de football"""
    print("🌍 IMPORTATION DES ÉQUIPES NATIONALES")
    print("=" * 60)
    
    try:
        from products.models import Team, Product, Category
        from decimal import Decimal
        
        # Données des équipes nationales par confédération
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
        category, created = Category.objects.get_or_create(
            name="Maillots Internationaux",
            defaults={
                'slug': 'maillots-internationaux',
                'description': 'Maillots officiels des équipes nationales de football'
            }
        )
        
        if created:
            print(f"✅ Catégorie créée: {category.name}")
        else:
            print(f"📁 Catégorie existante: {category.name}")
        
        # Importer les équipes
        total_created = 0
        for confederation, conf_data in international_teams.items():
            print(f"\n🌍 {confederation}")
            print("-" * 40)
            
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
                    total_created += 1
                    print(f"  ✅ Créée: {team.name}")
                else:
                    print(f"  📁 Existe: {team.name}")
        
        print(f"\n✅ {total_created} équipes internationales importées")
        
        # Créer les produits de maillots
        print(f"\n🛍️ CRÉATION DES MAILLOTS INTERNATIONAUX")
        print("-" * 40)
        
        # Types de maillots internationaux
        jersey_types = [
            {
                "name_suffix": "Domicile",
                "description_suffix": "domicile",
                "price": Decimal('18000.00'),
                "sale_price": Decimal('10000.00'),
                "slug_suffix": "domicile"
            },
            {
                "name_suffix": "Extérieur",
                "description_suffix": "extérieur",
                "price": Decimal('18000.00'),
                "sale_price": Decimal('10000.00'),
                "slug_suffix": "exterieur"
            },
            {
                "name_suffix": "Troisième",
                "description_suffix": "troisième maillot",
                "price": Decimal('20000.00'),
                "sale_price": Decimal('10000.00'),
                "slug_suffix": "troisieme"
            }
        ]
        
        # Récupérer toutes les équipes internationales
        international_teams_list = Team.objects.filter(
            league__in=["UEFA (Europe)", "CONMEBOL (Amérique du Sud)", "CONCACAF (Amérique du Nord/Centrale)", 
                       "CAF (Afrique)", "AFC (Asie)", "OFC (Océanie)"]
        )
        
        products_created = 0
        for team in international_teams_list:
            for jersey_type in jersey_types:
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
                        'category': category,
                        'team': team,
                        'stock_quantity': 25,
                        'available_sizes': ['S', 'M', 'L', 'XL', 'XXL'],
                        'is_featured': False,
                        'is_active': True
                    }
                )
                
                if created:
                    products_created += 1
        
        print(f"✅ {products_created} maillots internationaux créés")
        
        # Afficher les statistiques finales
        print(f"\n📊 STATISTIQUES FINALES")
        print("=" * 40)
        
        final_teams = Team.objects.count()
        final_products = Product.objects.count()
        
        print(f"🏆 Équipes totales: {final_teams}")
        print(f"🛍️ Produits totales: {final_products}")
        
        # Statistiques par confédération
        print(f"\n🌍 ÉQUIPES PAR CONFÉDÉRATION")
        print("-" * 40)
        
        confederations = ["UEFA (Europe)", "CONMEBOL (Amérique du Sud)", "CONCACAF (Amérique du Nord/Centrale)", 
                         "CAF (Afrique)", "AFC (Asie)", "OFC (Océanie)"]
        
        for confederation in confederations:
            count = Team.objects.filter(league=confederation).count()
            print(f"  {confederation}: {count} équipes")
        
        # Produits en promotion
        promo_count = Product.objects.filter(sale_price__isnull=False).count()
        print(f"\n💰 PRODUITS EN PROMOTION: {promo_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'importation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🌍 IMPORTATION DES ÉQUIPES NATIONALES")
    print("=" * 60)
    print("Ce script va importer les équipes nationales de football")
    print("Cela inclut:")
    print("• Équipes de l'UEFA (Europe)")
    print("• Équipes de la CONMEBOL (Amérique du Sud)")
    print("• Équipes de la CONCACAF (Amérique du Nord/Centrale)")
    print("• Équipes de la CAF (Afrique)")
    print("• Équipes de l'AFC (Asie)")
    print("• Équipes de l'OFC (Océanie)")
    print("• Création des maillots officiels")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Importation annulée")
        return False
    
    # Exécuter l'importation
    success = import_international_teams()
    
    if success:
        print(f"\n🎉 IMPORTATION TERMINÉE!")
        print("=" * 60)
        print("✅ Toutes les équipes nationales ont été importées")
        print("✅ Les maillots internationaux ont été créés")
        print("✅ Votre catalogue est maintenant complet!")
        print("✅ Vous pouvez ajouter les images des produits")
    else:
        print(f"\n❌ ERREUR LORS DE L'IMPORTATION")
        print("⚠️ Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

