from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django_filters import rest_framework as filters
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Team, Review
from .filters import ProductFilter


def home(request):
    """Page d'accueil avec produits vedettes et promotions"""
    featured_products = Product.objects.filter(
        is_featured=True, 
        is_active=True
    ).prefetch_related('images', 'team', 'category')[:8]
    
    sale_products = Product.objects.filter(
        sale_price__isnull=False,
        is_active=True
    ).prefetch_related('images', 'team', 'category')[:8]
    
    latest_products = Product.objects.filter(
        is_active=True
    ).prefetch_related('images', 'team', 'category')[:12]
    
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'sale_products': sale_products,
        'latest_products': latest_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    """Liste des produits avec filtres"""
    products = Product.objects.filter(is_active=True).prefetch_related('images', 'team', 'category')
    
    # Appliquer les filtres
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    # Obtenir les filtres disponibles
    categories = Category.objects.all()
    teams = Team.objects.all()
    
    context = {
        'products': products,
        'filter': product_filter,
        'categories': categories,
        'teams': teams,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Détail d'un produit"""
    product = get_object_or_404(
        Product.objects.prefetch_related('images', 'team', 'category', 'reviews__user'),
        slug=slug, 
        is_active=True
    )
    
    # Produits similaires
    similar_products = Product.objects.filter(
        Q(category=product.category) | Q(team=product.team),
        is_active=True
    ).exclude(id=product.id).prefetch_related('images')[:4]
    
    # Avis du produit
    reviews = product.reviews.all()
    
    context = {
        'product': product,
        'similar_products': similar_products,
        'reviews': reviews,
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    """Détail d'une catégorie avec ses produits"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category, 
        is_active=True
    ).prefetch_related('images', 'team')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_detail.html', context)


def team_detail(request, slug):
    """Détail d'une équipe avec ses produits"""
    team = get_object_or_404(Team, slug=slug)
    products = Product.objects.filter(
        team=team, 
        is_active=True
    ).prefetch_related('images', 'category')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'team': team,
        'products': products,
    }
    return render(request, 'products/team_detail.html', context)


def search(request):
    """Recherche de produits"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(team__name__icontains=query) |
            Q(category__name__icontains=query)
        ).prefetch_related('images', 'team', 'category')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search.html', context)


@login_required
def add_review(request, slug):
    """Ajouter un avis sur un produit"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Validation
        if not rating or not comment:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return redirect('products:product_detail', slug=product.slug)
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError()
        except ValueError:
            messages.error(request, 'La note doit être entre 1 et 5.')
            return redirect('products:product_detail', slug=product.slug)
        
        # Vérifier si l'utilisateur a déjà laissé un avis
        existing_review = Review.objects.filter(product=product, user=request.user).first()
        
        if existing_review:
            # Mettre à jour l'avis existant
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
            messages.success(request, 'Votre avis a été mis à jour.')
        else:
            # Créer un nouvel avis
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Votre avis a été publié.')
    
    return redirect('products:product_detail', slug=product.slug)
