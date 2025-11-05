#!/usr/bin/env python3
"""
Montage Vidéo pour YouTube Assistant
"""

import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.fx.all import resize
import random

class VideoBuilder:
    def __init__(self):
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_video(self, audio_path, music_path, output_name):
        """Crée une vidéo avec audio TTS et musique d'ambiance"""
        try:
            # Charge les fichiers audio
            voice_audio = AudioFileClip(audio_path)
            background_music = AudioFileClip(music_path)
            
            # Adapte la musique à la durée de la voix
            music_duration = voice_audio.duration
            background_music = background_music.subclip(0, music_duration)
            background_music = background_music.volumex(0.3)  # Réduit le volume
            
            # Mixe les deux pistes audio
            final_audio = CompositeAudioClip([voice_audio, background_music])
            
            # Crée un fond vidéo simple (écran noir avec titre)
            from moviepy.editor import ColorClip
            video_clip = ColorClip(
                size=(1080, 1920),  # Format vertical YouTube Shorts
                color=(0, 0, 0),    # Fond noir
                duration=music_duration
            )
            
            # Ajoute un titre basique
            title = "Révélations Surprenantes"
            txt_clip = TextClip(
                title, 
                fontsize=70, 
                color='white',
                font='Arial-Bold'
            )
            txt_clip = txt_clip.set_position('center').set_duration(5)  # Affiche 5 secondes
            
            # Assemble la vidéo
            final_video = CompositeVideoClip([video_clip, txt_clip])
            final_video = final_video.set_audio(final_audio)
            
            # Export
            output_path = os.path.join(self.output_dir, f"{output_name}.mp4")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            print(f"✅ Vidéo créée: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Erreur création vidéo: {e}")
            return None

def test_video_builder():
    """Test basique du montage vidéo"""
    builder = VideoBuilder()
    
    # Chemins de test (à adapter)
    test_audio = "output/audio/test_tts.wav"
    test_music = "assets_library/music/snowfall_ambiance_1.mp3"
    
    if os.path.exists(test_audio) and os.path.exists(test_music):
        result = builder.create_video(test_audio, test_music, "test_video")
        return result
    else:
        print("❌ Fichiers de test manquants")
        return None

if __name__ == "__main__":
    test_video_builder()
