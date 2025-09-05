from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/review/', views.add_review, name='add_review'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('team/<slug:slug>/', views.team_detail, name='team_detail'),
    path('search/', views.search, name='search'),
]
