#!/usr/bin/env python
"""
Script pour retirer l'option is_featured des maillots de club
Permet de gérer manuellement cette option depuis l'admin
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def remove_featured_club_jerseys():
    """Retire l'option is_featured de tous les maillots de club"""
    print("🏆 RETRAIT DE L'OPTION IS_FEATURED DES MAILLOTS DE CLUB")
    print("=" * 60)
    
    try:
        from products.models import Product, Team
        
        # Identifier les équipes de club (exclure les équipes internationales)
        club_leagues = [
            "Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League",
            "Championship", "Ligue 2", "Segunda División", "2. Bundesliga",
            "Serie B", "Championship", "Eredivisie", "Primeira Liga",
            "Liga MX", "MLS", "J1 League", "K League", "A-League"
        ]
        
        # Récupérer les équipes de club
        club_teams = Team.objects.filter(league__in=club_leagues)
        print(f"🏆 Équipes de club identifiées: {club_teams.count()}")
        
        # Récupérer tous les produits de maillots de club
        club_products = Product.objects.filter(
            team__in=club_teams,
            is_featured=True
        )
        
        print(f"🛍️ Maillots de club avec is_featured=True: {club_products.count()}")
        
        if club_products.count() == 0:
            print("✅ Aucun maillot de club n'a l'option is_featured activée")
            return True
        
        # Afficher les produits qui seront modifiés
        print(f"\n📋 MAILLOTS QUI SERONT MODIFIÉS:")
        print("-" * 50)
        
        for product in club_products:
            print(f"  • {product.name} ({product.team.name})")
        
        # Demander confirmation
        print(f"\n⚠️  ATTENTION:")
        print(f"Cette action va retirer l'option 'is_featured' de {club_products.count()} maillots de club")
        print(f"Vous pourrez ensuite gérer cette option manuellement depuis l'admin")
        
        response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("❌ Opération annulée")
            return False
        
        # Retirer l'option is_featured
        updated_count = 0
        for product in club_products:
            product.is_featured = False
            product.save()
            updated_count += 1
            print(f"  ✅ {product.name} - is_featured retiré")
        
        print(f"\n🎉 OPÉRATION TERMINÉE!")
        print("=" * 50)
        print(f"✅ {updated_count} maillots de club modifiés")
        print(f"✅ Option is_featured retirée de tous les maillots de club")
        print(f"✅ Vous pouvez maintenant gérer cette option depuis l'admin")
        
        # Afficher les statistiques finales
        print(f"\n📊 STATISTIQUES FINALES:")
        print("-" * 30)
        
        total_club_products = Product.objects.filter(team__in=club_teams).count()
        featured_club_products = Product.objects.filter(
            team__in=club_teams,
            is_featured=True
        ).count()
        
        print(f"🏆 Total maillots de club: {total_club_products}")
        print(f"⭐ Maillots de club en vedette: {featured_club_products}")
        
        # Vérifier les maillots internationaux (ne pas les toucher)
        international_teams = Team.objects.exclude(league__in=club_leagues)
        international_products = Product.objects.filter(team__in=international_teams)
        featured_international = international_products.filter(is_featured=True).count()
        
        print(f"🌍 Maillots internationaux: {international_products.count()}")
        print(f"⭐ Maillots internationaux en vedette: {featured_international}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'opération: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏆 RETRAIT DE L'OPTION IS_FEATURED DES MAILLOTS DE CLUB")
    print("=" * 60)
    print("Ce script va retirer l'option 'is_featured' de tous les maillots de club")
    print("Cela vous permettra de gérer cette option manuellement depuis l'admin")
    print("=" * 60)
    
    # Exécuter l'opération
    success = remove_featured_club_jerseys()
    
    if success:
        print(f"\n🎉 OPÉRATION RÉUSSIE!")
        print("=" * 60)
        print("✅ Tous les maillots de club ont été modifiés")
        print("✅ Vous pouvez maintenant gérer is_featured depuis l'admin")
        print("✅ Les maillots internationaux n'ont pas été touchés")
    else:
        print(f"\n❌ ERREUR LORS DE L'OPÉRATION")
        print("⚠️ Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
