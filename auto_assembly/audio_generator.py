#!/usr/bin/env python3
"""
Générateur Audio TTS pour YouTube Assistant
"""

import os
import edge_tts
import asyncio
from datetime import datetime

class AudioGenerator:
    def __init__(self):
        self.output_dir = "output/audio"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_audio(self, text, output_filename):
        """Génère un fichier audio depuis le texte"""
        try:
            # Configuration voix française
            voice = 'fr-FR-DeniseNeural'
            rate = '+10%'  # Légère accélération
            
            # Génération TTS
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Sauvegarde fichier audio
            await communicate.save(output_path)
            
            print(f"Audio généré: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Erreur génération audio: {e}")
            return None
    
    def clean_text_for_tts(self, text):
        """Nettoie le texte pour le TTS"""
        # Retire les emojis et caractères problématiques
        import re
        cleaned = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        return cleaned

def test_tts():
    """Test basique du TTS"""
    generator = AudioGenerator()
    
    test_text = """
    Bonjour et bienvenue. Aujourd'hui nous allons découvrir 
    trois révélations étonnantes qui vont vous surprendre.
    """
    
    # Test synchrone
    async def run_test():
        result = await generator.generate_audio(
            test_text, 
            "test_tts.wav"
        )
        return result
    
    # Exécution
    try:
        result = asyncio.run(run_test())
        if result:
            print("✅ Test TTS réussi")
        return result
    except Exception as e:
        print(f"❌ Test TTS échoué: {e}")
        return None

if __name__ == "__main__":
    test_tts()
