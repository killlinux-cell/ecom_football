from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Dashboard emails
    path('', views.dashboard_emails, name='dashboard_emails'),
    
    # Templates
    path('templates/', views.email_templates, name='email_templates'),
    path('templates/<int:template_id>/', views.email_template_detail, name='email_template_detail'),
    
    # Logs
    path('logs/', views.email_logs, name='email_logs'),
    path('logs/<int:log_id>/resend/', views.resend_email, name='resend_email'),
    
    # Paramètres
    path('settings/', views.email_settings, name='email_settings'),
    path('settings/test/', views.send_test_email, name='send_test_email'),
]
