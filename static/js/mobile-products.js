/**
 * Optimisation de l'affichage des produits sur mobile
 */

class MobileProductsOptimizer {
    constructor() {
        this.isListView = false;
        this.isScrolling = false;
        this.scrollTimeout = null;
        this.init();
    }

    init() {
        if (window.innerWidth <= 768) {
            this.createViewToggle();
            this.createBackToTopButton();
            this.createScrollIndicator();
            this.optimizeImages();
            this.setupInfiniteScroll();
            this.setupMobileFilters();
            this.setupSearch();
            this.restorePreferences();
        }
    }

    // Créer le bouton de basculement de vue
    createViewToggle() {
        const toggleButton = document.createElement('button');
        toggleButton.className = 'view-toggle';
        toggleButton.innerHTML = '<i class="fas fa-th"></i>';
        toggleButton.title = 'Basculer entre grille et liste';
        toggleButton.addEventListener('click', () => this.toggleView());
        
        document.body.appendChild(toggleButton);
    }

    // Basculer entre vue grille et liste
    toggleView() {
        const container = document.querySelector('.container .row');
        const toggleButton = document.querySelector('.view-toggle');
        
        if (!container) return;

        this.isListView = !this.isListView;
        
        if (this.isListView) {
            container.classList.add('list-view');
            toggleButton.innerHTML = '<i class="fas fa-th-large"></i>';
            toggleButton.title = 'Vue grille';
        } else {
            container.classList.remove('list-view');
            toggleButton.innerHTML = '<i class="fas fa-th"></i>';
            toggleButton.title = 'Vue liste';
        }

        // Sauvegarder la préférence
        localStorage.setItem('mobile-view-preference', this.isListView ? 'list' : 'grid');
        
        // Forcer le reflow pour s'assurer que les styles sont appliqués
        container.offsetHeight;
    }

