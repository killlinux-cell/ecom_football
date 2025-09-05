#!/usr/bin/env python
"""
Script pour créer les captures d'écran PWA
"""

from PIL import Image, ImageDraw

def create_screenshots():
    """Crée les captures d'écran pour le manifest PWA"""
    
    # Capture mobile home
    img = Image.new('RGB', (390, 844), '#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([0, 0, 390, 100], fill='#1e3c72')
    draw.text((195, 50), 'Maillots Football', fill='white', anchor='mm')
    
    # Content
    draw.rectangle([20, 120, 370, 300], fill='white', outline='#e9ecef')
    draw.text((195, 210), "Page d'accueil mobile", fill='#1e3c72', anchor='mm')
    
    img.save('static/screenshots/mobile-home.png')
    print('✅ Capture mobile-home créée')
    
    # Capture mobile product
    img = Image.new('RGB', (390, 844), '#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([0, 0, 390, 100], fill='#1e3c72')
    draw.text((195, 50), 'Maillots Football', fill='white', anchor='mm')
    
    # Product card
    draw.rectangle([20, 120, 370, 400], fill='white', outline='#e9ecef')
    draw.text((195, 260), 'Page produit mobile', fill='#1e3c72', anchor='mm')
    
    img.save('static/screenshots/mobile-product.png')
    print('✅ Capture mobile-product créée')
    
    # Capture desktop home
    img = Image.new('RGB', (1280, 720), '#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([0, 0, 1280, 80], fill='#1e3c72')
    draw.text((640, 40), 'Maillots Football - Page d\'accueil desktop', fill='white', anchor='mm')
    
    # Content
    draw.rectangle([50, 120, 1230, 600], fill='white', outline='#e9ecef')
    draw.text((640, 360), 'Page d\'accueil desktop', fill='#1e3c72', anchor='mm')
    
    img.save('static/screenshots/desktop-home.png')
    print('✅ Capture desktop-home créée')

if __name__ == "__main__":
    try:
        create_screenshots()
        print('🎉 Toutes les captures d\'écran ont été créées !')
    except Exception as e:
        print(f'❌ Erreur: {e}')
