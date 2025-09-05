# URLs pour l'application core
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='core_home'),
    path('manifest.json', views.pwa_manifest, name='pwa_manifest'),
    path('api/push-subscription/', views.push_subscription, name='push_subscription'),
    path('offline/', views.offline_page, name='offline_page'),
    path('sw.js', views.service_worker, name='service_worker'),
]
