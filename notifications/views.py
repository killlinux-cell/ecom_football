from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import EmailTemplate, EmailLog, EmailSettings
from .email_service import get_email_service
from orders.models import Order
from payments.models import Payment


def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin)
def dashboard_emails(request):
    """Dashboard principal des emails"""
    # Statistiques générales
    total_emails = EmailLog.objects.count()
    sent_emails = EmailLog.objects.filter(status='sent').count()
    failed_emails = EmailLog.objects.filter(status='failed').count()
    pending_emails = EmailLog.objects.filter(status='pending').count()
    
    # Emails des 7 derniers jours
    week_ago = timezone.now() - timedelta(days=7)
    recent_emails = EmailLog.objects.filter(created_at__gte=week_ago).count()
    
    # Emails par type
    emails_by_type = EmailLog.objects.values('template__template_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Derniers emails envoyés
    recent_email_logs = EmailLog.objects.select_related(
        'template', 'order', 'user'
    ).order_by('-created_at')[:10]
    
    context = {
        'total_emails': total_emails,
        'sent_emails': sent_emails,
        'failed_emails': failed_emails,
        'pending_emails': pending_emails,
        'recent_emails': recent_emails,
        'emails_by_type': emails_by_type,
        'recent_email_logs': recent_email_logs,
    }
    
    return render(request, 'notifications/dashboard_emails.html', context)


@login_required
@user_passes_test(is_admin)
def email_templates(request):
    """Gestion des templates d'emails"""
    templates = EmailTemplate.objects.all().order_by('template_type', 'name')
    
    # Recherche
    search = request.GET.get('search', '')
    if search:
        templates = templates.filter(
            Q(name__icontains=search) |
            Q(subject__icontains=search) |
            Q(template_type__icontains=search)
        )
    
    # Filtre par type
    template_type = request.GET.get('type', '')
    if template_type:
        templates = templates.filter(template_type=template_type)
    
    # Pagination
    paginator = Paginator(templates, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'templates': page_obj,
        'search': search,
        'template_type': template_type,
        'template_types': EmailTemplate.TEMPLATE_TYPES,
    }
    
    return render(request, 'notifications/email_templates.html', context)


@login_required
@user_passes_test(is_admin)
def email_template_detail(request, template_id):
    """Détail et édition d'un template"""
    template = get_object_or_404(EmailTemplate, id=template_id)
    
    if request.method == 'POST':
        template.name = request.POST.get('name', template.name)
        template.subject = request.POST.get('subject', template.subject)
        template.html_content = request.POST.get('html_content', template.html_content)
        template.text_content = request.POST.get('text_content', template.text_content)
        template.is_active = request.POST.get('is_active') == 'on'
        template.save()
        
        messages.success(request, f"Template '{template.name}' mis à jour avec succès!")
        return redirect('notifications:email_template_detail', template_id=template.id)
    
    context = {
        'template': template,
    }
    
    return render(request, 'notifications/email_template_detail.html', context)


@login_required
@user_passes_test(is_admin)
def email_logs(request):
    """Logs des emails envoyés"""
    logs = EmailLog.objects.select_related(
        'template', 'order', 'user'
    ).order_by('-created_at')
    
    # Filtres
    status = request.GET.get('status', '')
    if status:
        logs = logs.filter(status=status)
    
    template_type = request.GET.get('template_type', '')
    if template_type:
        logs = logs.filter(template__template_type=template_type)
    
    # Recherche
    search = request.GET.get('search', '')
    if search:
        logs = logs.filter(
            Q(recipient_email__icontains=search) |
            Q(subject__icontains=search) |
            Q(order__order_number__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'logs': page_obj,
        'status': status,
        'template_type': template_type,
        'search': search,
        'status_choices': EmailLog.STATUS_CHOICES,
        'template_types': EmailTemplate.TEMPLATE_TYPES,
    }
    
    return render(request, 'notifications/email_logs.html', context)


@login_required
@user_passes_test(is_admin)
def email_settings(request):
    """Configuration des paramètres email"""
    settings_obj, created = EmailSettings.objects.get_or_create(
        defaults={
            'from_email': 'noreply@maillots-football.ci',
            'from_name': 'Maillots Football',
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
        }
    )
    
    if request.method == 'POST':
        settings_obj.smtp_host = request.POST.get('smtp_host', settings_obj.smtp_host)
        settings_obj.smtp_port = int(request.POST.get('smtp_port', settings_obj.smtp_port))
        settings_obj.smtp_username = request.POST.get('smtp_username', settings_obj.smtp_username)
        settings_obj.smtp_password = request.POST.get('smtp_password', settings_obj.smtp_password)
        settings_obj.use_tls = request.POST.get('use_tls') == 'on'
        settings_obj.from_email = request.POST.get('from_email', settings_obj.from_email)
        settings_obj.from_name = request.POST.get('from_name', settings_obj.from_name)
        settings_obj.is_active = request.POST.get('is_active') == 'on'
        settings_obj.send_order_confirmations = request.POST.get('send_order_confirmations') == 'on'
        settings_obj.send_payment_confirmations = request.POST.get('send_payment_confirmations') == 'on'
        settings_obj.send_shipping_notifications = request.POST.get('send_shipping_notifications') == 'on'
        settings_obj.send_cart_reminders = request.POST.get('send_cart_reminders') == 'on'
        settings_obj.send_stock_alerts = request.POST.get('send_stock_alerts') == 'on'
        settings_obj.max_emails_per_hour = int(request.POST.get('max_emails_per_hour', settings_obj.max_emails_per_hour))
        settings_obj.cart_reminder_delay_hours = int(request.POST.get('cart_reminder_delay_hours', settings_obj.cart_reminder_delay_hours))
        settings_obj.save()
        
        messages.success(request, "Paramètres email mis à jour avec succès!")
        return redirect('notifications:email_settings')
    
    context = {
        'settings': settings_obj,
    }
    
    return render(request, 'notifications/email_settings.html', context)


@login_required
@user_passes_test(is_admin)
def send_test_email(request):
    """Envoie un email de test"""
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        template_type = request.POST.get('template_type')
        
        if not recipient_email or not template_type:
            messages.error(request, "Email et type de template requis!")
            return redirect('notifications:email_settings')
        
        try:
            # Créer un email de test
            template = EmailTemplate.objects.get(template_type=template_type, is_active=True)
            
            # Données de test
            test_data = {
                'customer_name': 'Test User',
                'order_number': 'TEST123',
                'order_total': 25000,
                'payment_amount': 25000,
                'payment_method': 'Wave',
            }
            
            # Rendu du contenu
            from django.template import Template, Context
            html_content = Template(template.html_content).render(Context(test_data))
            text_content = Template(template.text_content).render(Context(test_data)) if template.text_content else None
            
            # Création du log
            email_log = EmailLog.objects.create(
                template=template,
                recipient_email=recipient_email,
                recipient_name='Test User',
                subject=f"[TEST] {template.subject}",
                email_data=test_data,
                status='pending'
            )
            
            # Envoi
            success = get_email_service()._send_email(email_log, html_content, text_content)
            
            if success:
                messages.success(request, f"Email de test envoyé à {recipient_email}!")
            else:
                messages.error(request, "Erreur lors de l'envoi de l'email de test!")
                
        except EmailTemplate.DoesNotExist:
            messages.error(request, "Template non trouvé!")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return redirect('notifications:email_settings')


@login_required
@user_passes_test(is_admin)
def resend_email(request, log_id):
    """Renvoyer un email"""
    email_log = get_object_or_404(EmailLog, id=log_id)
    
    try:
        # Rendu du contenu
        from django.template import Template, Context
        html_content = Template(email_log.template.html_content).render(Context(email_log.email_data))
        text_content = Template(email_log.template.text_content).render(Context(email_log.email_data)) if email_log.template.text_content else None
        
        # Créer un nouveau log
        new_log = EmailLog.objects.create(
            template=email_log.template,
            recipient_email=email_log.recipient_email,
            recipient_name=email_log.recipient_name,
            subject=f"[RENVOI] {email_log.subject}",
            email_data=email_log.email_data,
            order=email_log.order,
            payment=email_log.payment,
            user=email_log.user,
            status='pending'
        )
        
        # Envoi
        success = get_email_service()._send_email(new_log, html_content, text_content)
        
        if success:
            messages.success(request, "Email renvoyé avec succès!")
        else:
            messages.error(request, "Erreur lors du renvoi de l'email!")
            
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
    
    return redirect('notifications:email_logs')
