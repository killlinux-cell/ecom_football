/**
 * PWA JavaScript pour Maillots Football
 * Gestion de l'installation, notifications et fonctionnalités PWA
 */

class PWAManager {
    constructor() {
        this.deferredPrompt = null;
        this.isInstalled = false;
        this.isOnline = navigator.onLine;
        
        this.init();
    }
    
    init() {
        this.registerServiceWorker();
        this.setupInstallPrompt();
        this.setupNotifications();
        this.setupOfflineDetection();
        this.setupUpdateDetection();
    }
    
    // Enregistrement du Service Worker
    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/sw.js');
                console.log('✅ Service Worker enregistré:', registration);
                
                // Écouter les mises à jour
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            this.showUpdateNotification();
                        }
                    });
                });
                
            } catch (error) {
                console.error('❌ Erreur Service Worker:', error);
            }
        }
    }
    
    // Gestion du prompt d'installation
    setupInstallPrompt() {
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });
        
        window.addEventListener('appinstalled', () => {
            this.isInstalled = true;
            this.hideInstallButton();
            this.showInstallSuccessMessage();
        });
    }
    
    // Afficher le bouton d'installation
    showInstallButton() {
        if (this.isInstalled) return;
        
        const installButton = this.createInstallButton();
        document.body.appendChild(installButton);
        
        // Auto-hide après 10 secondes
        setTimeout(() => {
            if (installButton.parentNode) {
                installButton.remove();
            }
        }, 10000);
    }
    
    // Créer le bouton d'installation
    createInstallButton() {
        const button = document.createElement('div');
        button.id = 'pwa-install-banner';
        button.innerHTML = `
            <div class="pwa-install-banner">
                <div class="pwa-install-content">
                    <div class="pwa-install-icon">
                        <i class="fas fa-download"></i>
                    </div>
                    <div class="pwa-install-text">
                        <strong>Installer l'app</strong>
                        <small>Accès rapide depuis votre écran d'accueil</small>
                    </div>
                    <div class="pwa-install-actions">
                        <button class="pwa-install-btn" onclick="pwaManager.installApp()">
                            Installer
                        </button>
                        <button class="pwa-dismiss-btn" onclick="pwaManager.dismissInstall()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Ajouter les styles
        const style = document.createElement('style');
        style.textContent = `
            .pwa-install-banner {
                position: fixed;
                bottom: 20px;
                left: 20px;
                right: 20px;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                border-radius: 15px;
                padding: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                z-index: 1000;
                animation: slideUp 0.3s ease-out;
            }
            
            @keyframes slideUp {
                from { transform: translateY(100px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            .pwa-install-content {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .pwa-install-icon {
                font-size: 2rem;
                color: #ffc107;
            }
            
            .pwa-install-text {
                flex: 1;
            }
            
            .pwa-install-text strong {
                display: block;
                font-size: 1.1rem;
            }
            
            .pwa-install-text small {
                opacity: 0.9;
                font-size: 0.9rem;
            }
            
            .pwa-install-actions {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .pwa-install-btn {
                background: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .pwa-install-btn:hover {
                background: #218838;
                transform: translateY(-2px);
            }
            
            .pwa-dismiss-btn {
                background: transparent;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .pwa-dismiss-btn:hover {
                background: rgba(255,255,255,0.2);
            }
            
            @media (max-width: 768px) {
                .pwa-install-banner {
                    left: 10px;
                    right: 10px;
                    bottom: 10px;
                }
                
                .pwa-install-content {
                    flex-direction: column;
                    text-align: center;
                    gap: 10px;
                }
                
                .pwa-install-actions {
                    width: 100%;
                    justify-content: center;
                }
            }
        `;
        document.head.appendChild(style);
        
        return button;
    }
    
    // Installer l'app
    async installApp() {
        if (!this.deferredPrompt) return;
        
        this.deferredPrompt.prompt();
        const { outcome } = await this.deferredPrompt.userChoice;
        
        if (outcome === 'accepted') {
            console.log('✅ App installée par l\'utilisateur');
        } else {
            console.log('❌ Installation refusée par l\'utilisateur');
        }
        
        this.deferredPrompt = null;
        this.hideInstallButton();
    }
    
    // Masquer le bouton d'installation
    hideInstallButton() {
        const banner = document.getElementById('pwa-install-banner');
        if (banner) {
            banner.remove();
        }
    }
    
    // Ignorer l'installation
    dismissInstall() {
        this.hideInstallButton();
        // Stocker la préférence
        localStorage.setItem('pwa-install-dismissed', 'true');
    }
    
    // Message de succès d'installation
    showInstallSuccessMessage() {
        this.showNotification('🎉 App installée !', 'Vous pouvez maintenant accéder à Maillots Football depuis votre écran d\'accueil.');
    }
    
    // Gestion des notifications
    async setupNotifications() {
        if ('Notification' in window) {
            const permission = await this.requestNotificationPermission();
            
            if (permission === 'granted') {
                this.setupPushNotifications();
            }
        }
    }
    
    // Demander la permission de notification
    async requestNotificationPermission() {
        if (Notification.permission === 'default') {
            return await Notification.requestPermission();
        }
        return Notification.permission;
    }
    
    // Configurer les notifications push
    setupPushNotifications() {
        if ('serviceWorker' in navigator && 'PushManager' in window) {
            navigator.serviceWorker.ready.then(registration => {
                // S'abonner aux notifications push
                this.subscribeToPush(registration);
            });
        }
    }
    
    // S'abonner aux notifications push
    async subscribeToPush(registration) {
        try {
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: this.urlBase64ToUint8Array('YOUR_VAPID_PUBLIC_KEY')
            });
            
            // Envoyer la subscription au serveur
            await this.sendSubscriptionToServer(subscription);
            
        } catch (error) {
            console.error('Erreur abonnement push:', error);
        }
    }
    
    // Envoyer la subscription au serveur
    async sendSubscriptionToServer(subscription) {
        try {
            const response = await fetch('/api/push-subscription/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(subscription)
            });
            
            if (response.ok) {
                console.log('✅ Subscription envoyée au serveur');
            }
        } catch (error) {
            console.error('Erreur envoi subscription:', error);
        }
    }
    
    // Détection hors ligne
    setupOfflineDetection() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showNotification('🌐 En ligne', 'Votre connexion est rétablie !');
            this.hideOfflineIndicator();
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showNotification('📴 Hors ligne', 'Vous êtes maintenant hors ligne. Certaines fonctionnalités peuvent être limitées.');
            this.showOfflineIndicator();
        });
    }
    
    // Afficher l'indicateur hors ligne
    showOfflineIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'offline-indicator';
        indicator.innerHTML = `
            <div class="offline-indicator">
                <i class="fas fa-wifi-slash"></i>
                <span>Hors ligne</span>
            </div>
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            .offline-indicator {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #dc3545;
                color: white;
                padding: 10px 15px;
                border-radius: 25px;
                font-weight: 600;
                z-index: 1000;
                animation: slideDown 0.3s ease-out;
            }
            
            @keyframes slideDown {
                from { transform: translateY(-100px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            .offline-indicator i {
                margin-right: 8px;
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(indicator);
    }
    
    // Masquer l'indicateur hors ligne
    hideOfflineIndicator() {
        const indicator = document.getElementById('offline-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    // Détection des mises à jour
    setupUpdateDetection() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.addEventListener('controllerchange', () => {
                this.showUpdateNotification();
            });
        }
    }
    
    // Afficher la notification de mise à jour
    showUpdateNotification() {
        this.showNotification('🔄 Mise à jour disponible', 'Une nouvelle version de l\'app est disponible. Rechargez la page pour l\'utiliser.');
    }
    
    // Afficher une notification
    showNotification(title, body) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: body,
                icon: '/static/icons/icon-192x192.png',
                badge: '/static/icons/badge-72x72.png',
                tag: 'maillots-notification'
            });
        } else {
            // Fallback avec toast
            this.showToast(title, body);
        }
    }
    
    // Afficher un toast
    showToast(title, message) {
        const toast = document.createElement('div');
        toast.className = 'pwa-toast';
        toast.innerHTML = `
            <div class="pwa-toast-content">
                <strong>${title}</strong>
                <p>${message}</p>
            </div>
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            .pwa-toast {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: #333;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                z-index: 1000;
                animation: toastSlide 0.3s ease-out;
                max-width: 400px;
            }
            
            @keyframes toastSlide {
                from { transform: translateX(-50%) translateY(-100px); opacity: 0; }
                to { transform: translateX(-50%) translateY(0); opacity: 1; }
            }
            
            .pwa-toast-content strong {
                display: block;
                margin-bottom: 5px;
            }
            
            .pwa-toast-content p {
                margin: 0;
                font-size: 0.9rem;
                opacity: 0.9;
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(toast);
        
        // Auto-remove après 5 secondes
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }
    
    // Utilitaires
    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');
        
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
}

// Initialiser le PWA Manager
const pwaManager = new PWAManager();

// Exposer globalement pour les boutons
window.pwaManager = pwaManager;
