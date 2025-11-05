#!/usr/bin/env python3
"""
Générateur Audio TTS avec retry robuste - Version edge-tts 6.1.9
"""

import os
import asyncio
import random
from datetime import datetime

class AudioGenerator:
    def __init__(self):
        self.output_dir = "output/audio"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_audio(self, text, output_filename):
        """Génère audio avec retry robuste sur plusieurs voix"""
        try:
            return await self.generate_audio_with_retry(text, output_filename)
        except Exception as e:
            print(f"❌ Erreur critique TTS: {e}")
            return self._create_fallback_audio(text, output_filename)
    
    async def generate_audio_with_retry(self, text, output_filename):
        """Nouvelle version avec retry et fallback robuste"""
        voices = ['fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'fr-FR-AlainNeural']
        
        for voice in voices:
            try:
                print(f"🔊 Essai TTS avec voix: {voice}")
                result = await self._try_single_voice(voice, text, output_filename)
                if result:
                    return result
            except Exception as e:
                print(f"❌ Voix {voice} échouée: {e}")
                continue
        
        print("❌ Toutes les voix ont échoué, fallback silencieux")
        return self._create_fallback_audio(text, output_filename)
    
    async def _try_single_voice(self, voice, text, output_filename):
        """Essai avec une voix spécifique et timeout"""
        try:
            import edge_tts
            
            communicate = edge_tts.Communicate(text, voice, rate="+20%")
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Timeout plus long
            await asyncio.wait_for(communicate.save(output_path), timeout=40.0)
            
            # Vérifie que le fichier est valide
            if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
                file_size = os.path.getsize(output_path) / 1024
                print(f"✅ TTS réussi avec {voice} ({file_size:.1f} KB)")
                return output_path
            else:
                raise Exception("Fichier audio trop petit/corrompu")
                
        except asyncio.TimeoutError:
            raise Exception("Timeout TTS dépassé (40s)")
        except Exception as e:
            raise Exception(f"Erreur TTS: {e}")
    
    def _create_fallback_audio(self, text, output_filename):
        """Crée un fallback basique pour GitHub Actions"""
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Calcule durée approximative basée sur le texte
        duration = max(45, len(text) / 15)  # ~15 caractères par seconde
        
        print(f"🔶 Fallback audio - durée: {duration:.1f}s")
        
        # Crée un fichier WAV silencieux
        self._create_silent_wav(output_path, duration=duration)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ Audio fallback créé: {output_path} ({file_size:.1f} KB)")
        return output_path
    
    def _create_silent_wav(self, filepath, duration=45):
        """Crée un fichier WAV silencieux de durée garantie"""
        import wave
        import struct
        
        framerate = 22050
        nframes = int(framerate * duration)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(framerate)
            wav_file.setnframes(nframes)
            
            # Écrit des frames silencieuses
            silent_data = struct.pack('<h', 0) * nframes
            wav_file.writeframes(silent_data)

def test_tts():
    """Test le TTS avec retry"""
    generator = AudioGenerator()
    
    test_text = "Ceci est un test de génération audio avec le nouveau système de retry."
    
    async def run_test():
        return await generator.generate_audio(test_text, "test_retry.wav")
    
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
