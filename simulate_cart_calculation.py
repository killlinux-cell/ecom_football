#!/usr/bin/env python
"""
Script pour simuler le calcul du panier et identifier l'incohérence
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def simulate_cart_scenario():
    """Simule le scénario de l'image pour identifier l'incohérence"""
    print("🧮 SIMULATION DU CALCUL DU PANIER")
    print("=" * 60)
    
    try:
        from products.models import Product, JerseyCustomization
        from decimal import Decimal
        
        # Scénario 1: Produit à 10 000 FCFA (comme dans l'image)
        print("📋 SCÉNARIO 1: Produit à 10 000 FCFA")
        print("-" * 40)
        
        base_price = Decimal('10000.00')
        quantity = 1
        subtotal_expected = Decimal('59500.00')
        
        print(f"   - Prix de base: {base_price} FCFA")
        print(f"   - Quantité: {quantity}")
        print(f"   - Sous-total attendu: {subtotal_expected} FCFA")
        print(f"   - Différence: {subtotal_expected - base_price} FCFA")
        
        # Analyser les personnalisations possibles
        customizations = JerseyCustomization.objects.all()
        print(f"\n   🎨 Personnalisations disponibles:")
        
        for cust in customizations:
            print(f"      - {cust.name}: {cust.price} FCFA")
            
            # Calculer combien de personnalisations il faudrait
            if cust.price > 0:
                needed = (subtotal_expected - base_price) / cust.price
                print(f"        → Il faudrait {needed:.1f} de cette personnalisation")
        
        # Scénario 2: Produit Barcelone réel (45 000 FCFA)
        print(f"\n📋 SCÉNARIO 2: Produit Barcelone réel")
        print("-" * 40)
        
        barcelone_products = Product.objects.filter(name__icontains='barcelone')
        if barcelone_products.exists():
            product = barcelone_products.first()
            print(f"   - Produit: {product.name}")
            print(f"   - Prix réel: {product.current_price} FCFA")
            print(f"   - Quantité: 1")
            print(f"   - Sous-total attendu: {subtotal_expected} FCFA")
            print(f"   - Différence: {subtotal_expected - product.current_price} FCFA")
            
            # Vérifier si c'est cohérent
            if abs(subtotal_expected - product.current_price) < 1000:
                print(f"   ✅ COHÉRENT: Le prix correspond au sous-total!")
            else:
                print(f"   ❌ INCOHÉRENT: Différence de {subtotal_expected - product.current_price} FCFA")
        
        # Scénario 3: Calcul avec personnalisations
        print(f"\n📋 SCÉNARIO 3: Calcul avec personnalisations")
        print("-" * 40)
        
        # Simuler différentes combinaisons de personnalisations
        combinations = [
            ("Nom et Numéro (10 caractères)", Decimal('5000.00') * 10),  # 50 000 FCFA
            ("Nom et Numéro (20 caractères)", Decimal('5000.00') * 20),  # 100 000 FCFA
            ("Couleurs Personnalisées", Decimal('10000.00')),            # 10 000 FCFA
            ("Logo Personnalisé", Decimal('8000.00')),                   # 8 000 FCFA
            ("Taille Spéciale", Decimal('15000.00')),                    # 15 000 FCFA
        ]
        
        for name, price in combinations:
            total = base_price + price
            print(f"   - {name}: {price} FCFA")
            print(f"     → Total: {base_price} + {price} = {total} FCFA")
            
            if abs(total - subtotal_expected) < 1000:
                print(f"     ✅ CORRESPOND AU SOUS-TOTAL ATTENDU!")
                print(f"     🎯 SOLUTION TROUVÉE: {name}")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la simulation: {str(e)}")
        return False

def analyze_pricing_logic():
    """Analyse la logique de calcul des prix"""
    print("\n🔍 ANALYSE DE LA LOGIQUE DE CALCUL")
    print("=" * 60)
    
    try:
        from products.models import JerseyCustomization
        
        # Analyser la logique de calcul des personnalisations
        name_customization = JerseyCustomization.objects.filter(
            customization_type='name'
        ).first()
        
        if name_customization:
            print(f"📝 Personnalisation 'Nom et Numéro':")
            print(f"   - Prix unitaire: {name_customization.price} FCFA")
            print(f"   - Logique: Prix × nombre de caractères")
            
            # Tester différentes longueurs de texte
            test_texts = [
                "MESSI 10",      # 8 caractères
                "NEYMAR JR 11",  # 12 caractères
                "RONALDO 7",     # 9 caractères
                "BENZEMA 9",     # 9 caractères
            ]
            
            print(f"\n   🧪 Tests avec différents textes:")
            for text in test_texts:
                price = name_customization.price * len(text)
                print(f"      - '{text}' ({len(text)} chars): {price} FCFA")
                
                # Vérifier si cela explique l'incohérence
                if price > 40000:
                    print(f"        ⚠️ PRIX TRÈS ÉLEVÉ!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        return False

def main():
    """Fonction principale de simulation"""
    print("🔧 SIMULATION DU CALCUL DU PANIER")
    print("=" * 60)
    
    tests = [
        ("Simulation du scénario", simulate_cart_scenario),
        ("Analyse de la logique de calcul", analyze_pricing_logic),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA SIMULATION:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"   {status} - {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 SIMULATION TERMINÉE!")
        print("✅ L'incohérence a été identifiée")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ L'incohérence reste inexpliquée")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
