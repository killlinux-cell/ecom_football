from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_home, name='home'),
    
    # Gestion des produits
    path('products/', views.dashboard_products, name='products'),
    path('products/create/', views.dashboard_product_create, name='product_create'),
    path('products/<int:product_id>/edit/', views.dashboard_product_edit, name='product_edit'),
    
    # Gestion des catégories
    path('categories/', views.dashboard_categories, name='categories'),
    
    # Gestion des équipes
    path('teams/', views.dashboard_teams, name='teams'),
    
    # Gestion des utilisateurs
    path('users/', views.dashboard_users, name='users'),
    path('users/<int:user_id>/edit/', views.dashboard_user_edit, name='user_edit'),
    
    # Gestion des commandes
    path('orders/', views.dashboard_orders, name='orders'),
    path('orders/<int:order_id>/', views.dashboard_order_detail, name='order_detail'),
    path('orders/<int:order_id>/invoice/', views.dashboard_order_invoice, name='order_invoice'),
    
    # Gestion des paiements
    path('payments/', views.dashboard_payments, name='payments'),
    path('payments/logs/', views.dashboard_payment_logs, name='payment_logs'),
    
    # Gestion des personnalisations
    path('customizations/', views.dashboard_customizations, name='customizations'),
    
    # Analyses et rapports
    path('analytics/', views.dashboard_analytics, name='analytics'),
    
    # Paramètres
    path('settings/', views.dashboard_settings, name='settings'),
    
    # API pour les notifications
    path('api/notifications/', views.dashboard_notifications_api, name='notifications_api'),
    
    # Vues pour les utilisateurs (leurs commandes et factures)
    path('my-orders/', views.user_orders, name='user_orders'),
    path('my-orders/<int:order_id>/', views.user_order_detail, name='user_order_detail'),
    path('my-orders/<int:order_id>/invoice/', views.user_order_invoice, name='user_order_invoice'),
]
