#!/usr/bin/env python
"""
Script pour corriger les prix des personnalisations
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_customization_prices():
    """Corrige les prix des personnalisations"""
    print("🔧 CORRECTION DES PRIX DE PERSONNALISATIONS")
    print("=" * 60)
    
    try:
        from products.models import JerseyCustomization, CartItemCustomization
        from decimal import Decimal
        
        # Analyser les personnalisations actuelles
        customizations = JerseyCustomization.objects.all()
        print(f"📊 {customizations.count()} personnalisation(s) trouvée(s)")
        
        for cust in customizations:
            print(f"\n🎨 {cust.name} ({cust.customization_type})")
            print(f"   - Prix actuel: {cust.price} FCFA")
            
            # Proposer de nouveaux prix plus raisonnables
            if cust.customization_type == 'name':
                new_price = Decimal('500.00')  # 500 FCFA par caractère au lieu de 5000
                print(f"   - Nouveau prix proposé: {new_price} FCFA par caractère")
                print(f"   - Exemple: 'MESSI 10' (8 chars) = {new_price * 8} FCFA")
            elif cust.customization_type == 'badge':
                new_price = Decimal('2000.00')  # 2000 FCFA au lieu de 8000
                print(f"   - Nouveau prix proposé: {new_price} FCFA")
            elif cust.customization_type == 'color':
                new_price = Decimal('3000.00')  # 3000 FCFA au lieu de 10000
                print(f"   - Nouveau prix proposé: {new_price} FCFA")
            elif cust.customization_type == 'size':
                new_price = Decimal('5000.00')  # 5000 FCFA au lieu de 15000
                print(f"   - Nouveau prix proposé: {new_price} FCFA")
            else:
                new_price = cust.price  # Garder le prix actuel
                print(f"   - Prix inchangé: {new_price} FCFA")
            
            # Demander confirmation
            response = input(f"\nVoulez-vous modifier le prix de '{cust.name}'? (y/n): ")
            
            if response.lower() == 'y':
                old_price = cust.price
                cust.price = new_price
                cust.save()
                
                print(f"   ✅ Prix modifié: {old_price} → {new_price} FCFA")
                
                # Recalculer les personnalisations existantes
                existing_customizations = CartItemCustomization.objects.filter(customization=cust)
                if existing_customizations.exists():
                    print(f"   🔄 Recalcul de {existing_customizations.count()} personnalisation(s) existante(s)...")
                    
                    for custom in existing_customizations:
                        if cust.customization_type == 'name' and custom.custom_text:
                            custom.price = new_price * len(custom.custom_text) * custom.quantity
                        else:
                            custom.price = new_price * custom.quantity
                        custom.save()
                    
                    print(f"   ✅ Personnalisations recalculées")
            else:
                print(f"   ❌ Prix inchangé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def test_new_pricing():
    """Teste les nouveaux prix"""
    print("\n🧪 TEST DES NOUVEAUX PRIX")
    print("=" * 60)
    
    try:
        from products.models import JerseyCustomization
        from decimal import Decimal
        
        # Tester avec des exemples réalistes
        name_cust = JerseyCustomization.objects.filter(customization_type='name').first()
        
        if name_cust:
            print(f"📝 Test de la personnalisation 'Nom et Numéro':")
            print(f"   - Prix par caractère: {name_cust.price} FCFA")
            
            test_cases = [
                "MESSI 10",      # 8 caractères
                "NEYMAR JR 11",  # 12 caractères
                "RONALDO 7",     # 9 caractères
                "BENZEMA 9",     # 9 caractères
            ]
            
            print(f"\n   🧪 Calculs avec les nouveaux prix:")
            for text in test_cases:
                price = name_cust.price * len(text)
                print(f"      - '{text}' ({len(text)} chars): {price} FCFA")
                
                # Vérifier si c'est raisonnable
                if price > 10000:
                    print(f"        ⚠️ Encore trop cher!")
                elif price > 5000:
                    print(f"        ⚠️ Cher mais acceptable")
                else:
                    print(f"        ✅ Prix raisonnable")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION DES PRIX DE PERSONNALISATIONS")
    print("=" * 60)
    
    # Corriger les prix
    success1 = fix_customization_prices()
    
    # Tester les nouveaux prix
    success2 = test_new_pricing()
    
    if success1 and success2:
        print("\n🎉 CORRECTION TERMINÉE!")
        print("✅ Les prix des personnalisations ont été corrigés")
        print("✅ Les calculs sont maintenant cohérents")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ Des problèmes persistent")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
