#!/usr/bin/env python3
"""
TTS 100% gratuit - Festival + eSpeak fallback
"""

import os
import json
import subprocess

class FreeTTSGenerator:
    def __init__(self):
        self.output_dir = "output/audio"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_audio(self, text, output_filename):
        """Génère audio avec solutions 100% gratuites"""
        
        # Essaie Festival d'abord (meilleure qualité)
        output_path = os.path.join(self.output_dir, output_filename)
        
        if self._try_festival(text, output_path):
            print("✅ Audio généré avec Festival TTS")
            return output_path
            
        # Fallback eSpeak
        if self._try_espeak(text, output_path):
            print("✅ Audio généré avec eSpeak TTS")
            return output_path
            
        # Dernier recours: fichier silencieux
        print("❌ TTS gratuit échoué, fallback silencieux")
        return self._create_silent_audio(output_path, duration=30)
    
    def _try_festival(self, text, output_path):
        """Tente Festival TTS"""
        try:
            # Nettoie le texte pour shell
            clean_text = text.replace('"', '\\"').replace('$', '\\$')
            
            cmd = f'echo "{clean_text}" | text2wave -o {output_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            
            return result.returncode == 0 and os.path.exists(output_path)
        except:
            return False
    
    def _try_espeak(self, text, output_path):
        """Tente eSpeak TTS"""
        try:
            clean_text = text.replace('"', '\\"')
            cmd = f'espeak-ng -v fr-fr "{clean_text}" --stdout > {output_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            
            return result.returncode == 0 and os.path.exists(output_path)
        except:
            return False
    
    def _create_silent_audio(self, output_path, duration=30):
        """Crée fichier audio silencieux"""
        try:
            # Utilise ffmpeg pour créer silence
            cmd = f'ffmpeg -f lavfi -i anullsrc=channel_layout=mono:sample_rate=22050 -t {duration} {output_path} -y'
            subprocess.run(cmd, shell=True, capture_output=True)
            return output_path
        except:
            # Fallback basique
            open(output_path, 'wb').close()
            return output_path

def main():
    """Génère audio depuis script"""
    try:
        with open('selected_script.json', 'r', encoding='utf-8') as f:
            script_data = json.load(f)
        
        generator = FreeTTSGenerator()
        text = script_data['content'][:100]  # Texte court
        audio_path = generator.generate_audio(text, "generated_tts.wav")
        
        print(f"📁 Audio généré: {audio_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
