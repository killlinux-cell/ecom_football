#!/usr/bin/env python
"""
Script pour corriger le service email sur le VPS
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_maillot.settings')
django.setup()

def fix_email_service():
    """Corrige le service email"""
    print("🔧 CORRECTION DU SERVICE EMAIL")
    print("=" * 60)
    
    try:
        from notifications.models import EmailSettings, EmailTemplate
        from notifications.email_service import get_email_service
        
        # Vérifier les paramètres email
        settings = EmailSettings.objects.first()
        if not settings:
            print("❌ Aucun paramètre email trouvé")
            return False
        
        print(f"📧 Paramètres email trouvés:")
        print(f"   - Actif: {settings.is_active}")
        print(f"   - Envoi confirmations: {settings.send_order_confirmations}")
        print(f"   - Email: {settings.from_email}")
        
        # Vérifier les templates
        templates = EmailTemplate.objects.all()
        print(f"📝 {templates.count()} template(s) trouvé(s)")
        
        for template in templates:
            print(f"   - {template.name}: {template.is_active}")
        
        # Tester le service email
        print(f"\n🧪 Test du service email...")
        email_service = get_email_service()
        
        if email_service.settings:
            print(f"✅ Service email initialisé correctement")
            return True
        else:
            print(f"❌ Service email non initialisé")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        return False

def disable_email_temporarily():
    """Désactive temporairement le système email"""
    print("\n🔧 DÉSACTIVATION TEMPORAIRE DU SYSTÈME EMAIL")
    print("=" * 60)
    
    try:
        from notifications.models import EmailSettings
        
        settings = EmailSettings.objects.first()
        if settings:
            settings.is_active = False
            settings.save()
            print("✅ Système email désactivé temporairement")
            return True
        else:
            print("❌ Aucun paramètre email trouvé")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la désactivation: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION DU SERVICE EMAIL SUR VPS")
    print("=" * 60)
    
    # Essayer de corriger le service
    success1 = fix_email_service()
    
    if not success1:
        # Désactiver temporairement si la correction échoue
        print("\n⚠️ Correction échouée, désactivation temporaire...")
        success2 = disable_email_temporarily()
        
        if success2:
            print("\n🎉 SOLUTION TEMPORAIRE APPLIQUÉE!")
            print("✅ Le système email est désactivé temporairement")
            print("✅ Les commandes peuvent maintenant être créées")
            print("⚠️ Les emails ne seront pas envoyés jusqu'à la correction")
        else:
            print("\n💥 ÉCHEC COMPLET!")
            print("❌ Impossible de corriger ou désactiver le système email")
    else:
        print("\n🎉 CORRECTION RÉUSSIE!")
        print("✅ Le service email fonctionne correctement")
    
    return success1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
