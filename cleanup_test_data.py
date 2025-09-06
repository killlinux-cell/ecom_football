#!/usr/bin/env python
"""
Script de nettoyage des données de test
Supprime les équipes et produits de test créés lors des tests
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def cleanup_test_data():
    """Nettoie les données de test"""
    print("🧹 NETTOYAGE DES DONNÉES DE TEST")
    print("=" * 60)
    
    try:
        from products.models import Team, Product, Category
        
        # Équipes de test à supprimer
        test_team_patterns = [
            "Test Team",
            "Test Category",
            "TEST Product",
            "test_review_user",
            "test_display_user"
        ]
        
        # Supprimer les équipes de test
        teams_deleted = 0
        for pattern in test_team_patterns:
            teams = Team.objects.filter(name__icontains=pattern)
            count = teams.count()
            if count > 0:
                print(f"🗑️ Suppression de {count} équipes contenant '{pattern}'")
                teams.delete()
                teams_deleted += count
        
        # Supprimer les produits de test
        products_deleted = 0
        for pattern in test_team_patterns:
            products = Product.objects.filter(name__icontains=pattern)
            count = products.count()
            if count > 0:
                print(f"🗑️ Suppression de {count} produits contenant '{pattern}'")
                products.delete()
                products_deleted += count
        
        # Supprimer les catégories de test
        categories_deleted = 0
        for pattern in test_team_patterns:
            categories = Category.objects.filter(name__icontains=pattern)
            count = categories.count()
            if count > 0:
                print(f"🗑️ Suppression de {count} catégories contenant '{pattern}'")
                categories.delete()
                categories_deleted += count
        
        print(f"\n📊 RÉSUMÉ DU NETTOYAGE")
        print("=" * 40)
        print(f"🗑️ Équipes supprimées: {teams_deleted}")
        print(f"🗑️ Produits supprimés: {products_deleted}")
        print(f"🗑️ Catégories supprimées: {categories_deleted}")
        
        # Afficher les statistiques finales
        print(f"\n📈 STATISTIQUES FINALES")
        print("=" * 40)
        print(f"🏆 Équipes restantes: {Team.objects.count()}")
        print(f"🛍️ Produits restants: {Product.objects.count()}")
        print(f"📁 Catégories restantes: {Category.objects.count()}")
        
        # Statistiques par championnat
        print(f"\n🏆 ÉQUIPES PAR CHAMPIONNAT")
        print("-" * 40)
        leagues = ["Ligue 1", "La Liga", "Bundesliga", "Serie A", "Premier League"]
        for league in leagues:
            count = Team.objects.filter(league=league).count()
            print(f"  {league}: {count} équipes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🧹 NETTOYAGE DES DONNÉES DE TEST")
    print("=" * 60)
    print("Ce script va supprimer toutes les données de test créées lors des tests")
    print("Cela inclut:")
    print("• Équipes de test")
    print("• Produits de test")
    print("• Catégories de test")
    print("• Utilisateurs de test")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\nVoulez-vous continuer ? (o/n): ").lower().strip()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Nettoyage annulé")
        return False
    
    # Exécuter le nettoyage
    success = cleanup_test_data()
    
    if success:
        print(f"\n🎉 NETTOYAGE TERMINÉ!")
        print("=" * 60)
        print("✅ Toutes les données de test ont été supprimées")
        print("✅ Seules les vraies équipes de football restent")
        print("✅ Votre base de données est propre et prête pour la production!")
    else:
        print(f"\n❌ ERREUR LORS DU NETTOYAGE")
        print("⚠️ Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
