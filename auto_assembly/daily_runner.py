#!/usr/bin/env python3
"""
YouTube Assistant - Runner Quotidien
Version avec gestion musique snowfall
"""

import os
import sys
import random
from datetime import datetime

def get_random_snowfall_music():
    """Retourne une musique snowfall aléatoire"""
    music_dir = "assets_library/music"
    if os.path.exists(music_dir):
        music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        if music_files:
            selected = random.choice(music_files)
            print(f"Musique selectionnee: {selected}")
            return os.path.join(music_dir, selected)
    print("Aucune musique snowfall disponible")
    return None

def test_assets():
    """Teste tous les assets disponibles"""
    print("=== TEST ASSETS ===")
    
    # Test musiques
    music_dir = "assets_library/music"
    if os.path.exists(music_dir):
        music_files = os.listdir(music_dir)
        print(f"Musiques snowfall: {len(music_files)}")
        for music in music_files:
            print(f"  🎵 {music}")
    else:
        print("❌ Dossier musique manquant")
        return False
    
    # Test brief
    brief_path = "human_input/daily_brief.txt"
    if os.path.exists(brief_path):
        with open(brief_path, 'r') as f:
            brief = f.read().strip()
        print(f"Brief: {brief}")
        return True
    else:
        print("❌ Brief quotidien manquant")
        return False

def main():
    print("YouTube Assistant - Systeme Snowfall")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test assets
    if not test_assets():
        return False
    
    # Selection musique pour aujourd'hui
    musique_du_jour = get_random_snowfall_music()
    if musique_du_jour:
        print(f"Musique du jour: {os.path.basename(musique_du_jour)}")
    else:
        print("❌ Erreur selection musique")
        return False
    
    print("✅ Pret pour generation video")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
