#!/usr/bin/env python3
"""
TTS eSpeak seulement - Version fiable GitHub Actions
"""

import os
import json
import subprocess

def generate_audio_espeak(text, output_path):
    """Génère audio avec eSpeak NG"""
    try:
        # Nettoie texte pour shell
        clean_text = text.replace('"', '\\"').replace('`', '\\`')[:100]
        
        cmd = f'espeak-ng -v fr-fr "{clean_text}" --stdout > {output_path}'
        result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"✅ eSpeak TTS réussi: {file_size:.1f} KB")
            return True
        else:
            print(f"❌ eSpeak échoué: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception eSpeak: {e}")
        return False

def create_silent_audio(output_path, duration=45):
    """Crée audio silencieux avec ffmpeg"""
    try:
        cmd = f'ffmpeg -f lavfi -i anullsrc=channel_layout=mono:sample_rate=22050 -t {duration} {output_path} -y -loglevel quiet'
        subprocess.run(cmd, shell=True, timeout=30)
        return True
    except:
        return False

def main():
    print("🔊 Début génération audio eSpeak")
    
    try:
        # Charge script
        with open('selected_script.json', 'r', encoding='utf-8') as f:
            script_data = json.load(f)
        
        text = script_data['content'][:100]  # 100 caractères max
        print(f"📝 Texte: {text}")
        
        # Préparer output
        os.makedirs("output/audio", exist_ok=True)
        output_path = "output/audio/generated_tts.wav"
        
        # Générer avec eSpeak
        if generate_audio_espeak(text, output_path):
            print("🎯 Audio généré avec succès")
            return True
        else:
            print("🔶 Fallback: audio silencieux")
            if create_silent_audio(output_path):
                print("✅ Audio silencieux créé")
                return True
            return False
            
    except Exception as e:
        print(f"💥 Erreur: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
