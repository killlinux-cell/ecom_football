from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.template.loader import render_to_string
from products.models import Product, Category, Team, JerseyCustomization
from orders.models import Order, OrderItem, OrderItemCustomization
from payments.models import Payment, PaymentLog
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
import json

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def dashboard_home(request):
    """Dashboard principal avec toutes les statistiques"""
    
    # Si l'utilisateur n'est pas admin, rediriger vers ses commandes
    if not request.user.is_staff:
        return redirect('dashboard:user_orders')
    
    # Périodes pour les statistiques
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    
    # Statistiques générales
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.filter(is_staff=False).count()  # Seulement les clients (non-staff)
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # Commandes récentes
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # Produits les plus vendus
    top_products = OrderItem.objects.values('product_name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]
    
    # Statistiques des 7 derniers jours
    orders_7_days = Order.objects.filter(created_at__date__gte=last_7_days).count()
    revenue_7_days = Order.objects.filter(
        created_at__date__gte=last_7_days,
        payment_status='paid'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Commandes par statut
    orders_by_status = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Produits en rupture de stock
    out_of_stock_products = Product.objects.filter(
        stock_quantity__lte=0
    ).count()
    
    # Produits en promotion
    products_on_sale = Product.objects.filter(sale_price__isnull=False, sale_price__lt=F('price')).count()
    
    # Statistiques des utilisateurs
    new_users_7_days = User.objects.filter(
        date_joined__date__gte=last_7_days,
        is_staff=False
    ).count()
    
    new_users_30_days = User.objects.filter(
        date_joined__date__gte=last_30_days,
        is_staff=False
    ).count()
    
    # Utilisateurs avec commandes
    users_with_orders = User.objects.filter(
        orders__isnull=False,
        is_staff=False
    ).distinct().count()
    
    # Calcul du taux d'engagement
    engagement_rate = 0
    if total_users > 0:
        engagement_rate = round((users_with_orders / total_users) * 100, 1)
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'orders_7_days': orders_7_days,
        'revenue_7_days': revenue_7_days,
        'orders_by_status': list(orders_by_status),
        'out_of_stock_products': out_of_stock_products,
        'products_on_sale': products_on_sale,
        'new_users_7_days': new_users_7_days,
        'new_users_30_days': new_users_30_days,
        'users_with_orders': users_with_orders,
        'engagement_rate': engagement_rate,
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_orders(request):
    """Dashboard des commandes"""
    
    # Filtres
    status_filter = request.GET.get('status', '')
    payment_status_filter = request.GET.get('payment_status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_query = request.GET.get('search', '')
    
    # Base des commandes pour les filtres
    orders = Order.objects.select_related('user', 'shipping_address').order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if payment_status_filter:
        orders = orders.filter(payment_status=payment_status_filter)
    
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)
    
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    # Actions en lot
    if request.method == 'POST':
        from orders.sync_utils import cancel_order_and_payment
        
        action = request.POST.get('action')
        order_ids = request.POST.getlist('order_ids')
        
        if action and order_ids:
            if action == 'mark_pending':
                Order.objects.filter(id__in=order_ids).update(status='pending')
                messages.success(request, f'{len(order_ids)} commande(s) marquée(s) comme en attente.')
            elif action == 'mark_processing':
                Order.objects.filter(id__in=order_ids).update(status='processing')
                messages.success(request, f'{len(order_ids)} commande(s) marquée(s) comme en cours.')
            elif action == 'mark_shipped':
                Order.objects.filter(id__in=order_ids).update(status='shipped')
                messages.success(request, f'{len(order_ids)} commande(s) marquée(s) comme expédiée(s).')
            elif action == 'mark_delivered':
                Order.objects.filter(id__in=order_ids).update(status='delivered')
                messages.success(request, f'{len(order_ids)} commande(s) marquée(s) comme livrée(s).')
            elif action == 'mark_cancelled':
                # Utiliser la synchronisation pour les annulations
                cancelled_count = 0
                for order_id in order_ids:
                    try:
                        order = Order.objects.get(id=order_id)
                        cancel_order_and_payment(order, updated_by=request.user)
                        cancelled_count += 1
                    except Order.DoesNotExist:
                        continue
                messages.success(request, f'{cancelled_count} commande(s) et paiement(s) associé(s) annulé(s) avec succès.')
            
            return redirect('dashboard:orders')
    
    # Statistiques GLOBALES (toutes les commandes, pas seulement les filtrées)
    all_orders = Order.objects.all()
    
    # Total des commandes
    total_orders_count = all_orders.count()
    
    # Commandes en attente
    pending_orders_count = all_orders.filter(status='pending').count()
    
    # Commandes livrées
    delivered_orders_count = all_orders.filter(status='delivered').count()
    
    # Revenus totaux (commandes payées)
    total_revenue = all_orders.filter(payment_status='paid').aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # Pagination des commandes filtrées
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'total_orders_count': total_orders_count,
        'pending_orders_count': pending_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'total_revenue': total_revenue,
        'status_filter': status_filter,
        'payment_status_filter': payment_status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'search_query': search_query,
    }
    
    return render(request, 'dashboard/orders.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_order_detail(request, order_id):
    """Détails d'une commande"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all().prefetch_related('customizations__customization')
    
    # Récupérer les informations de paiement Wave si elles existent
    payment = None
    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        pass
    
    if request.method == 'POST':
        from orders.sync_utils import sync_order_payment_status, cancel_order_and_payment
        
        # Mise à jour du statut de la commande
        new_status = request.POST.get('status')
        new_payment_status = request.POST.get('payment_status')
        notes = request.POST.get('notes', '')
        
        # Sauvegarder les anciens statuts pour comparaison
        old_payment_status = order.payment_status
        old_status = order.status
        
        # Gestion spéciale pour les annulations
        if new_status == 'cancelled' and old_status != 'cancelled':
            cancel_order_and_payment(order, updated_by=request.user)
            messages.success(request, 'Commande et paiement annulés avec succès!')
        else:
            # Mise à jour normale
            if new_status:
                order.status = new_status
            if new_payment_status:
                order.payment_status = new_payment_status
            if notes:
                order.notes = notes
            
            order.save()
            
            # Synchroniser avec le paiement si le statut de paiement a changé
            if new_payment_status and new_payment_status != old_payment_status:
                sync_success = sync_order_payment_status(order, new_payment_status, updated_by=request.user)
                if sync_success:
                    messages.success(request, 'Commande et paiement synchronisés avec succès!')
                else:
                    messages.success(request, 'Commande mise à jour avec succès!')
            else:
                messages.success(request, 'Commande mise à jour avec succès!')
        
        return redirect('dashboard:order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'order_items': order_items,
        'payment': payment,
    }
    
    return render(request, 'dashboard/order_detail.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_order_invoice(request, order_id):
    """Génération de facture PDF"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all().prefetch_related('customizations__customization')
    
    # Générer le HTML de la facture
    html_content = render_to_string('dashboard/invoice.html', {
        'order': order,
        'order_items': order_items,
    })
    
    # Pour l'instant, on retourne le HTML. Plus tard, on pourra utiliser weasyprint pour le PDF
    return HttpResponse(html_content, content_type='text/html')

@login_required
@user_passes_test(is_admin)
def dashboard_products(request):
    """Gestion des produits"""
    products = Product.objects.select_related('category', 'team').order_by('-created_at')
    
    # Filtres
    category_filter = request.GET.get('category', '')
    team_filter = request.GET.get('team', '')
    search_query = request.GET.get('search', '')
    stock_filter = request.GET.get('stock', '')
    
    if category_filter:
        products = products.filter(category__slug=category_filter)
    if team_filter:
        products = products.filter(team__slug=team_filter)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    if stock_filter == 'out_of_stock':
        products = products.filter(stock_quantity__lte=0)
    elif stock_filter == 'low_stock':
        products = products.filter(stock_quantity__lte=5, stock_quantity__gt=0)
    
    # Actions en lot
    if request.method == 'POST':
        action = request.POST.get('action')
        product_ids = request.POST.getlist('product_ids')
        
        if action and product_ids:
            if action == 'activate':
                Product.objects.filter(id__in=product_ids).update(is_active=True)
                messages.success(request, f'{len(product_ids)} produit(s) activé(s).')
            elif action == 'deactivate':
                Product.objects.filter(id__in=product_ids).update(is_active=False)
                messages.success(request, f'{len(product_ids)} produit(s) désactivé(s).')
            elif action == 'feature':
                Product.objects.filter(id__in=product_ids).update(is_featured=True)
                messages.success(request, f'{len(product_ids)} produit(s) mis en vedette.')
            elif action == 'unfeature':
                Product.objects.filter(id__in=product_ids).update(is_featured=False)
                messages.success(request, f'{len(product_ids)} produit(s) retiré(s) de la vedette.')
            elif action == 'delete':
                Product.objects.filter(id__in=product_ids).delete()
                messages.success(request, f'{len(product_ids)} produit(s) supprimé(s).')
            
            return redirect('dashboard:products')
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    teams = Team.objects.all()
    
    # Statistiques
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    out_of_stock = Product.objects.filter(stock_quantity__lte=0).count()
    low_stock = Product.objects.filter(stock_quantity__lte=5, stock_quantity__gt=0).count()
    
    context = {
        'products': page_obj,
        'categories': categories,
        'teams': teams,
        'current_category': category_filter,
        'current_team': team_filter,
        'search_query': search_query,
        'stock_filter': stock_filter,
        'total_products': total_products,
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
    }
    
    return render(request, 'dashboard/products.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_product_edit(request, product_id):
    """Édition d'un produit"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        # Logique de mise à jour du produit
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.sale_price = request.POST.get('sale_price') or None
        product.stock_quantity = request.POST.get('stock_quantity')
        product.is_active = request.POST.get('is_active') == 'on'
        product.is_featured = request.POST.get('is_featured') == 'on'
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        messages.success(request, 'Produit mis à jour avec succès!')
        return redirect('dashboard:products')
    
    categories = Category.objects.all()
    teams = Team.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
        'teams': teams,
    }
    
    return render(request, 'dashboard/product_edit.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_product_create(request):
    """Création d'un nouveau produit"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Créer le produit
                product = Product.objects.create(
                    name=request.POST.get('name'),
                    description=request.POST.get('description'),
                    price=request.POST.get('price'),
                    sale_price=request.POST.get('sale_price') or None,
                    stock_quantity=request.POST.get('stock_quantity'),
                    category_id=request.POST.get('category'),
                    team_id=request.POST.get('team'),
                    is_active=request.POST.get('is_active') == 'on',
                    is_featured=request.POST.get('is_featured') == 'on',
                )
                
                # Gérer l'image principale
                if 'image' in request.FILES:
                    product.image = request.FILES['image']
                    product.save()
                
                # Gérer les images supplémentaires
                if 'additional_images' in request.FILES:
                    from products.models import ProductImage
                    for i, image in enumerate(request.FILES.getlist('additional_images')):
                        ProductImage.objects.create(
                            product=product,
                            image=image,
                            alt_text=f"{product.name} - Image {i+1}",
                            order=i+1
                        )
                
                messages.success(request, 'Produit créé avec succès!')
                return redirect('dashboard:product_edit', product_id=product.id)
                
        except Exception as e:
            messages.error(request, f'Erreur lors de la création: {str(e)}')
    
    categories = Category.objects.all()
    teams = Team.objects.all()
    
    context = {
        'categories': categories,
        'teams': teams,
    }
    
    return render(request, 'dashboard/product_create.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_categories(request):
    """Gestion des catégories"""
    categories = Category.objects.all().order_by('name')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            Category.objects.create(name=name, description=description)
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('dashboard:categories')
    
    context = {'categories': categories}
    return render(request, 'dashboard/categories.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_teams(request):
    """Gestion des équipes"""
    teams = Team.objects.all().order_by('name')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        country = request.POST.get('country')
        league = request.POST.get('league')
        
        if name and country:
            Team.objects.create(name=name, country=country, league=league)
            messages.success(request, 'Équipe créée avec succès!')
            return redirect('dashboard:teams')
    
    context = {'teams': teams}
    return render(request, 'dashboard/teams.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_users(request):
    """Gestion des utilisateurs"""
    users = User.objects.all().order_by('-date_joined')
    
    # Filtres
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'dashboard/users.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_user_edit(request, user_id):
    """Édition d'un utilisateur"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        
        # Gestion du mot de passe
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        user.save()
        messages.success(request, 'Utilisateur mis à jour avec succès!')
        return redirect('dashboard:users')
    
    context = {'user': user}
    return render(request, 'dashboard/user_edit.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_customizations(request):
    """Gestion des personnalisations"""
    customizations = JerseyCustomization.objects.all().order_by('-created_at')
    
    # Filtres
    product_filter = request.GET.get('product', '')
    if product_filter:
        # Filtrer par type de personnalisation au lieu de produit
        customizations = customizations.filter(customization_type=product_filter)
    
    # Pagination
    paginator = Paginator(customizations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Récupérer tous les types de personnalisation disponibles
    customization_types = JerseyCustomization.CUSTOMIZATION_TYPES
    
    context = {
        'customizations': page_obj,
        'customization_types': customization_types,
        'current_type': product_filter,
    }
    
    return render(request, 'dashboard/customizations.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_analytics(request):
    """Analyses et rapports"""
    
    # Statistiques des ventes par mois
    current_year = timezone.now().year
    monthly_sales = []
    
    for month in range(1, 13):
        month_start = timezone.datetime(current_year, month, 1, tzinfo=timezone.utc)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(days=1)
        
        month_revenue = Order.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end,
            payment_status='paid'
        ).aggregate(total=Sum('total'))['total'] or 0
        
        month_orders = Order.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).count()
        
        monthly_sales.append({
            'month': month_start.strftime('%B'),
            'revenue': month_revenue,
            'orders': month_orders
        })
    
    # Top 10 des produits les plus vendus
    top_products = OrderItem.objects.values('product_name').annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(F('price') * F('quantity'))
    ).order_by('-total_sold')[:10]
    
    # Statistiques des équipes
    team_stats = Team.objects.annotate(
        product_count=Count('products'),
        total_sales=Sum('products__orderitem__quantity', default=0)
    ).order_by('-total_sales')
    
    context = {
        'monthly_sales': monthly_sales,
        'top_products': top_products,
        'team_stats': team_stats,
    }
    
    return render(request, 'dashboard/analytics.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_payments(request):
    """Dashboard des paiements"""
    
    # Filtres
    status_filter = request.GET.get('status', '')
    payment_method_filter = request.GET.get('payment_method', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_query = request.GET.get('search', '')
    
    payments = Payment.objects.select_related('order', 'order__user').order_by('-created_at')
    
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    if payment_method_filter:
        payments = payments.filter(payment_method=payment_method_filter)
    
    if date_from:
        payments = payments.filter(created_at__date__gte=date_from)
    
    if date_to:
        payments = payments.filter(created_at__date__lte=date_to)
    
    if search_query:
        payments = payments.filter(
            Q(payment_id__icontains=search_query) |
            Q(order__order_number__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_email__icontains=search_query) |
            Q(wave_transaction_id__icontains=search_query)
        )
    
    # Actions en lot
    if request.method == 'POST':
        from orders.sync_utils import validate_payment_and_order, sync_payment_order_status
        
        action = request.POST.get('action')
        payment_ids = request.POST.getlist('payment_ids')
        
        if action and payment_ids:
            if action == 'validate_wave_payments':
                updated = 0
                for payment in Payment.objects.filter(id__in=payment_ids, payment_method='wave_direct', status='pending'):
                    if payment.wave_transaction_id:
                        validate_payment_and_order(payment, updated_by=request.user)
                        updated += 1
                
                if updated == 1:
                    messages.success(request, "1 paiement Wave et commande associée ont été validés.")
                else:
                    messages.success(request, f"{updated} paiements Wave et commandes associées ont été validés.")
                    
            elif action == 'mark_completed':
                updated = 0
                for payment in Payment.objects.filter(id__in=payment_ids):
                    sync_payment_order_status(payment, 'completed', updated_by=request.user)
                    updated += 1
                messages.success(request, f"{updated} paiement(s) et commande(s) associée(s) marqué(s) comme terminé(s).")
                
            elif action == 'mark_failed':
                updated = 0
                for payment in Payment.objects.filter(id__in=payment_ids):
                    sync_payment_order_status(payment, 'failed', updated_by=request.user)
                    updated += 1
                messages.success(request, f"{updated} paiement(s) et commande(s) associée(s) marqué(s) comme échoué(s).")
            
            return redirect('dashboard:payments')
    
    # Statistiques des paiements
    total_payments = payments.count()
    total_amount = payments.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Compteurs par statut
    pending_payments_count = payments.filter(status='pending').count()
    completed_payments_count = payments.filter(status='completed').count()
    failed_payments_count = payments.filter(status='failed').count()
    cancelled_payments_count = payments.filter(status='cancelled').count()
    
    # Paiements par statut (pour les graphiques)
    payments_by_status = Payment.objects.values('status').annotate(
        count=Count('id'),
        total_amount=Sum('amount')
    ).order_by('status')
    
    # Paiements Wave en attente
    wave_pending_count = Payment.objects.filter(
        payment_method='wave_direct', 
        status='pending'
    ).count()
    
    context = {
        'payments': payments,
        'total_payments': total_payments,
        'total_amount': total_amount,
        'pending_payments_count': pending_payments_count,
        'completed_payments_count': completed_payments_count,
        'failed_payments_count': failed_payments_count,
        'cancelled_payments_count': cancelled_payments_count,
        'payments_by_status': list(payments_by_status),
        'wave_pending_count': wave_pending_count,
        'status_filter': status_filter,
        'payment_method_filter': payment_method_filter,
        'date_from': date_from,
        'date_to': date_to,
        'search_query': search_query,
    }
    
    return render(request, 'dashboard/payments.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_payment_logs(request):
    """Logs des paiements"""
    logs = PaymentLog.objects.select_related('payment', 'payment__order').order_by('-created_at')
    
    # Filtres
    event_filter = request.GET.get('event', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if event_filter:
        logs = logs.filter(event=event_filter)
    
    if date_from:
        logs = logs.filter(created_at__date__gte=date_from)
    
    if date_to:
        logs = logs.filter(created_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Événements disponibles
    events = PaymentLog.objects.values_list('event', flat=True).distinct().order_by('event')
    
    context = {
        'logs': page_obj,
        'events': events,
        'event_filter': event_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'dashboard/payment_logs.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_settings(request):
    """Paramètres du système"""
    if request.method == 'POST':
        # Ici vous pouvez ajouter la logique pour sauvegarder les paramètres
        messages.success(request, 'Paramètres mis à jour avec succès!')
        return redirect('dashboard:settings')
    
    context = {}
    return render(request, 'dashboard/settings.html', context)

@login_required
@user_passes_test(is_admin)
def dashboard_notifications_api(request):
    """API pour récupérer les nouvelles commandes et notifications"""
    try:
        # Récupérer le timestamp de la dernière vérification
        last_check = request.GET.get('last_check')
        if last_check:
            last_check = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
        else:
            # Par défaut, vérifier les 5 dernières minutes
            last_check = timezone.now() - timedelta(minutes=5)
        
        # Nouvelles commandes
        new_orders = Order.objects.filter(
            created_at__gt=last_check
        ).order_by('-created_at')[:10]
        
        # Nouvelles commandes en attente
        pending_orders = Order.objects.filter(
            status='pending',
            created_at__gt=last_check
        ).count()
        
        # Nouveaux paiements en attente
        pending_payments = Payment.objects.filter(
            status='pending',
            created_at__gt=last_check
        ).count()
        
        # Paiements Wave en attente
        wave_pending = Payment.objects.filter(
            payment_method='wave_direct',
            status='pending'
        ).count()
        
        notifications = []
        
        # Notifications pour les nouvelles commandes
        for order in new_orders:
            notifications.append({
                'type': 'new_order',
                'title': 'Nouvelle commande',
                'message': f'Commande #{order.order_number} de {order.user.get_full_name() or order.user.username}',
                'amount': float(order.total),
                'order_id': order.id,
                'created_at': order.created_at.isoformat(),
                'icon': 'fas fa-shopping-cart',
                'color': 'success'
            })
        
        # Notification pour les paiements Wave en attente
        if wave_pending > 0:
            notifications.append({
                'type': 'wave_pending',
                'title': 'Paiements Wave en attente',
                'message': f'{wave_pending} paiement(s) Wave en attente de validation',
                'count': wave_pending,
                'created_at': timezone.now().isoformat(),
                'icon': 'fas fa-exclamation-triangle',
                'color': 'warning'
            })
        
        # Statistiques en temps réel
        stats = {
            'total_orders_today': Order.objects.filter(
                created_at__date=timezone.now().date()
            ).count(),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'total_revenue_today': Order.objects.filter(
                created_at__date=timezone.now().date(),
                payment_status='paid'
            ).aggregate(total=Sum('total'))['total'] or 0
        }
        
        return JsonResponse({
            'success': True,
            'notifications': notifications,
            'stats': stats,
            'last_check': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def user_orders(request):
    """Vue pour que les utilisateurs voient leurs commandes"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/user_orders.html', context)

@login_required
def user_order_detail(request, order_id):
    """Vue pour que les utilisateurs voient les détails de leur commande"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'dashboard/user_order_detail.html', context)

@login_required
def user_order_invoice(request, order_id):
    """Vue pour que les utilisateurs voient leur facture"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'company_name': 'Orapide Shop',
        'company_address': 'Abidjan, Côte d\'Ivoire',
        'company_phone': '+225 XX XX XX XX',
        'company_email': 'contact@orapide.shop',
    }
    
    return render(request, 'dashboard/user_invoice.html', context)
