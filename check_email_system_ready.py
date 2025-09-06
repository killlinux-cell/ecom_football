#!/usr/bin/env python
"""
Script de vérification du système d'emails
Vérifie que tout est prêt pour le déploiement
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def check_email_system_ready():
    """Vérifie que le système d'emails est prêt pour le déploiement"""
    print("📧 VÉRIFICATION DU SYSTÈME D'EMAILS")
    print("=" * 50)
    
    all_ready = True
    
    try:
        from notifications.models import EmailSettings, EmailTemplate, EmailLog
        from notifications.email_service import get_email_service
        
        # 1. Vérifier les modèles
        print("1️⃣ Vérification des modèles...")
        try:
            settings_count = EmailSettings.objects.count()
            templates_count = EmailTemplate.objects.count()
            logs_count = EmailLog.objects.count()
            
            print(f"   ✅ EmailSettings: {settings_count} configuration(s)")
            print(f"   ✅ EmailTemplate: {templates_count} template(s)")
            print(f"   ✅ EmailLog: {logs_count} log(s)")
        except Exception as e:
            print(f"   ❌ Erreur modèles: {str(e)}")
            all_ready = False
        
        # 2. Vérifier les templates
        print("\n2️⃣ Vérification des templates...")
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
            try:
                template = EmailTemplate.objects.get(
                    template_type=template_type,
                    is_active=True
                )
                print(f"   ✅ {template.name} ({template_type})")
            except EmailTemplate.DoesNotExist:
                print(f"   ❌ Template manquant: {template_type}")
                missing_templates.append(template_type)
                all_ready = False
        
        # 3. Vérifier la configuration SMTP
        print("\n3️⃣ Vérification de la configuration SMTP...")
        try:
            settings = EmailSettings.objects.first()
            if settings:
                print(f"   ✅ Configuration trouvée")
                print(f"   📧 Serveur SMTP: {settings.smtp_host}:{settings.smtp_port}")
                print(f"   📧 Email: {settings.smtp_username}")
                print(f"   📧 TLS: {'Activé' if settings.use_tls else 'Désactivé'}")
                print(f"   📧 Système actif: {'Oui' if settings.is_active else 'Non'}")
                
                if not settings.smtp_username or not settings.smtp_password:
                    print(f"   ⚠️  Configuration SMTP incomplète")
                    all_ready = False
            else:
                print(f"   ❌ Aucune configuration SMTP trouvée")
                all_ready = False
        except Exception as e:
            print(f"   ❌ Erreur configuration: {str(e)}")
            all_ready = False
        
        # 4. Vérifier le service email
        print("\n4️⃣ Vérification du service email...")
        try:
            email_service = get_email_service()
            if email_service:
                print(f"   ✅ Service email initialisé")
            else:
                print(f"   ❌ Service email non initialisé")
                all_ready = False
        except Exception as e:
            print(f"   ❌ Erreur service email: {str(e)}")
            all_ready = False
        
        # 5. Vérifier les templates HTML
        print("\n5️⃣ Vérification des templates HTML...")
        try:
            from django.template.loader import get_template
            base_template = get_template('emails/base_email.html')
            print(f"   ✅ Template de base trouvé")
        except Exception as e:
            print(f"   ❌ Template de base manquant: {str(e)}")
            all_ready = False
        
        # 6. Vérifier les URLs
        print("\n6️⃣ Vérification des URLs...")
        try:
            from django.urls import reverse
            reverse('notifications:dashboard_emails')
            reverse('notifications:email_settings')
            print(f"   ✅ URLs configurées")
        except Exception as e:
            print(f"   ❌ URLs manquantes: {str(e)}")
            all_ready = False
        
        # 7. Vérifier les migrations
        print("\n7️⃣ Vérification des migrations...")
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'notifications_%'")
                tables = cursor.fetchall()
                expected_tables = ['notifications_emailsettings', 'notifications_emailtemplate', 'notifications_emaillog']
                
                for table in expected_tables:
                    if (table,) in tables:
                        print(f"   ✅ Table {table} existe")
                    else:
                        print(f"   ❌ Table {table} manquante")
                        all_ready = False
        except Exception as e:
            print(f"   ❌ Erreur vérification tables: {str(e)}")
            all_ready = False
        
        # Résumé final
        print(f"\n📊 RÉSUMÉ DE LA VÉRIFICATION")
        print("=" * 50)
        
        if all_ready:
            print("🎉 SYSTÈME D'EMAILS PRÊT POUR LE DÉPLOIEMENT!")
            print("✅ Tous les composants sont configurés")
            print("✅ Vous pouvez déployer en toute sécurité")
        else:
            print("⚠️  SYSTÈME D'EMAILS NON PRÊT")
            print("❌ Des composants manquent ou sont mal configurés")
            print("🔧 Exécutez les commandes de correction ci-dessous")
        
        # Commandes de correction si nécessaire
        if not all_ready:
            print(f"\n🔧 COMMANDES DE CORRECTION:")
            print("-" * 30)
            
            if missing_templates:
                print("1. Initialiser les templates:")
                print("   python manage.py init_email_templates")
            
            if not settings:
                print("2. Configurer SMTP:")
                print("   python configure_gmail_smtp.py")
            
            print("3. Appliquer les migrations:")
            print("   python manage.py migrate")
            
            print("4. Vérifier à nouveau:")
            print("   python check_email_system_ready.py")
        
        return all_ready
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("📧 VÉRIFICATION DU SYSTÈME D'EMAILS")
    print("=" * 50)
    print("Ce script vérifie que le système d'emails est prêt pour le déploiement")
    print("=" * 50)
    
    # Exécuter la vérification
    is_ready = check_email_system_ready()
    
    if is_ready:
        print(f"\n🚀 PRÊT POUR LE DÉPLOIEMENT!")
        print("=" * 50)
        print("✅ Le système d'emails est entièrement configuré")
        print("✅ Vous pouvez déployer sur le VPS")
        print("✅ Les emails fonctionneront correctement")
    else:
        print(f"\n⚠️  CORRECTIONS NÉCESSAIRES")
        print("=" * 50)
        print("❌ Le système d'emails n'est pas prêt")
        print("🔧 Exécutez les commandes de correction affichées ci-dessus")
    
    return is_ready

if __name__ == "__main__":
    is_ready = main()
    sys.exit(0 if is_ready else 1)
