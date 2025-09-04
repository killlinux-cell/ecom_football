#!/usr/bin/env python3
"""
Script de test pour vérifier la responsivité mobile du site e-commerce
"""

import os
import sys
import django
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

class MobileResponsiveTest(TestCase):
    """Tests pour vérifier la responsivité mobile"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = Client()
        
    def test_mobile_css_loaded(self):
        """Vérifier que le CSS mobile est chargé"""
        response = self.client.get(reverse('products:home'))
        self.assertContains(response, 'mobile.css')
        print("✅ CSS mobile chargé correctement")
        
    def test_mobile_navigation(self):
        """Vérifier la navigation mobile"""
        response = self.client.get(reverse('products:home'))
        
        # Vérifier la présence du bouton hamburger
        self.assertContains(response, 'navbar-toggler')
        print("✅ Navigation mobile présente")
        
        # Vérifier les fonctionnalités JavaScript
        self.assertContains(response, 'initMobileFeatures')
        print("✅ Fonctionnalités JavaScript mobiles présentes")
        
    def test_product_list_mobile(self):
        """Vérifier la liste des produits sur mobile"""
        response = self.client.get(reverse('products:product_list'))
        
        # Vérifier les classes responsive
        self.assertContains(response, 'col-lg-4 col-md-6 col-sm-6 col-12')
        print("✅ Grille responsive des produits configurée")
        
        # Vérifier le bouton filtres mobile
        self.assertContains(response, 'd-lg-none')
        print("✅ Bouton filtres mobile présent")
        
    def test_cart_mobile(self):
        """Vérifier le panier sur mobile"""
        response = self.client.get(reverse('cart:cart_detail'))
        
        # Vérifier que la page du panier se charge
        self.assertEqual(response.status_code, 200)
        print("✅ Page panier accessible")
        
        # Vérifier la structure de base du panier
        self.assertContains(response, 'Mon Panier')
        print("✅ Structure panier mobile présente")
        
        # Vérifier les classes CSS (même si panier vide)
        if 'cart-item' in response.content.decode():
            print("✅ Classes CSS du panier mobile présentes")
        else:
            print("ℹ️  Panier vide - classes CSS seront présentes avec des articles")
        
    def test_mobile_viewport_meta(self):
        """Vérifier la balise viewport pour mobile"""
        response = self.client.get(reverse('products:home'))
        self.assertContains(response, 'width=device-width, initial-scale=1.0')
        print("✅ Balise viewport mobile configurée")
        
    def test_bootstrap_responsive(self):
        """Vérifier que Bootstrap est chargé"""
        response = self.client.get(reverse('products:home'))
        self.assertContains(response, 'bootstrap@5.3.0')
        print("✅ Bootstrap 5 chargé pour la responsivité")

def run_mobile_tests():
    """Exécuter tous les tests mobiles"""
    print("🧪 Test de la responsivité mobile du site e-commerce")
    print("=" * 50)
    
    try:
        # Créer une instance de test
        test_instance = MobileResponsiveTest()
        test_instance.setUp()
        
        # Exécuter les tests
        test_instance.test_mobile_css_loaded()
        test_instance.test_mobile_navigation()
        test_instance.test_product_list_mobile()
        test_instance.test_cart_mobile()
        test_instance.test_mobile_viewport_meta()
        test_instance.test_bootstrap_responsive()
        
        print("\n" + "=" * 50)
        print("✅ Tous les tests mobiles sont passés avec succès !")
        print("📱 Votre site est maintenant optimisé pour mobile")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests : {e}")
        return False

if __name__ == "__main__":
    success = run_mobile_tests()
    sys.exit(0 if success else 1)
