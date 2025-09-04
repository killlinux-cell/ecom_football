#!/usr/bin/env python
"""
Script de test pour vérifier que toutes les fonctionnalités du dashboard
remplacent correctement l'admin Django.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

from products.models import Product, Category, Team
from orders.models import Order
from payments.models import Payment

class DashboardFunctionalityTest(TestCase):
    """Test de toutes les fonctionnalités du dashboard"""
    
    def setUp(self):
        """Configuration initiale"""
        # Créer un utilisateur admin
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Créer un client de test
        self.client = Client()
        self.client.login(username='admin', password='testpass123')
        
        # Créer des données de test
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        self.team = Team.objects.create(
            name='Test Team',
            country='Test Country',
            league='Test League'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10000,
            stock_quantity=10,
            category=self.category,
            team=self.team
        )
    
    def test_dashboard_home_access(self):
        """Test d'accès au dashboard principal"""
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
    
    def test_products_management(self):
        """Test de la gestion des produits"""
        # Liste des produits
        response = self.client.get(reverse('dashboard:products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        
        # Création d'un produit
        response = self.client.get(reverse('dashboard:product_create'))
        self.assertEqual(response.status_code, 200)
        
        # Édition d'un produit
        response = self.client.get(reverse('dashboard:product_edit', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_categories_management(self):
        """Test de la gestion des catégories"""
        response = self.client.get(reverse('dashboard:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
    
    def test_teams_management(self):
        """Test de la gestion des équipes"""
        response = self.client.get(reverse('dashboard:teams'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Team')
    
    def test_users_management(self):
        """Test de la gestion des utilisateurs"""
        response = self.client.get(reverse('dashboard:users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin')
        
        # Édition d'un utilisateur
        response = self.client.get(reverse('dashboard:user_edit', args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_orders_management(self):
        """Test de la gestion des commandes"""
        response = self.client.get(reverse('dashboard:orders'))
        self.assertEqual(response.status_code, 200)
    
    def test_payments_management(self):
        """Test de la gestion des paiements"""
        response = self.client.get(reverse('dashboard:payments'))
        self.assertEqual(response.status_code, 200)
        
        # Logs des paiements
        response = self.client.get(reverse('dashboard:payment_logs'))
        self.assertEqual(response.status_code, 200)
    
    def test_customizations_management(self):
        """Test de la gestion des personnalisations"""
        response = self.client.get(reverse('dashboard:customizations'))
        self.assertEqual(response.status_code, 200)
    
    def test_analytics_access(self):
        """Test d'accès aux analyses"""
        response = self.client.get(reverse('dashboard:analytics'))
        self.assertEqual(response.status_code, 200)
    
    def test_settings_access(self):
        """Test d'accès aux paramètres"""
        response = self.client.get(reverse('dashboard:settings'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_redirect(self):
        """Test de redirection de l'admin vers le dashboard"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')
    
    def test_unauthorized_access(self):
        """Test d'accès non autorisé"""
        # Créer un utilisateur non-admin
        regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='testpass123'
        )
        
        # Se connecter avec l'utilisateur régulier
        self.client.login(username='regular', password='testpass123')
        
        # Essayer d'accéder au dashboard
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login

def run_tests():
    """Exécuter tous les tests"""
    print("🧪 Test des fonctionnalités du dashboard...")
    print("=" * 50)
    
    # Créer une instance de test
    test_instance = DashboardFunctionalityTest()
    test_instance.setUp()
    
    tests = [
        ("Accès au dashboard principal", test_instance.test_dashboard_home_access),
        ("Gestion des produits", test_instance.test_products_management),
        ("Gestion des catégories", test_instance.test_categories_management),
        ("Gestion des équipes", test_instance.test_teams_management),
        ("Gestion des utilisateurs", test_instance.test_users_management),
        ("Gestion des commandes", test_instance.test_orders_management),
        ("Gestion des paiements", test_instance.test_payments_management),
        ("Gestion des personnalisations", test_instance.test_customizations_management),
        ("Accès aux analyses", test_instance.test_analytics_access),
        ("Accès aux paramètres", test_instance.test_settings_access),
        ("Redirection admin", test_instance.test_admin_redirect),
        ("Accès non autorisé", test_instance.test_unauthorized_access),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✅ {test_name}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_name}: {str(e)}")
            failed += 1
    
    print("=" * 50)
    print(f"📊 Résultats: {passed} réussis, {failed} échoués")
    
    if failed == 0:
        print("🎉 Tous les tests sont passés ! Le dashboard est prêt.")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return failed == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
