#!/usr/bin/env python
"""
Script pour déployer les templates d'emails sur le VPS
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def deploy_email_templates():
    """Déploie les templates d'emails sur le VPS"""
    print("🚀 Déploiement des templates d'emails sur le VPS...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # 1. Vérifier les migrations
        print("📋 Vérification des migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # 2. Initialiser les templates d'emails
        print("📧 Initialisation des templates d'emails...")
        execute_from_command_line(['manage.py', 'init_email_templates'])
        
        # 3. Vérifier que les templates sont créés
        from notifications.models import EmailTemplate
        templates = EmailTemplate.objects.all()
        
        print(f"✅ {templates.count()} templates d'emails trouvés:")
        for template in templates:
            print(f"   - {template.name} ({template.template_type}) - {'✅ Actif' if template.is_active else '❌ Inactif'}")
        
        # 4. Tester le service d'emails
        print("\n🧪 Test du service d'emails...")
        from notifications.email_service import get_email_service
        service = get_email_service()
        
        if service.settings:
            print(f"✅ Service d'emails configuré:")
            print(f"   - Email expéditeur: {service.settings.from_email}")
            print(f"   - Nom expéditeur: {service.settings.from_name}")
            print(f"   - Statut: {'✅ Actif' if service.settings.is_active else '❌ Inactif'}")
        else:
            print("⚠️ Aucun paramètre email configuré")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du déploiement: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_email_templates():
    """Test des templates d'emails"""
    print("\n🧪 Test des templates d'emails...")
    
    try:
        from notifications.models import EmailTemplate
        
        # Vérifier tous les types de templates requis
        required_templates = [
            'order_confirmation',
            'payment_confirmation', 
            'order_shipped',
            'order_delivered',
            'cart_reminder',
            'stock_alert'
        ]
        
        missing_templates = []
        for template_type in required_templates:
            template = EmailTemplate.objects.filter(
                template_type=template_type,
                is_active=True
            ).first()
            
            if template:
                print(f"✅ {template_type}: {template.name}")
            else:
                print(f"❌ {template_type}: Template manquant")
                missing_templates.append(template_type)
        
        if missing_templates:
            print(f"\n⚠️ Templates manquants: {', '.join(missing_templates)}")
            return False
        else:
            print("\n🎉 Tous les templates sont présents et actifs!")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("📧 Déploiement des templates d'emails sur le VPS")
    print("=" * 60)
    
    # Déployer les templates
    deploy_success = deploy_email_templates()
    
    if deploy_success:
        # Tester les templates
        test_success = test_email_templates()
        
        if test_success:
            print("\n🎉 DÉPLOIEMENT RÉUSSI!")
            print("✅ Les templates d'emails sont maintenant disponibles sur le VPS")
            print("📧 Vous pouvez maintenant tester l'envoi d'emails")
        else:
            print("\n⚠️ Déploiement partiel")
            print("❌ Certains templates sont manquants")
    else:
        print("\n💥 ÉCHEC DU DÉPLOIEMENT")
        print("❌ Impossible de déployer les templates")
    
    return deploy_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
