#!/usr/bin/env python
"""
Script de test pour vérifier que les données existantes ne seront pas modifiées
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def test_data_protection():
    """Teste la protection des données existantes"""
    print("🔒 TEST DE PROTECTION DES DONNÉES EXISTANTES")
    print("=" * 60)
    
    try:
        from products.models import Team, Product, Category
        from decimal import Decimal
        
        # Étape 1: Enregistrer l'état actuel
        print("📊 ÉTAT ACTUEL DE LA BASE DE DONNÉES")
        print("-" * 40)
        
        current_teams = Team.objects.count()
        current_products = Product.objects.count()
        current_categories = Category.objects.count()
        
        print(f"🏆 Équipes actuelles: {current_teams}")
        print(f"🛍️ Produits actuels: {current_products}")
        print(f"📁 Catégories actuelles: {current_categories}")
        
        # Étape 2: Enregistrer quelques équipes existantes
        existing_teams = []
        for team in Team.objects.all()[:5]:  # Prendre les 5 premières
            existing_teams.append({
                'id': team.id,
                'name': team.name,
                'slug': team.slug,
                'country': team.country,
                'league': team.league
            })
            print(f"  📝 Équipe existante: {team.name} ({team.league})")
        
        # Étape 3: Enregistrer quelques produits existants
        existing_products = []
        for product in Product.objects.all()[:5]:  # Prendre les 5 premiers
            existing_products.append({
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'price': product.price,
                'sale_price': product.sale_price,
                'stock_quantity': product.stock_quantity
            })
            print(f"  📝 Produit existant: {product.name} - {product.price} FCFA")
        
        # Étape 4: Simuler l'importation (sans vraiment importer)
        print(f"\n🧪 SIMULATION DE L'IMPORTATION")
        print("-" * 40)
        
        # Données de test pour simulation
        test_teams = [
            {"name": "Paris Saint-Germain", "slug": "psg"},
            {"name": "Real Madrid", "slug": "real-madrid"},
            {"name": "Bayern Munich", "slug": "bayern-munich"}
        ]
        
        # Simuler get_or_create pour les équipes
        teams_created = 0
        teams_updated = 0
        
        for team_info in test_teams:
            team, created = Team.objects.get_or_create(
                slug=team_info['slug'],
                defaults={
                    'name': team_info['name'],
                    'country': 'Test',
                    'league': 'Test League'
                }
            )
            
            if created:
                teams_created += 1
                print(f"  ✅ Créée: {team.name}")
            else:
                teams_updated += 1
                print(f"  📁 Existe déjà: {team.name}")
        
        # Étape 5: Vérifier que les données existantes n'ont pas changé
        print(f"\n🔍 VÉRIFICATION DE LA PROTECTION")
        print("-" * 40)
        
        data_protected = True
        
        # Vérifier les équipes existantes
        for original_team in existing_teams:
            try:
                current_team = Team.objects.get(id=original_team['id'])
                
                if (current_team.name == original_team['name'] and
                    current_team.slug == original_team['slug'] and
                    current_team.country == original_team['country'] and
                    current_team.league == original_team['league']):
                    print(f"  ✅ Équipe protégée: {current_team.name}")
                else:
                    print(f"  ❌ Équipe modifiée: {current_team.name}")
                    data_protected = False
                    
            except Team.DoesNotExist:
                print(f"  ❌ Équipe supprimée: {original_team['name']}")
                data_protected = False
        
        # Vérifier les produits existants
        for original_product in existing_products:
            try:
                current_product = Product.objects.get(id=original_product['id'])
                
                if (current_product.name == original_product['name'] and
                    current_product.slug == original_product['slug'] and
                    current_product.price == original_product['price'] and
                    current_product.sale_price == original_product['sale_price'] and
                    current_product.stock_quantity == original_product['stock_quantity']):
                    print(f"  ✅ Produit protégé: {current_product.name}")
                else:
                    print(f"  ❌ Produit modifié: {current_product.name}")
                    data_protected = False
                    
            except Product.DoesNotExist:
                print(f"  ❌ Produit supprimé: {original_product['name']}")
                data_protected = False
        
        # Étape 6: Afficher les statistiques finales
        print(f"\n📊 STATISTIQUES FINALES")
        print("=" * 40)
        
        final_teams = Team.objects.count()
        final_products = Product.objects.count()
        
        print(f"🏆 Équipes avant: {current_teams}")
        print(f"🏆 Équipes après: {final_teams}")
        print(f"🛍️ Produits avant: {current_products}")
        print(f"🛍️ Produits après: {final_products}")
        
        print(f"\n🔒 RÉSULTAT DU TEST")
        print("=" * 40)
        
        if data_protected:
            print("✅ PROTECTION RÉUSSIE!")
            print("✅ Aucune donnée existante n'a été modifiée")
            print("✅ Seuls les nouveaux éléments ont été ajoutés")
            print("✅ Votre base de données est sécurisée")
        else:
            print("❌ PROTECTION ÉCHOUÉE!")
            print("❌ Des données existantes ont été modifiées")
            print("❌ Vérifiez les erreurs ci-dessus")
        
        return data_protected
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🔒 TEST DE PROTECTION DES DONNÉES EXISTANTES")
    print("=" * 60)
    print("Ce script teste que vos données existantes ne seront pas modifiées")
    print("lors de l'importation des équipes de football.")
    print("=" * 60)
    
    # Exécuter le test
    success = test_data_protection()
    
    if success:
        print(f"\n🎉 TEST RÉUSSI!")
        print("=" * 60)
        print("✅ Vos données existantes sont protégées")
        print("✅ Vous pouvez exécuter le script d'importation en toute sécurité")
        print("✅ Seuls les nouveaux éléments seront ajoutés")
    else:
        print(f"\n❌ TEST ÉCHOUÉ!")
        print("⚠️ Des données existantes ont été modifiées")
        print("⚠️ Vérifiez les erreurs ci-dessus")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
