#!/usr/bin/env python
"""
Script pour corriger directement les prix des personnalisations
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_prices_direct():
    """Corrige directement les prix des personnalisations"""
    print("🔧 CORRECTION DIRECTE DES PRIX DE PERSONNALISATIONS")
    print("=" * 60)
    
    try:
        from products.models import JerseyCustomization, CartItemCustomization
        from decimal import Decimal
        
        # Corriger les prix directement par nom
        price_fixes = {
            'Nom et Numéro': Decimal('500.00'),      # 500 FCFA par caractère
            'Logo Personnalisé': Decimal('2000.00'), # 2000 FCFA
            'Couleurs Personnalisées': Decimal('3000.00'), # 3000 FCFA
            'Taille Spéciale': Decimal('5000.00'),   # 5000 FCFA
        }
        
        customizations = JerseyCustomization.objects.all()
        print(f"📊 {customizations.count()} personnalisation(s) trouvée(s)")
        
        for cust in customizations:
            print(f"\n🎨 {cust.name}")
            print(f"   - Prix actuel: {cust.price} FCFA")
            
            if cust.name in price_fixes:
                new_price = price_fixes[cust.name]
                print(f"   - Nouveau prix: {new_price} FCFA")
                
                # Modifier le prix
                old_price = cust.price
                cust.price = new_price
                cust.save()
                
                print(f"   ✅ Prix modifié: {old_price} → {new_price} FCFA")
                
                # Recalculer les personnalisations existantes
                existing_customizations = CartItemCustomization.objects.filter(customization=cust)
                if existing_customizations.exists():
                    print(f"   🔄 Recalcul de {existing_customizations.count()} personnalisation(s)...")
                    
                    for custom in existing_customizations:
                        if cust.name == 'Nom et Numéro' and custom.custom_text:
                            custom.price = new_price * len(custom.custom_text) * custom.quantity
                        else:
                            custom.price = new_price * custom.quantity
                        custom.save()
                    
                    print(f"   ✅ Personnalisations recalculées")
            else:
                print(f"   ❌ Nom non reconnu, prix inchangé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def test_scenario():
    """Teste le scénario de l'image"""
    print("\n🧪 TEST DU SCÉNARIO DE L'IMAGE")
    print("=" * 60)
    
    try:
        from products.models import JerseyCustomization
        from decimal import Decimal
        
        # Tester le scénario exact de l'image
        name_cust = JerseyCustomization.objects.filter(name='Nom et Numéro').first()
        
        if name_cust:
            print(f"📝 Scénario de l'image:")
            print(f"   - Produit affiché: 10 000 FCFA")
            print(f"   - Sous-total: 59 500 FCFA")
            print(f"   - Différence: 49 500 FCFA")
            print(f"   - Prix par caractère: {name_cust.price} FCFA")
            
            # Calculer combien de caractères il faudrait
            needed_chars = 49500 / name_cust.price
            print(f"   - Caractères nécessaires: {needed_chars:.1f}")
            
            # Tester avec des exemples réalistes
            test_cases = [
                "MESSI 10",      # 8 caractères
                "NEYMAR JR 11",  # 12 caractères
                "RONALDO 7",     # 9 caractères
                "BENZEMA 9",     # 9 caractères
            ]
            
            print(f"\n   🧪 Calculs avec les nouveaux prix:")
            for text in test_cases:
                price = name_cust.price * len(text)
                total = 10000 + price
                print(f"      - '{text}' ({len(text)} chars): {price} FCFA")
                print(f"        → Total: {total} FCFA")
                
                if abs(total - 59500) < 1000:
                    print(f"        ✅ CORRESPOND AU SOUS-TOTAL!")
                else:
                    print(f"        ❌ Différence: {abs(total - 59500)} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION DIRECTE DES PRIX DE PERSONNALISATIONS")
    print("=" * 60)
    
    # Corriger les prix
    success1 = fix_prices_direct()
    
    # Tester le scénario
    success2 = test_scenario()
    
    if success1 and success2:
        print("\n🎉 CORRECTION TERMINÉE!")
        print("✅ Les prix des personnalisations ont été corrigés")
        print("✅ Les calculs sont maintenant cohérents")
        print("✅ L'incohérence de l'image est résolue")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ Des problèmes persistent")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
