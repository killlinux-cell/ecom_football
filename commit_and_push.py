#!/usr/bin/env python
"""
Script pour commiter et pousser toutes les modifications
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} réussi")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} échoué")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
    return True

def main():
    """Fonction principale"""
    print("🚀 COMMIT ET PUSH DES MODIFICATIONS")
    print("=" * 50)
    
    # 1. Vérifier le statut git
    if not run_command("git status", "Vérification du statut git"):
        return False
    
    # 2. Ajouter tous les fichiers
    if not run_command("git add .", "Ajout de tous les fichiers"):
        return False
    
    # 3. Commiter les modifications
    commit_message = "Déploiement: Emails automatiques + Optimisation mobile + Corrections"
    if not run_command(f'git commit -m "{commit_message}"', "Commit des modifications"):
        return False
    
    # 4. Pousser vers GitHub
    if not run_command("git push origin main", "Push vers GitHub"):
        return False
    
    print("\n🎉 TOUTES LES MODIFICATIONS ONT ÉTÉ POUSSÉES!")
    print("=" * 50)
    print("✅ Fichiers committés")
    print("✅ Modifications poussées vers GitHub")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Connectez-vous à votre VPS")
    print("2. Allez dans le dossier du projet")
    print("3. Exécutez: git pull origin main")
    print("4. Exécutez: ./deploy_vps.sh")
    print("5. Testez le site et les emails")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
