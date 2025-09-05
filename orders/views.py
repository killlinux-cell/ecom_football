from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from .models import Order, OrderItem, Address, OrderItemCustomization
from .forms import OrderCreateForm, AddressForm
from cart.cart import Cart


@login_required
def order_create(request):
    """Créer une nouvelle commande"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, "Votre panier est vide.")
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Créer la commande
                order = form.save(commit=False)
                order.user = request.user
                
                # Calculer les totaux
                subtotal = cart.get_total_price()
                
                # Calculer les frais de livraison selon les paramètres
                from core.models import ShippingSettings
                shipping_settings = ShippingSettings.get_active_settings()
                shipping_cost = shipping_settings.calculate_shipping_cost(subtotal)
                
                total = subtotal + shipping_cost
                
                order.subtotal = subtotal
                order.shipping_cost = shipping_cost
                order.total = total
                order.save()
                
                # VALIDATION: Vérifier que le panier n'est pas vide
                if len(cart) == 0:
                    messages.error(request, "Erreur: Le panier est vide lors de la création de la commande.")
                    order.delete()
                    return redirect('cart:cart_detail')
                
                # Créer les articles de commande avec personnalisations
                articles_created = 0
                for item in cart:
                    # Récupérer le cart_item pour les personnalisations
                    from cart.models import CartItem
                    cart_item = CartItem.objects.filter(
                        cart__user=request.user,
                        product=item['product'],
                        size=item['size']
                    ).first()
                    
                    # Créer l'article de commande avec le prix actuel (promotion si applicable)
                    current_price = item['product'].current_price
                    base_price = current_price * item['quantity']
                    
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].name,
                        size=item['size'],
                        quantity=item['quantity'],
                        price=current_price,  # Utiliser le prix actuel (promotion)
                        total_price=base_price  # Prix de base avec promotion
                    )
                    
                    # Copier les personnalisations du cart_item vers l'order_item
                    if cart_item:
                        for cart_custom in cart_item.customizations.all():
                            OrderItemCustomization.objects.create(
                                order_item=order_item,
                                customization=cart_custom.customization,
                                custom_text=cart_custom.custom_text,
                                quantity=cart_custom.quantity,
                                price=cart_custom.price
                            )
                        
                        # Mettre à jour le total_price avec les personnalisations
                        order_item.total_price = order_item.get_total_with_customizations()
                        order_item.save()
                    
                    articles_created += 1
                
                # VALIDATION FINALE: Vérifier qu'au moins un article a été créé
                if articles_created == 0:
                    messages.error(request, "Erreur: Aucun article n'a pu être ajouté à la commande.")
                    order.delete()
                    return redirect('cart:cart_detail')
                
                # Recalculer les totaux pour s'assurer de la cohérence
                order.recalculate_totals()
                
                # Vider le panier
                cart.clear()
                
                messages.success(request, f"Commande {order.order_number} créée avec succès.")
                
                # Rediriger selon la méthode de paiement choisie
                payment_method = request.POST.get('payment_method', 'paydunya')
                order.payment_method = payment_method
                order.save()
                
                if payment_method == 'wave_direct':
                    return redirect('payments:wave_direct_payment', order_id=order.id)
                elif payment_method == 'cash_on_delivery':
                    # Pour le paiement à la livraison, marquer comme en attente de paiement
                    order.payment_status = 'cash_on_delivery'
                    order.save()
                    messages.info(request, "Votre commande sera payée lors de la livraison.")
                    return redirect('orders:order_detail', order_id=order.id)
                else:
                    return redirect('payments:process_payment', order_id=order.id)
    else:
        form = OrderCreateForm()
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/order_create.html', context)


@login_required
def mark_cash_payment_received(request, order_id):
    """Marquer une commande comme payée à la livraison (pour l'admin)"""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('core:home')
    
    order = get_object_or_404(Order, id=order_id)
    
    if order.payment_method == 'cash_on_delivery' and order.payment_status == 'cash_on_delivery':
        order.payment_status = 'paid'
        order.paid_at = timezone.now()
        order.save()
        
        messages.success(request, f"Commande {order.order_number} marquée comme payée.")
        
        # Envoyer un email de confirmation si le système email est activé
        try:
            from notifications.email_service import get_email_service
            email_service = get_email_service()
            if email_service.settings and email_service.settings.send_order_confirmations:
                email_service.send_order_confirmation(order)
        except Exception as e:
            print(f"Erreur envoi email: {str(e)}")
    else:
        messages.error(request, "Cette commande ne peut pas être marquée comme payée à la livraison.")
    
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    """Afficher le détail d'une commande"""
    # Permettre aux administrateurs de voir toutes les commandes
    if request.user.is_staff or request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
    else:
        # Les utilisateurs normaux ne peuvent voir que leurs propres commandes
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_list(request):
    """Liste des commandes de l'utilisateur"""
    # Permettre aux administrateurs de voir toutes les commandes
    if request.user.is_staff or request.user.is_superuser:
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Les utilisateurs normaux ne peuvent voir que leurs propres commandes
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_cancel(request, order_id):
    """Annuler une commande"""
    from orders.sync_utils import cancel_order_and_payment
    
    # Permettre aux administrateurs d'annuler n'importe quelle commande
    if request.user.is_staff or request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
    else:
        # Les utilisateurs normaux ne peuvent annuler que leurs propres commandes
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.can_be_cancelled:
        # Utiliser la fonction de synchronisation pour annuler commande et paiement
        cancel_order_and_payment(order, updated_by=request.user)
        messages.success(request, f"Commande {order.order_number} et paiement associé annulés avec succès.")
    else:
        messages.error(request, "Cette commande ne peut pas être annulée.")
    
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def address_create(request):
    """Créer une nouvelle adresse"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Adresse ajoutée avec succès.")
            return redirect('orders:order_create')
    else:
        form = AddressForm()
    
    context = {
        'form': form,
    }
    return render(request, 'orders/address_form.html', context)
