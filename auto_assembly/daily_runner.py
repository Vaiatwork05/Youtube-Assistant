#!/usr/bin/env python3
"""
YouTube Assistant - Runner Complet TTS + Vidéo
"""

import os
import sys
import random
import asyncio
from datetime import datetime

# Import des modules
sys.path.append(os.path.dirname(__file__))
try:
    from audio_generator import AudioGenerator
    from video_builder import VideoBuilder
    MODULES_LOADED = True
except ImportError as e:
    print(f"❌ Modules manquants: {e}")
    MODULES_LOADED = False

def get_random_snowfall_music():
    """Retourne une musique snowfall aléatoire"""
    music_dir = "assets_library/music"
    if os.path.exists(music_dir):
        music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        if music_files:
            selected = random.choice(music_files)
            print(f"🎵 Musique sélectionnée: {selected}")
            return os.path.join(music_dir, selected)
    print("❌ Aucune musique snowfall disponible")
    return None

def get_daily_script():
    """Récupère le script validé"""
    script_path = "human_input/script_approved.txt"
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            script = f.read().strip()
            print(f"📝 Script chargé: {len(script)} caractères")
            return script
    print("❌ Aucun script disponible")
    return None

def validate_assets():
    """Valide tous les assets nécessaires"""
    print("🔍 Validation des assets...")
    
    # Vérification musique
    music_dir = "assets_library/music"
    if not os.path.exists(music_dir):
        print("❌ Dossier musique manquant")
        return False
    
    music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
    if not music_files:
        print("❌ Aucun fichier musique trouvé")
        return False
    
    print(f"✅ Musiques: {len(music_files)} fichiers")
    
    # Vérification script
    script_path = "human_input/script_approved.txt"
    if not os.path.exists(script_path):
        print("❌ Script manquant")
        create_template_script()
        return False
    
    print("✅ Script présent")
    return True

async def generate_audio_content(script):
    """Génère le fichier audio TTS avec le nouveau système"""
    try:
        audio_gen = AudioGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        audio_file = f"voiceover_{timestamp}.wav"
        
        print("🔊 Génération TTS avec retry...")
        audio_path = await audio_gen.generate_audio(script, audio_file)
        
        if audio_path and os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path) / 1024
            print(f"✅ Audio généré: {os.path.basename(audio_path)} ({file_size:.1f} KB)")
            return audio_path
        else:
            print("❌ Échec génération audio")
            return None
            
    except Exception as e:
        print(f"❌ Erreur génération audio: {e}")
        return None

def create_video_content(audio_path, music_path):
    """Crée la vidéo finale"""
    try:
        video_builder = VideoBuilder()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_name = f"video_{timestamp}"
        
        print("🎬 Montage vidéo en cours...")
        video_path = video_builder.create_video(audio_path, music_path, output_name)
        
        if video_path and os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / (1024 * 1024)
            print(f"✅ Vidéo créée: {os.path.basename(video_path)} ({file_size:.1f} MB)")
            return video_path
        else:
            print("❌ Échec montage vidéo")
            return None
            
    except Exception as e:
        print(f"❌ Erreur création vidéo: {e}")
        return None

async def execute_production_pipeline():
    """Exécute le pipeline complet de production"""
    print("🚀 DÉMARRAGE PRODUCTION")
    print("=" * 50)
    
    # 1. Validation assets
    if not validate_assets():
        return False
    
    # 2. Récupération inputs
    music_path = get_random_snowfall_music()
    script = get_daily_script()
    
    if not music_path or not script:
        return False
    
    # 3. Génération audio TTS
    audio_path = await generate_audio_content(script)
    if not audio_path:
        return False
    
    # 4. Montage vidéo
    video_path = create_video_content(audio_path, music_path)
    if not video_path:
        return False
    
    # 5. Rapport final
    print("=" * 50)
    print("🎉 PRODUCTION TERMINÉE AVEC SUCCÈS")
    print(f"📁 Vidéo: {os.path.basename(video_path)}")
    print(f"⏱️  Durée: {datetime.now().strftime('%H:%M:%S')}")
    return True

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

def main():
    """Fonction principale"""
    print("YouTube Assistant - Pipeline Complet")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    
    if not MODULES_LOADED:
        print("❌ Modules non chargés - installation requise")
        return False
    
    try:
        success = asyncio.run(execute_production_pipeline())
        return success
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
