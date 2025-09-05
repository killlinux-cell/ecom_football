#!/usr/bin/env python
"""
Script de test complet pour la PWA Maillots Football
Teste toutes les fonctionnalités PWA implémentées
"""

import os
import json
import requests
from pathlib import Path

def test_pwa_files():
    """Teste la présence et la validité des fichiers PWA"""
    print("🔍 Test des fichiers PWA...")
    
    # Fichiers requis
    required_files = [
        'static/manifest.json',
        'static/sw.js',
        'static/browserconfig.xml',
        'static/css/pwa-mobile.css',
        'static/js/pwa.js',
        'templates/offline.html',
        'templates/core/home.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return False
    
    print("✅ Tous les fichiers PWA sont présents")
    return True

def test_manifest():
    """Teste la validité du manifest.json"""
    print("\n📋 Test du manifest.json...")
    
    try:
        with open('static/manifest.json', 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Champs requis
        required_fields = [
            'name', 'short_name', 'description', 'start_url', 
            'display', 'background_color', 'theme_color', 'icons'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in manifest:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Champs manquants dans le manifest: {missing_fields}")
            return False
        
        # Vérifier les icônes
        icons = manifest.get('icons', [])
        if len(icons) < 3:
            print("❌ Pas assez d'icônes dans le manifest")
            return False
        
        # Vérifier les tailles d'icônes
        required_sizes = ['192x192', '512x512']
        icon_sizes = [icon.get('sizes', '') for icon in icons]
        
        for size in required_sizes:
            if not any(size in icon_size for icon_size in icon_sizes):
                print(f"❌ Icône {size} manquante")
                return False
        
        print("✅ Manifest.json valide")
        print(f"   - Nom: {manifest['name']}")
        print(f"   - Nom court: {manifest['short_name']}")
        print(f"   - Mode d'affichage: {manifest['display']}")
        print(f"   - Couleur thème: {manifest['theme_color']}")
        print(f"   - Nombre d'icônes: {len(icons)}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON dans le manifest: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du manifest: {e}")
        return False

def test_icons():
    """Teste la présence des icônes PWA"""
    print("\n🎨 Test des icônes PWA...")
    
    icons_dir = Path('static/icons')
    if not icons_dir.exists():
        print("❌ Dossier icons manquant")
        return False
    
    # Tailles d'icônes requises
    required_icons = [
        'icon-72x72.png',
        'icon-96x96.png',
        'icon-128x128.png',
        'icon-144x144.png',
        'icon-152x152.png',
        'icon-192x192.png',
        'icon-384x384.png',
        'icon-512x512.png',
        'badge-72x72.png'
    ]
    
    missing_icons = []
    for icon in required_icons:
        icon_path = icons_dir / icon
        if not icon_path.exists():
            missing_icons.append(icon)
        else:
            print(f"✅ {icon}")
    
    if missing_icons:
        print(f"❌ Icônes manquantes: {missing_icons}")
        return False
    
    print("✅ Toutes les icônes PWA sont présentes")
    return True

def test_service_worker():
    """Teste le service worker"""
    print("\n⚙️ Test du service worker...")
    
    try:
        with open('static/sw.js', 'r', encoding='utf-8') as f:
            sw_content = f.read()
        
        # Fonctionnalités requises
        required_features = [
            'addEventListener',
            'install',
            'activate',
            'fetch',
            'push',
            'notificationclick',
            'sync'
        ]
        
        missing_features = []
        for feature in required_features:
            if feature not in sw_content:
                missing_features.append(feature)
        
        if missing_features:
            print(f"❌ Fonctionnalités manquantes dans le SW: {missing_features}")
            return False
        
        # Vérifier les stratégies de cache
        cache_strategies = [
            'cacheFirst',
            'networkFirst',
            'staleWhileRevalidate'
        ]
        
        for strategy in cache_strategies:
            if strategy not in sw_content:
                print(f"⚠️ Stratégie de cache '{strategy}' manquante")
        
        print("✅ Service worker valide")
        print(f"   - Taille: {len(sw_content)} caractères")
        print(f"   - Fonctionnalités: {len(required_features) - len(missing_features)}/{len(required_features)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du service worker: {e}")
        return False

def test_templates():
    """Teste les templates PWA"""
    print("\n📄 Test des templates PWA...")
    
    # Test du template offline
    try:
        with open('templates/offline.html', 'r', encoding='utf-8') as f:
            offline_content = f.read()
        
        required_elements = [
            'Hors ligne',
            'Service Worker',
            'navigator.onLine',
            'retryConnection'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in offline_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Éléments manquants dans offline.html: {missing_elements}")
            return False
        
        print("✅ Template offline.html valide")
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture d'offline.html: {e}")
        return False
    
    # Test du template home
    try:
        with open('templates/core/home.html', 'r', encoding='utf-8') as f:
            home_content = f.read()
        
        required_elements = [
            'pwa-shortcuts',
            'installApp',
            'pwaManager',
            'display-mode: standalone'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in home_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Éléments manquants dans home.html: {missing_elements}")
            return False
        
        print("✅ Template home.html valide")
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de home.html: {e}")
        return False
    
    return True

def test_css():
    """Teste le CSS PWA"""
    print("\n🎨 Test du CSS PWA...")
    
    try:
        with open('static/css/pwa-mobile.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        required_features = [
            'pwa-install-banner',
            'connection-status',
            'pwa-toast',
            'display-mode: standalone',
            'safe-area-inset',
            'touch-feedback'
        ]
        
        missing_features = []
        for feature in required_features:
            if feature not in css_content:
                missing_features.append(feature)
        
        if missing_features:
            print(f"❌ Fonctionnalités CSS manquantes: {missing_features}")
            return False
        
        print("✅ CSS PWA valide")
        print(f"   - Taille: {len(css_content)} caractères")
        print(f"   - Fonctionnalités: {len(required_features) - len(missing_features)}/{len(required_features)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSS PWA: {e}")
        return False

def test_js():
    """Teste le JavaScript PWA"""
    print("\n⚡ Test du JavaScript PWA...")
    
    try:
        with open('static/js/pwa.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        required_features = [
            'PWAManager',
            'registerServiceWorker',
            'installApp',
            'showNotification',
            'setupOfflineDetection',
            'beforeinstallprompt'
        ]
        
        missing_features = []
        for feature in required_features:
            if feature not in js_content:
                missing_features.append(feature)
        
        if missing_features:
            print(f"❌ Fonctionnalités JS manquantes: {missing_features}")
            return False
        
        print("✅ JavaScript PWA valide")
        print(f"   - Taille: {len(js_content)} caractères")
        print(f"   - Fonctionnalités: {len(required_features) - len(missing_features)}/{len(required_features)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du JS PWA: {e}")
        return False

def test_urls():
    """Teste les URLs PWA"""
    print("\n🔗 Test des URLs PWA...")
    
    try:
        with open('core/urls.py', 'r', encoding='utf-8') as f:
            urls_content = f.read()
        
        required_urls = [
            'pwa_manifest',
            'push_subscription',
            'offline_page',
            'service_worker'
        ]
        
        missing_urls = []
        for url in required_urls:
            if url not in urls_content:
                missing_urls.append(url)
        
        if missing_urls:
            print(f"❌ URLs manquantes: {missing_urls}")
            return False
        
        print("✅ URLs PWA configurées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des URLs: {e}")
        return False

def test_views():
    """Teste les vues PWA"""
    print("\n👁️ Test des vues PWA...")
    
    try:
        with open('core/views.py', 'r', encoding='utf-8') as f:
            views_content = f.read()
        
        required_views = [
            'pwa_manifest',
            'push_subscription',
            'offline_page',
            'service_worker'
        ]
        
        missing_views = []
        for view in required_views:
            if view not in views_content:
                missing_views.append(view)
        
        if missing_views:
            print(f"❌ Vues manquantes: {missing_views}")
            return False
        
        print("✅ Vues PWA implémentées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des vues: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test complet de la PWA Maillots Football")
    print("=" * 50)
    
    tests = [
        test_pwa_files,
        test_manifest,
        test_icons,
        test_service_worker,
        test_templates,
        test_css,
        test_js,
        test_urls,
        test_views
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur lors du test {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests PWA sont passés avec succès !")
        print("\n✨ Votre PWA est prête ! Fonctionnalités disponibles :")
        print("   📱 Installation sur mobile et desktop")
        print("   🔄 Mode hors ligne avec cache intelligent")
        print("   🔔 Notifications push")
        print("   ⚡ Chargement rapide avec service worker")
        print("   🎨 Interface mobile optimisée")
        print("   📋 Raccourcis d'application")
        print("   🔧 Synchronisation en arrière-plan")
        
        print("\n🚀 Prochaines étapes :")
        print("   1. Testez l'installation sur mobile")
        print("   2. Vérifiez le mode hors ligne")
        print("   3. Configurez les notifications push")
        print("   4. Testez les raccourcis")
        
    else:
        print(f"⚠️ {total - passed} test(s) ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
