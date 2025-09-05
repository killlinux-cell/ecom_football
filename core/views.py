from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    """Vue d'accueil avec raccourcis PWA"""
    context = {
        'pwa_shortcuts': [
            {
                'name': 'Nouveautés',
                'url': '/products/?category=new',
                'icon': 'fas fa-star',
                'color': '#28a745'
            },
            {
                'name': 'Promotions',
                'url': '/products/?category=sale',
                'icon': 'fas fa-percentage',
                'color': '#ffc107'
            },
            {
                'name': 'Mon Panier',
                'url': '/cart/',
                'icon': 'fas fa-shopping-cart',
                'color': '#17a2b8'
            },
            {
                'name': 'Mes Commandes',
                'url': '/dashboard/my-orders/',
                'icon': 'fas fa-list',
                'color': '#6f42c1'
            }
        ]
    }
    return render(request, 'core/home.html', context)

@require_http_methods(["GET"])
def pwa_manifest(request):
    """API pour récupérer le manifest PWA"""
    manifest_data = {
        "name": "Maillots Football - Boutique Officielle",
        "short_name": "Maillots Football",
        "description": "Votre boutique de confiance pour les maillots de football",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#1e3c72",
        "orientation": "portrait-primary",
        "scope": "/",
        "lang": "fr",
        "dir": "ltr",
        "categories": ["shopping", "sports", "lifestyle"]
    }
    return JsonResponse(manifest_data)

@csrf_exempt
@require_http_methods(["POST"])
def push_subscription(request):
    """API pour gérer les abonnements aux notifications push"""
    try:
        data = json.loads(request.body)
        subscription = data.get('subscription')
        
        if subscription:
            # Ici vous pouvez sauvegarder la subscription en base de données
            # pour envoyer des notifications push plus tard
            print(f"Subscription reçue: {subscription}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Subscription enregistrée avec succès'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Données de subscription manquantes'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Données JSON invalides'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erreur serveur: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def offline_page(request):
    """Page hors ligne pour PWA"""
    return render(request, 'offline.html')

@require_http_methods(["GET"])
def service_worker(request):
    """Service Worker pour PWA"""
    response = render(request, 'sw.js', content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    return response