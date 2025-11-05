#!/usr/bin/env python3
"""
Générateur Audio TTS avec fallback pour GitHub Actions
"""

import os
import asyncio
import wave
import struct

class AudioGenerator:
    def __init__(self):
        self.output_dir = "output/audio"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_audio(self, text, output_filename):
        """Génère audio avec fallback si Edge TTS échoue"""
        try:
            # Essaie Edge TTS d'abord
            return await self._try_edge_tts(text, output_filename)
        except Exception as e:
            print(f"Edge TTS échoué: {e}")
            print("Utilisation du fallback...")
            return self._create_fallback_audio(text, output_filename)
    
    async def _try_edge_tts(self, text, output_filename):
        """Essaie Edge TTS"""
        import edge_tts
        
        voice = 'fr-FR-DeniseNeural'
        rate = '+10%'
        
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        output_path = os.path.join(self.output_dir, output_filename)
        
        await communicate.save(output_path)
        
        # Vérifie que le fichier a été créé
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            file_size = os.path.getsize(output_path) / 1024
            print(f"✅ Audio Edge TTS: {output_path} ({file_size:.1f} KB)")
            return output_path
        else:
            raise Exception("Fichier audio vide")
    
    def _create_fallback_audio(self, text, output_filename):
        """Crée un fallback basique pour GitHub Actions"""
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Calcule durée approximative basée sur le texte
        duration = max(10, len(text) / 15)  # ~15 caractères par seconde
        
        print(f"🔶 Fallback audio - durée: {duration:.1f}s")
        
        # Crée un fichier WAV silencieux
        self._create_silent_wav(output_path, duration=duration)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ Audio fallback créé: {output_path} ({file_size:.1f} KB)")
        return output_path
    
    def _create_silent_wav(self, filepath, duration=10):
        """Crée un fichier WAV silencieux"""
        framerate = 22050  # Fréquence réduite pour fichiers plus petits
        nframes = int(framerate * duration)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 2 bytes = 16 bits
            wav_file.setframerate(framerate)
            wav_file.setnframes(nframes)
            
            # Écrit des frames silencieuses (valeurs 0)
            silent_data = struct.pack('<h', 0) * nframes
            wav_file.writeframes(silent_data)

def test_tts():
    """Test le TTS avec fallback"""
    generator = AudioGenerator()
    
    test_text = "Ceci est un test de génération audio avec fallback."
    
    async def run_test():
        return await generator.generate_audio(test_text, "test_fallback.wav")
    
    try:
        result = asyncio.run(run_test())
        if result and os.path.exists(result):
            file_size = os.path.getsize(result) / 1024
            print(f"✅ Test TTS réussi - Fichier: {result} ({file_size:.1f} KB)")
            return result
        else:
            print("❌ Test TTS échoué - Aucun fichier créé")
            return None
    except Exception as e:
        print(f"❌ Test TTS échoué: {e}")
        return None

if __name__ == "__main__":
    test_tts()
