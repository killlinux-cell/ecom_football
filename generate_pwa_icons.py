#!/usr/bin/env python
"""
Script pour générer les icônes PWA à partir d'une image source
"""

import os
from PIL import Image, ImageDraw
import json

def create_pwa_icons():
    """Crée toutes les icônes PWA nécessaires"""
    
    # Créer le dossier icons s'il n'existe pas
    icons_dir = 'static/icons'
    os.makedirs(icons_dir, exist_ok=True)
    
    # Tailles d'icônes requises pour PWA
    icon_sizes = [
        (72, 72),
        (96, 96),
        (128, 128),
        (144, 144),
        (152, 152),
        (192, 192),
        (384, 384),
        (512, 512)
    ]
    
    # Couleurs du thème
    primary_color = '#1e3c72'
    secondary_color = '#2a5298'
    white = '#ffffff'
    
    print("🎨 Génération des icônes PWA...")
    
    for size in icon_sizes:
        width, height = size
        
        # Créer une image avec un fond dégradé
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Créer un fond circulaire avec dégradé
        margin = width // 20
        draw.ellipse([margin, margin, width-margin, height-margin], 
                    fill=primary_color, outline=secondary_color, width=2)
        
        # Ajouter l'icône de football
        ball_size = int(width * 0.6)
        ball_margin = (width - ball_size) // 2
        
        # Dessiner un ballon de football stylisé
        draw.ellipse([ball_margin, ball_margin, ball_margin + ball_size, ball_margin + ball_size], 
                    fill=white, outline=primary_color, width=2)
        
        # Ajouter des détails du ballon
        center_x, center_y = width // 2, height // 2
        detail_size = ball_size // 4
        
        # Lignes du ballon
        for i in range(3):
            y_offset = (i - 1) * detail_size // 2
            draw.line([center_x - detail_size, center_y + y_offset, 
                      center_x + detail_size, center_y + y_offset], 
                     fill=primary_color, width=2)
        
        # Sauvegarder l'icône
        icon_path = os.path.join(icons_dir, f'icon-{width}x{height}.png')
        img.save(icon_path, 'PNG')
        print(f"✅ Icône créée: {icon_path}")
    
    # Créer l'icône de badge pour les notifications
    badge_size = 72
    badge_img = Image.new('RGBA', (badge_size, badge_size), (0, 0, 0, 0))
    badge_draw = ImageDraw.Draw(badge_img)
    
    # Badge circulaire rouge
    badge_draw.ellipse([0, 0, badge_size, badge_size], fill='#dc3545')
    
    # Numéro de notification (exemple)
    badge_draw.text((badge_size//2, badge_size//2), "1", 
                   fill=white, anchor="mm", font_size=badge_size//2)
    
    badge_path = os.path.join(icons_dir, 'badge-72x72.png')
    badge_img.save(badge_path, 'PNG')
    print(f"✅ Badge créé: {badge_path}")
    
    # Créer les icônes de raccourcis
    shortcut_icons = [
        ('shortcut-new.png', 'N', '#28a745'),
        ('shortcut-sale.png', 'S', '#ffc107'),
        ('shortcut-cart.png', 'C', '#17a2b8'),
        ('shortcut-orders.png', 'O', '#6f42c1')
    ]
    
    for filename, letter, color in shortcut_icons:
        shortcut_img = Image.new('RGBA', (96, 96), (0, 0, 0, 0))
        shortcut_draw = ImageDraw.Draw(shortcut_img)
        
        # Fond circulaire
        shortcut_draw.ellipse([8, 8, 88, 88], fill=color)
        
        # Lettre au centre
        shortcut_draw.text((48, 48), letter, fill=white, anchor="mm", font_size=32)
        
        shortcut_path = os.path.join(icons_dir, filename)
        shortcut_img.save(shortcut_path, 'PNG')
        print(f"✅ Raccourci créé: {shortcut_path}")
    
    print("🎉 Toutes les icônes PWA ont été générées avec succès!")

if __name__ == "__main__":
    try:
        create_pwa_icons()
    except ImportError:
        print("❌ Erreur: PIL (Pillow) n'est pas installé.")
        print("Installez-le avec: pip install Pillow")
    except Exception as e:
        print(f"❌ Erreur lors de la génération des icônes: {e}")
