/**
 * Service Worker pour Maillots Football PWA
 * Version: 1.0.0
 */

const CACHE_NAME = 'maillots-football-v1.0.0';
const STATIC_CACHE = 'maillots-static-v1.0.0';
const DYNAMIC_CACHE = 'maillots-dynamic-v1.0.0';
const IMAGE_CACHE = 'maillots-images-v1.0.0';

// Ressources à mettre en cache lors de l'installation
const STATIC_ASSETS = [
    '/',
    '/static/css/bootstrap.min.css',
    '/static/css/custom.css',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/custom.js',
    '/static/manifest.json',
    '/offline/',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png'
];

// API endpoints à mettre en cache
const API_ENDPOINTS = [
    '/api/products/',
    '/api/categories/',
    '/api/teams/'
];

// Installation du Service Worker
self.addEventListener('install', event => {
    console.log('🔧 Service Worker: Installation en cours...');
    
    event.waitUntil(
        Promise.all([
            // Cache des ressources statiques
            caches.open(STATIC_CACHE).then(cache => {
                console.log('📦 Cache des ressources statiques...');
                return cache.addAll(STATIC_ASSETS);
            }),
            
            // Cache des endpoints API
            caches.open(DYNAMIC_CACHE).then(cache => {
                console.log('🌐 Cache des endpoints API...');
                return cache.addAll(API_ENDPOINTS);
            })
        ]).then(() => {
            console.log('✅ Service Worker: Installation terminée');
            return self.skipWaiting();
        })
    );
});

// Activation du Service Worker
self.addEventListener('activate', event => {
    console.log('🚀 Service Worker: Activation en cours...');
    
    event.waitUntil(
        Promise.all([
            // Nettoyage des anciens caches
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && 
                            cacheName !== DYNAMIC_CACHE && 
                            cacheName !== IMAGE_CACHE) {
                            console.log('🗑️ Suppression de l\'ancien cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            }),
            
            // Prise de contrôle immédiate
            self.clients.claim()
        ]).then(() => {
            console.log('✅ Service Worker: Activation terminée');
        })
    );
});

// Interception des requêtes
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Stratégies de cache selon le type de ressource
    if (request.method === 'GET') {
        if (url.pathname.startsWith('/static/') || url.pathname.endsWith('.css') || url.pathname.endsWith('.js')) {
            // Ressources statiques - Cache First
            event.respondWith(cacheFirst(request, STATIC_CACHE));
        } else if (url.pathname.startsWith('/media/') || url.pathname.match(/\.(jpg|jpeg|png|gif|webp|svg)$/)) {
            // Images - Cache First avec fallback
            event.respondWith(cacheFirst(request, IMAGE_CACHE));
        } else if (url.pathname.startsWith('/api/')) {
            // API - Network First avec fallback cache
            event.respondWith(networkFirst(request, DYNAMIC_CACHE));
        } else if (url.pathname.startsWith('/products/') || url.pathname.startsWith('/cart/')) {
            // Pages importantes - Network First
            event.respondWith(networkFirst(request, DYNAMIC_CACHE));
        } else {
            // Autres pages - Stale While Revalidate
            event.respondWith(staleWhileRevalidate(request, DYNAMIC_CACHE));
        }
    }
});

// Stratégie Cache First
async function cacheFirst(request, cacheName) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.error('Erreur Cache First:', error);
        return new Response('Ressource non disponible hors ligne', { status: 503 });
    }
}

// Stratégie Network First
async function networkFirst(request, cacheName) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        console.log('Réseau indisponible, utilisation du cache...');
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Fallback pour les pages
        if (request.destination === 'document') {
            return caches.match('/offline/');
        }
        
        return new Response('Ressource non disponible hors ligne', { status: 503 });
    }
}

// Stratégie Stale While Revalidate
async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request).then(networkResponse => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(() => {
        // En cas d'erreur réseau, retourner la version en cache
        return cachedResponse || new Response('Page non disponible hors ligne', { status: 503 });
    });
    
    return cachedResponse || fetchPromise;
}

// Gestion des notifications push
self.addEventListener('push', event => {
    console.log('📱 Notification push reçue:', event);
    
    let notificationData = {
        title: 'Maillots Football',
        body: 'Nouvelle notification',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/badge-72x72.png',
        tag: 'maillots-notification',
        requireInteraction: false,
        actions: [
            {
                action: 'view',
                title: 'Voir',
                icon: '/static/icons/view-icon.png'
            },
            {
                action: 'dismiss',
                title: 'Ignorer',
                icon: '/static/icons/dismiss-icon.png'
            }
        ]
    };
    
    if (event.data) {
        try {
            const data = event.data.json();
            notificationData = { ...notificationData, ...data };
        } catch (error) {
            console.error('Erreur parsing notification data:', error);
        }
    }
    
    event.waitUntil(
        self.registration.showNotification(notificationData.title, notificationData)
    );
});

// Gestion des clics sur les notifications
self.addEventListener('notificationclick', event => {
    console.log('🔔 Clic sur notification:', event);
    
    event.notification.close();
    
    if (event.action === 'dismiss') {
        return;
    }
    
    const urlToOpen = event.notification.data?.url || '/';
    
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
            // Chercher une fenêtre existante
            for (const client of clientList) {
                if (client.url.includes(self.location.origin) && 'focus' in client) {
                    client.navigate(urlToOpen);
                    return client.focus();
                }
            }
            
            // Ouvrir une nouvelle fenêtre
            if (clients.openWindow) {
                return clients.openWindow(urlToOpen);
            }
        })
    );
});

// Gestion de la synchronisation en arrière-plan
self.addEventListener('sync', event => {
    console.log('🔄 Synchronisation en arrière-plan:', event.tag);
    
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Fonction de synchronisation en arrière-plan
async function doBackgroundSync() {
    try {
        // Synchroniser les données du panier
        await syncCartData();
        
        // Synchroniser les préférences utilisateur
        await syncUserPreferences();
        
        console.log('✅ Synchronisation en arrière-plan terminée');
    } catch (error) {
        console.error('❌ Erreur synchronisation en arrière-plan:', error);
    }
}

// Synchronisation des données du panier
async function syncCartData() {
    // Implémentation de la synchronisation du panier
    console.log('🛒 Synchronisation du panier...');
}

// Synchronisation des préférences utilisateur
async function syncUserPreferences() {
    // Implémentation de la synchronisation des préférences
    console.log('⚙️ Synchronisation des préférences...');
}

// Gestion des messages du client
self.addEventListener('message', event => {
    console.log('💬 Message reçu du client:', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'GET_VERSION') {
        event.ports[0].postMessage({ version: CACHE_NAME });
    }
});

// Gestion des erreurs
self.addEventListener('error', event => {
    console.error('❌ Erreur Service Worker:', event.error);
});

self.addEventListener('unhandledrejection', event => {
    console.error('❌ Promise rejetée non gérée:', event.reason);
});

console.log('🎉 Service Worker chargé avec succès!');
