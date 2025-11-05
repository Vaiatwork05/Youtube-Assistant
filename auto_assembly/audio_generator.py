#!/usr/bin/env python3
"""
TTS 100% gratuit - Festival + eSpeak fallback
Version GitHub Actions
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
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Essaie Festival d'abord
        if self._try_festival(text, output_path):
            print("✅ Audio généré avec Festival TTS")
            return output_path
            
        # Fallback eSpeak
        if self._try_espeak(text, output_path):
            print("✅ Audio généré avec eSpeak TTS")
            return output_path
            
        # Dernier recours
        print("🔶 Fallback: audio silencieux")
        return self._create_silent_audio(output_path)
    
    def _try_festival(self, text, output_path):
        """Tente Festival TTS"""
        try:
            clean_text = text.replace('"', '\\"').replace('$', '\\$')[:100]
            cmd = f'echo "{clean_text}" | text2wave -o {output_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024
                print(f"📊 Festival: {file_size:.1f} KB")
                return True
            return False
        except Exception as e:
            print(f"❌ Festival failed: {e}")
            return False
    
    def _try_espeak(self, text, output_path):
        """Tente eSpeak TTS"""
        try:
            clean_text = text.replace('"', '\\"')[:100]
            cmd = f'espeak-ng -v fr-fr "{clean_text}" --stdout > {output_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024
                print(f"📊 eSpeak: {file_size:.1f} KB")
                return True
            return False
        except Exception as e:
            print(f"❌ eSpeak failed: {e}")
            return False
    
    def _create_silent_audio(self, output_path):
        """Crée fichier audio silencieux"""
        try:
            cmd = f'ffmpeg -f lavfi -i anullsrc=channel_layout=mono:sample_rate=22050 -t 45 {output_path} -y'
            subprocess.run(cmd, shell=True, capture_output=True)
            return output_path
        except:
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
        
        print(f"🎯 Audio final: {audio_path}")
        return True
        
    except Exception as e:
        print(f💥 Erreur: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