    // Créer le bouton retour en haut
    createBackToTopButton() {
        const backToTop = document.createElement('button');
        backToTop.className = 'back-to-top';
        backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
        backToTop.title = 'Retour en haut';
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        document.body.appendChild(backToTop);

        // Afficher/masquer selon le scroll
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });
    }

    // Créer l'indicateur de position
    createScrollIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'scroll-indicator';
        document.body.appendChild(indicator);

        let scrollTimeout;
        window.addEventListener('scroll', () => {
            indicator.classList.add('show');
            
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                indicator.classList.remove('show');
            }, 1000);

            // Calculer la position
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercent = Math.round((scrollTop / docHeight) * 100);
            
            indicator.textContent = `${scrollPercent}%`;
        });
    }

    // Optimiser le chargement des images
    optimizeImages() {
        const images = document.querySelectorAll('.product-card img');
        
        // Lazy loading natif si supporté
        if ('loading' in HTMLImageElement.prototype) {
            images.forEach(img => {
                img.loading = 'lazy';
            });
        } else {
            // Fallback pour les navigateurs plus anciens
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => {
                img.classList.add('lazy');
                imageObserver.observe(img);
            });
        }
    }

    // Configuration du scroll infini
    setupInfiniteScroll() {
        const pagination = document.querySelector('.pagination');
        if (!pagination) return;

        let loading = false;
        const nextPageLink = pagination.querySelector('.page-item:last-child .page-link');
        
        if (!nextPageLink) return;

        window.addEventListener('scroll', () => {
            if (loading) return;

            const scrollTop = window.scrollY;
            const windowHeight = window.innerHeight;
            const docHeight = document.documentElement.scrollHeight;

            // Charger la page suivante quand on arrive à 80% de la page
            if (scrollTop + windowHeight >= docHeight * 0.8) {
                this.loadNextPage(nextPageLink.href);
            }
        });
    }

    // Charger la page suivante
    async loadNextPage(url) {
        if (this.isLoading) return;
        
        this.isLoading = true;
        
        try {
            const response = await fetch(url);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Extraire les nouveaux produits
            const newProducts = doc.querySelectorAll('.product-card');
            const container = document.querySelector('.row');
            
            newProducts.forEach(product => {
                container.appendChild(product);
            });

            // Mettre à jour la pagination
            const newPagination = doc.querySelector('.pagination');
            if (newPagination) {
                const currentPagination = document.querySelector('.pagination');
                currentPagination.innerHTML = newPagination.innerHTML;
            }

        } catch (error) {
            console.error('Erreur lors du chargement:', error);
        } finally {
            this.isLoading = false;
        }
    }

    // Configuration des filtres mobiles
    setupMobileFilters() {
        const filtersButton = document.querySelector('[data-bs-toggle="collapse"][data-bs-target="#filters-body"]');
        if (!filtersButton) return;

        // Créer les filtres mobiles rapides
        const quickFilters = document.createElement('div');
        quickFilters.className = 'mobile-filters';
        quickFilters.innerHTML = `
            <div class="d-flex flex-wrap justify-content-center">
                <button class="btn btn-outline-primary btn-sm" data-filter="on_sale">
                    <i class="fas fa-tag me-1"></i>Promotions
                </button>
                <button class="btn btn-outline-primary btn-sm" data-filter="in_stock">
                    <i class="fas fa-check me-1"></i>En stock
                </button>
                <button class="btn btn-outline-primary btn-sm" data-filter="new">
                    <i class="fas fa-star me-1"></i>Nouveautés
                </button>
                <button class="btn btn-outline-secondary btn-sm" data-filter="clear">
                    <i class="fas fa-times me-1"></i>Effacer
                </button>
            </div>
        `;

        document.body.appendChild(quickFilters);

        // Gérer les clics sur les filtres rapides
        quickFilters.addEventListener('click', (e) => {
            if (e.target.matches('[data-filter]')) {
                const filter = e.target.dataset.filter;
                this.applyQuickFilter(filter);
            }
        });

        // Afficher/masquer les filtres mobiles
        let filtersVisible = false;
        const toggleFilters = () => {
            filtersVisible = !filtersVisible;
            quickFilters.classList.toggle('show', filtersVisible);
        };

        filtersButton.addEventListener('click', toggleFilters);
    }

    // Appliquer un filtre rapide
    applyQuickFilter(filter) {
        const url = new URL(window.location);
        
        switch (filter) {
            case 'on_sale':
                url.searchParams.set('on_sale', 'true');
                break;
            case 'in_stock':
                url.searchParams.set('in_stock', 'true');
                break;
            case 'new':
                url.searchParams.set('sort', 'newest');
                break;
            case 'clear':
                url.search = '';
                break;
        }

        window.location.href = url.toString();
    }

    // Configuration de la recherche mobile
    setupSearch() {
        // Améliorer la recherche existante dans la navbar
        const existingSearchForm = document.querySelector('.navbar form[method="GET"]');
        if (existingSearchForm) {
            const searchInput = existingSearchForm.querySelector('input[name="q"]');
            const searchButton = existingSearchForm.querySelector('button[type="submit"]');
            
            if (searchInput && searchButton) {
                // Améliorer l'input de recherche
                searchInput.style.fontSize = '16px'; // Empêcher le zoom sur iOS
                searchInput.style.padding = '0.75rem';
                
                // Ajouter un placeholder plus descriptif
                if (!searchInput.placeholder) {
                    searchInput.placeholder = 'Rechercher un produit...';
                }
                
                // Améliorer le bouton
                searchButton.style.minHeight = '44px';
                searchButton.style.minWidth = '44px';
                
                // Ajouter la fonctionnalité de recherche instantanée
                let searchTimeout;
                searchInput.addEventListener('input', (e) => {
                    clearTimeout(searchTimeout);
                    const query = e.target.value.trim();
                    
                    if (query.length >= 2) {
                        searchTimeout = setTimeout(() => {
                            this.showSearchSuggestions(query);
                        }, 300);
                    } else {
                        this.hideSearchSuggestions();
                    }
                });
                
                // Gérer la soumission
                existingSearchForm.addEventListener('submit', (e) => {
                    const query = searchInput.value.trim();
                    if (!query) {
                        e.preventDefault();
                        searchInput.focus();
                    }
                });
            }
        }
        
        // Créer une barre de recherche mobile alternative si nécessaire
        this.createMobileSearchBar();
    }
    
    // Créer une barre de recherche mobile alternative
    createMobileSearchBar() {
        // Vérifier si on est sur une page de produits
        const isProductPage = window.location.pathname.includes('/products/') || 
                             window.location.pathname.includes('/search/');
        
        if (!isProductPage) return;
        
        // Créer la barre de recherche mobile
        const mobileSearch = document.createElement('div');
        mobileSearch.className = 'mobile-search';
        mobileSearch.innerHTML = `
            <div class="input-group">
                <input type="text" class="form-control" placeholder="Rechercher un produit..." id="mobile-search">
                <button class="btn btn-primary" type="button" id="mobile-search-btn">
                    <i class="fas fa-search"></i>
                </button>
            </div>
        `;

        // Insérer après la navbar
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.parentNode.insertBefore(mobileSearch, navbar.nextSibling);
        }

        // Gérer la recherche
        const searchBtn = mobileSearch.querySelector('#mobile-search-btn');
        const searchInputMobile = mobileSearch.querySelector('#mobile-search');

        const performSearch = () => {
            const query = searchInputMobile.value.trim();
            if (query) {
                // Rediriger vers la page de recherche
                window.location.href = `/search/?q=${encodeURIComponent(query)}`;
            }
        };

        searchBtn.addEventListener('click', performSearch);
        searchInputMobile.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    // Afficher des suggestions de recherche
    showSearchSuggestions(query) {
        // Cette fonction pourrait être étendue pour afficher des suggestions
        // Pour l'instant, on se contente de la recherche normale
        console.log('Recherche suggérée:', query);
    }
    
    // Masquer les suggestions de recherche
    hideSearchSuggestions() {
        // Masquer les suggestions si elles existent
        const suggestions = document.querySelector('.search-suggestions');
        if (suggestions) {
            suggestions.remove();
        }
    }

    // Restaurer les préférences utilisateur
    restorePreferences() {
        const savedView = localStorage.getItem('mobile-view-preference');
        if (savedView === 'list') {
            this.toggleView();
        }
    }
}

// Initialiser quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
    if (window.innerWidth <= 768) {
        new MobileProductsOptimizer();
    }
});

// Réinitialiser lors du redimensionnement
window.addEventListener('resize', () => {
    if (window.innerWidth <= 768 && !document.querySelector('.view-toggle')) {
        new MobileProductsOptimizer();
    } else if (window.innerWidth > 768) {
        // Nettoyer les éléments mobiles
        const mobileElements = document.querySelectorAll('.view-toggle, .back-to-top, .scroll-indicator, .mobile-filters, .mobile-search');
        mobileElements.forEach(el => el.remove());
    }
});
