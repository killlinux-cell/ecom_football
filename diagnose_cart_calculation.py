#!/usr/bin/env python
"""
Script de diagnostic pour analyser les incohérences de calcul du panier
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def analyze_cart_calculation():
    """Analyse le calcul du panier et des personnalisations"""
    print("🔍 DIAGNOSTIC DU CALCUL DU PANIER")
    print("=" * 60)
    
    try:
        from cart.models import Cart, CartItem
        from products.models import Product, CartItemCustomization
        from django.contrib.auth.models import User
        
        # Analyser tous les paniers actifs
        carts = Cart.objects.all()
        print(f"📊 {carts.count()} panier(s) trouvé(s)")
        
        for cart in carts:
            print(f"\n🛒 Panier ID: {cart.id}")
            print(f"   - Utilisateur: {cart.user.username if cart.user else 'Anonyme'}")
            print(f"   - Session: {cart.session_key}")
            print(f"   - Articles: {cart.items.count()}")
            
            total_calculated = 0
            for item in cart.items.all():
                print(f"\n   📦 Article: {item.product.name} ({item.size})")
                print(f"      - Quantité: {item.quantity}")
                print(f"      - Prix unitaire: {item.product.current_price} FCFA")
                print(f"      - Prix de base: {item.base_price} FCFA")
                
                # Analyser les personnalisations
                customizations = item.customizations.all()
                if customizations:
                    print(f"      - Personnalisations: {customizations.count()}")
                    for cust in customizations:
                        print(f"        * {cust.customization.name}: {cust.price} FCFA")
                        if cust.custom_text:
                            print(f"          Texte: '{cust.custom_text}'")
                else:
                    print(f"      - Personnalisations: Aucune")
                
                print(f"      - Prix total: {item.total_price} FCFA")
                total_calculated += item.total_price
            
            print(f"\n   💰 Total calculé: {total_calculated} FCFA")
            
            # Vérifier s'il y a des incohérences
            if total_calculated > 0:
                # Chercher des produits à 10 000 FCFA
                products_10k = Product.objects.filter(current_price=10000)
                if products_10k.exists():
                    print(f"\n   🔍 Produits à 10 000 FCFA trouvés:")
                    for product in products_10k:
                        print(f"      - {product.name}: {product.current_price} FCFA")
                
                # Vérifier si le total est anormalement élevé
                if total_calculated > 50000:
                    print(f"\n   ⚠️ ATTENTION: Total anormalement élevé ({total_calculated} FCFA)")
                    print(f"      Cela pourrait expliquer l'incohérence observée!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        return False

def analyze_specific_product():
    """Analyse un produit spécifique (Maillot Barcelone Vintage)"""
    print("\n🔍 ANALYSE DU PRODUIT BARCELONE VINTAGE")
    print("=" * 60)
    
    try:
        from products.models import Product, JerseyCustomization, CartItemCustomization
        from cart.models import CartItem
        
        # Chercher le produit Barcelone Vintage
        products = Product.objects.filter(name__icontains='barcelone')
        if not products.exists():
            products = Product.objects.filter(name__icontains='vintage')
        
        if not products.exists():
            print("❌ Produit Barcelone Vintage non trouvé")
            return False
        
        for product in products:
            print(f"📦 Produit: {product.name}")
            print(f"   - Prix: {product.current_price} FCFA")
            print(f"   - ID: {product.id}")
            
            # Chercher les cart_items avec ce produit
            cart_items = CartItem.objects.filter(product=product)
            print(f"   - Articles dans les paniers: {cart_items.count()}")
            
            for item in cart_items:
                print(f"\n   🛒 Article dans le panier:")
                print(f"      - Taille: {item.size}")
                print(f"      - Quantité: {item.quantity}")
                print(f"      - Prix de base: {item.base_price} FCFA")
                
                # Analyser les personnalisations
                customizations = item.customizations.all()
                if customizations:
                    print(f"      - Personnalisations: {customizations.count()}")
                    total_custom_price = 0
                    for cust in customizations:
                        print(f"        * {cust.customization.name}: {cust.price} FCFA")
                        if cust.custom_text:
                            print(f"          Texte: '{cust.custom_text}' (longueur: {len(cust.custom_text)})")
                        total_custom_price += cust.price
                    
                    print(f"      - Total personnalisations: {total_custom_price} FCFA")
                    print(f"      - Prix total: {item.total_price} FCFA")
                    
                    # Vérifier si les personnalisations expliquent la différence
                    if item.total_price > 50000:
                        print(f"      ⚠️ PRIX ANORMALEMENT ÉLEVÉ!")
                        print(f"         Différence: {item.total_price - item.base_price} FCFA")
                        print(f"         Cela pourrait expliquer l'incohérence!")
                else:
                    print(f"      - Personnalisations: Aucune")
                    print(f"      - Prix total: {item.total_price} FCFA")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        return False

def check_customization_prices():
    """Vérifie les prix des personnalisations"""
    print("\n🔍 VÉRIFICATION DES PRIX DE PERSONNALISATIONS")
    print("=" * 60)
    
    try:
        from products.models import JerseyCustomization, CartItemCustomization
        
        # Analyser les types de personnalisations
        customizations = JerseyCustomization.objects.all()
        print(f"📊 {customizations.count()} type(s) de personnalisation trouvé(s)")
        
        for cust in customizations:
            print(f"\n🎨 {cust.name} ({cust.customization_type})")
            print(f"   - Prix unitaire: {cust.price} FCFA")
            
            # Analyser les personnalisations appliquées
            applied = CartItemCustomization.objects.filter(customization=cust)
            print(f"   - Appliquées: {applied.count()} fois")
            
            if applied.exists():
                total_revenue = sum(c.price for c in applied)
                print(f"   - Revenus totaux: {total_revenue} FCFA")
                
                # Analyser les prix les plus élevés
                max_price = max(c.price for c in applied)
                print(f"   - Prix maximum: {max_price} FCFA")
                
                if max_price > 10000:
                    print(f"   ⚠️ PRIX TRÈS ÉLEVÉ DÉTECTÉ!")
                    expensive = applied.filter(price=max_price).first()
                    if expensive:
                        print(f"      - Texte: '{expensive.custom_text}'")
                        print(f"      - Longueur: {len(expensive.custom_text) if expensive.custom_text else 0}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {str(e)}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🔧 DIAGNOSTIC DES INCOHÉRENCES DE CALCUL DU PANIER")
    print("=" * 60)
    
    tests = [
        ("Analyse du calcul du panier", analyze_cart_calculation),
        ("Analyse du produit Barcelone", analyze_specific_product),
        ("Vérification des prix de personnalisations", check_customization_prices),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"   {status} - {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 DIAGNOSTIC TERMINÉ!")
        print("✅ Les incohérences ont été identifiées")
    else:
        print("\n💥 CERTAINS TESTS ONT ÉCHOUÉ!")
        print("❌ Des problèmes persistent dans le diagnostic")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
