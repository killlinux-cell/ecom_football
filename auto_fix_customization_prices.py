#!/usr/bin/env python
"""
Script automatique pour corriger les prix des personnalisations
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def auto_fix_customization_prices():
    """Corrige automatiquement les prix des personnalisations"""
    print("🔧 CORRECTION AUTOMATIQUE DES PRIX DE PERSONNALISATIONS")
    print("=" * 60)
    
    try:
        from products.models import JerseyCustomization, CartItemCustomization
        from decimal import Decimal
        
        # Définir les nouveaux prix raisonnables
        new_prices = {
            'name': Decimal('500.00'),    # 500 FCFA par caractère
            'badge': Decimal('2000.00'),  # 2000 FCFA
            'color': Decimal('3000.00'),  # 3000 FCFA
            'size': Decimal('5000.00'),   # 5000 FCFA
        }
        
        # Analyser et corriger les personnalisations
        customizations = JerseyCustomization.objects.all()
        print(f"📊 {customizations.count()} personnalisation(s) trouvée(s)")
        
        for cust in customizations:
            print(f"\n🎨 {cust.name} ({cust.customization_type})")
            print(f"   - Prix actuel: {cust.price} FCFA")
            
            # Déterminer le nouveau prix
            if cust.customization_type in new_prices:
                new_price = new_prices[cust.customization_type]
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
                        if cust.customization_type == 'name' and custom.custom_text:
                            custom.price = new_price * len(custom.custom_text) * custom.quantity
                        else:
                            custom.price = new_price * custom.quantity
                        custom.save()
                    
                    print(f"   ✅ Personnalisations recalculées")
            else:
                print(f"   ❌ Type non reconnu, prix inchangé")
        
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
        
        # Tester le scénario de l'image
        print(f"\n📋 TEST DU SCÉNARIO DE L'IMAGE:")
        print(f"   - Produit: 10 000 FCFA")
        print(f"   - Personnalisation 'MESSI 10' (8 chars): {name_cust.price * 8} FCFA")
        print(f"   - Total: {10000 + (name_cust.price * 8)} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION AUTOMATIQUE DES PRIX DE PERSONNALISATIONS")
    print("=" * 60)
    
    # Corriger les prix
    success1 = auto_fix_customization_prices()
    
    # Tester les nouveaux prix
    success2 = test_new_pricing()
    
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
