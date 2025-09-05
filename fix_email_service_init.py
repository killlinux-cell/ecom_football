#!/usr/bin/env python
"""
Script pour corriger l'initialisation du service d'emails
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_email_service_initialization():
    """Corrige l'initialisation du service d'emails"""
    print("🔧 Correction de l'initialisation du service d'emails...")
    
    try:
        # Vérifier si les tables existent
        from django.db import connection
        cursor = connection.cursor()
        
        # Vérifier la table notifications_emailsettings
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='notifications_emailsettings'
        """)
        
        if not cursor.fetchone():
            print("❌ Table notifications_emailsettings n'existe pas")
            print("📋 Exécution des migrations...")
            
            # Exécuter les migrations
            from django.core.management import execute_from_command_line
            execute_from_command_line(['manage.py', 'makemigrations', 'notifications'])
            execute_from_command_line(['manage.py', 'migrate', 'notifications'])
            
            print("✅ Migrations appliquées avec succès")
        else:
            print("✅ Table notifications_emailsettings existe")
        
        # Tester l'initialisation du service
        from notifications.email_service import get_email_service
        service = get_email_service()
        print("✅ Service d'emails initialisé avec succès")
        
        # Tester la récupération des paramètres
        settings = service._get_email_settings()
        if settings:
            print(f"✅ Paramètres email trouvés: {settings.from_email}")
        else:
            print("⚠️ Aucun paramètre email configuré")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_email_service_initialization()
    if success:
        print("\n🎉 Correction terminée avec succès!")
        print("📧 Le service d'emails est maintenant fonctionnel")
    else:
        print("\n💥 Échec de la correction")
        sys.exit(1)
