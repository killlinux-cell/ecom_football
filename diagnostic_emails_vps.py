#!/usr/bin/env python
"""
Script de diagnostic pour les emails sur le VPS
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def diagnostic_complet():
    """Diagnostic complet du système d'emails"""
    print("🔍 DIAGNOSTIC COMPLET DU SYSTÈME D'EMAILS")
    print("=" * 60)
    
    # 1. Vérifier les modèles
    print("\n📋 1. Vérification des modèles...")
    try:
        from notifications.models import EmailTemplate, EmailSettings, EmailLog
        print("✅ Modèles importés avec succès")
    except ImportError as e:
        print(f"❌ Erreur import modèles: {e}")
        return False
    
    # 2. Vérifier les templates
    print("\n📧 2. Vérification des templates d'emails...")
    try:
        templates = EmailTemplate.objects.all()
        print(f"📊 {templates.count()} templates trouvés:")
        
        required_types = [
            'order_confirmation',
            'payment_confirmation', 
            'order_shipped',
            'order_delivered',
            'cart_reminder',
            'stock_alert'
        ]
        
        for template_type in required_types:
            template = EmailTemplate.objects.filter(
                template_type=template_type,
                is_active=True
            ).first()
            
            if template:
                print(f"   ✅ {template_type}: {template.name}")
            else:
                print(f"   ❌ {template_type}: MANQUANT")
        
    except Exception as e:
        print(f"❌ Erreur vérification templates: {e}")
        return False
    
    # 3. Vérifier les paramètres SMTP
    print("\n⚙️ 3. Vérification des paramètres SMTP...")
    try:
        settings = EmailSettings.objects.first()
        if settings:
            print(f"✅ Paramètres trouvés:")
            print(f"   - Email expéditeur: {settings.from_email}")
            print(f"   - Nom expéditeur: {settings.from_name}")
            print(f"   - SMTP Host: {settings.smtp_host}")
            print(f"   - SMTP Port: {settings.smtp_port}")
            print(f"   - TLS activé: {'Oui' if settings.use_tls else 'Non'}")
            print(f"   - Statut: {'✅ Actif' if settings.is_active else '❌ Inactif'}")
        else:
            print("❌ Aucun paramètre SMTP configuré")
    except Exception as e:
        print(f"❌ Erreur vérification paramètres: {e}")
    
    # 4. Vérifier le service d'emails
    print("\n🔧 4. Vérification du service d'emails...")
    try:
        from notifications.email_service import get_email_service
        service = get_email_service()
        
        if service.settings:
            print("✅ Service d'emails initialisé")
            print(f"   - Paramètres chargés: Oui")
            print(f"   - Statut: {'Actif' if service.settings.is_active else 'Inactif'}")
        else:
            print("⚠️ Service d'emails initialisé mais sans paramètres")
    except Exception as e:
        print(f"❌ Erreur service d'emails: {e}")
    
    # 5. Vérifier les logs d'emails
    print("\n📝 5. Vérification des logs d'emails...")
    try:
        logs = EmailLog.objects.all()
        print(f"📊 {logs.count()} logs d'emails trouvés")
        
        if logs.exists():
            recent_logs = logs.order_by('-created_at')[:5]
            print("   Derniers envois:")
            for log in recent_logs:
                status_icon = "✅" if log.status == 'sent' else "❌" if log.status == 'failed' else "⏳"
                print(f"   {status_icon} {log.created_at.strftime('%d/%m/%Y %H:%M')} - {log.recipient_email} - {log.status}")
    except Exception as e:
        print(f"❌ Erreur vérification logs: {e}")
    
    # 6. Test de rendu de template
    print("\n🎨 6. Test de rendu de template...")
    try:
        template = EmailTemplate.objects.filter(
            template_type='order_confirmation',
            is_active=True
        ).first()
        
        if template:
            # Test de rendu simple
            from django.template import Template, Context
            test_context = {
                'customer_name': 'Test User',
                'order_number': 'TEST123',
                'order_total': 25000,
            }
            
            try:
                rendered = Template(template.html_content).render(Context(test_context))
                print("✅ Template de confirmation rendu avec succès")
            except Exception as e:
                print(f"❌ Erreur rendu template: {e}")
        else:
            print("❌ Template de confirmation non trouvé")
    except Exception as e:
        print(f"❌ Erreur test rendu: {e}")
    
    return True

def suggestions_correction():
    """Suggestions de correction"""
    print("\n💡 SUGGESTIONS DE CORRECTION")
    print("=" * 40)
    
    try:
        from notifications.models import EmailTemplate, EmailSettings
        
        # Vérifier les templates manquants
        required_types = [
            'order_confirmation',
            'payment_confirmation', 
            'order_shipped',
            'order_delivered',
            'cart_reminder',
            'stock_alert'
        ]
        
        missing_templates = []
        for template_type in required_types:
            if not EmailTemplate.objects.filter(template_type=template_type, is_active=True).exists():
                missing_templates.append(template_type)
        
        if missing_templates:
            print("🔧 Templates manquants détectés:")
            print("   Solution: python manage.py init_email_templates")
            print(f"   Templates à créer: {', '.join(missing_templates)}")
        
        # Vérifier les paramètres SMTP
        if not EmailSettings.objects.exists():
            print("🔧 Paramètres SMTP manquants:")
            print("   Solution: Configurer via /dashboard/emails/settings/")
            print("   Ou créer manuellement dans l'admin Django")
        
        # Vérifier l'activation
        settings = EmailSettings.objects.first()
        if settings and not settings.is_active:
            print("🔧 Service d'emails désactivé:")
            print("   Solution: Activer dans /dashboard/emails/settings/")
        
    except Exception as e:
        print(f"❌ Erreur suggestions: {e}")

def main():
    """Fonction principale"""
    success = diagnostic_complet()
    suggestions_correction()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 DIAGNOSTIC TERMINÉ")
        print("📋 Consultez les suggestions ci-dessus pour corriger les problèmes")
    else:
        print("💥 DIAGNOSTIC ÉCHOUÉ")
        print("❌ Des erreurs critiques ont été détectées")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
