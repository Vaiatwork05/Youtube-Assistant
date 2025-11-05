
#!/usr/bin/env python3
"""
YouTube Assistant - Runner avec TTS
"""

import os
import sys
import random
import asyncio
from datetime import datetime

# Import du nouveau module TTS
sys.path.append(os.path.dirname(__file__))
from audio_generator import AudioGenerator

def get_random_snowfall_music():
    """Retourne une musique snowfall aléatoire"""
    music_dir = "assets_library/music"
    if os.path.exists(music_dir):
        music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        if music_files:
            selected = random.choice(music_files)
            print(f"Musique sélectionnée: {selected}")
            return os.path.join(music_dir, selected)
    print("Aucune musique snowfall disponible")
    return None

def get_daily_script():
    """Récupère le script validé"""
    script_path = "human_input/script_approved.txt"
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

async def generate_daily_content():
    """Génère le contenu audio du jour"""
    print("=== GÉNÉRATION CONTENU QUOTIDIEN ===")
    
    # 1. Récupération inputs
    musique = get_random_snowfall_music()
    script = get_daily_script()
    
    if not script:
        print("❌ Aucun script disponible")
        return False
    
    if not musique:
        print("❌ Aucune musique disponible")
        return False
    
    print(f"Script: {len(script)} caractères")
    print(f"Musique: {os.path.basename(musique)}")
    
    # 2. Génération audio TTS
    audio_gen = AudioGenerator()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    audio_file = f"voiceover_{timestamp}.wav"
    
    print("Génération TTS en cours...")
    audio_path = await audio_gen.generate_audio(script, audio_file)
    
    if not audio_path:
        print("❌ Échec génération audio")
        return False
    
    print(f"✅ Audio généré: {os.path.basename(audio_path)}")
    return True

def main():
    print("YouTube Assistant - Génération TTS")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Vérification assets
    if not os.path.exists("human_input/script_approved.txt"):
        print("❌ Script manquant - création template...")
        create_template_script()
        return False
    
    # Génération contenu
    try:
        success = asyncio.run(generate_daily_content())
        return success
    except Exception as e:
        print(f"❌ Erreur génération: {e}")
        return False

def create_template_script():
    """Crée un template de script si manquant"""
    template = """TITRE: 3 Révélations Surprenantes Aujourd'hui

POINT 1: Une découverte étonnante qui change tout
POINT 2: La vérité cachée derrière les apparences  
POINT 3: Ce que personne ne veut que vous sachiez

CTA: Likez pour la partie 2!
"""
    os.makedirs("human_input", exist_ok=True)
    with open("human_input/script_approved.txt", "w", encoding='utf-8') as f:
        f.write(template)
    print("✅ Template script créé dans human_input/")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
