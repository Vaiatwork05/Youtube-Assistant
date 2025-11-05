#!/usr/bin/env python3
"""
Montage Vidéo pour YouTube Assistant
"""

import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, ColorClip, CompositeAudioClip

class VideoBuilder:
    def __init__(self):
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_video(self, audio_path, music_path, output_name):
        """Crée une vidéo avec audio TTS et musique d'ambiance"""
        try:
            print(f"🎬 Chargement audio: {os.path.basename(audio_path)}")
            print(f"🎵 Chargement musique: {os.path.basename(music_path)}")
            
            # Charge les fichiers audio
            voice_audio = AudioFileClip(audio_path)
            background_music = AudioFileClip(music_path)
            
            # Adapte la musique à la durée de la voix
            music_duration = voice_audio.duration
            background_music = background_music.subclip(0, music_duration)
            background_music = background_music.volumex(0.3)  # Réduit le volume
            
            print(f"⏱️ Durée audio: {music_duration:.1f}s")
            
            # Mixe les deux pistes audio
            final_audio = CompositeAudioClip([voice_audio, background_music])
            
            # Crée un fond vidéo simple (écran noir avec titre)
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
            txt_clip = txt_clip.set_position('center').set_duration(min(5, music_duration))
            
            # Assemble la vidéo
            final_video = CompositeVideoClip([video_clip, txt_clip])
            final_video = final_video.set_audio(final_audio)
            
            # Export
            output_path = os.path.join(self.output_dir, f"{output_name}.mp4")
            print(f"📤 Export vidéo: {output_path}")
            
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Vidéo créée: {output_path} ({file_size:.1f} MB)")
            return output_path
            
        except Exception as e:
            print(f"❌ Erreur création vidéo: {e}")
            import traceback
            traceback.print_exc()
            return None

def test_video_builder():
    """Test basique du montage vidéo"""
    builder = VideoBuilder()
    
    # Chemins de test
    test_audio = "output/audio/voiceover_20251105_1252.wav"  # Fichier existant
    test_music = "assets_library/music/snowfall_ambiance_1.mp3"
    
    if os.path.exists(test_audio) and os.path.exists(test_music):
        print("🧪 Test VideoBuilder...")
        result = builder.create_video(test_audio, test_music, "test_video")
        return result
    else:
        print("❌ Fichiers de test manquants")
        print(f"Audio existe: {os.path.exists(test_audio)}")
        print(f"Musique existe: {os.path.exists(test_music)}")
        return None

if __name__ == "__main__":
    test_video_builder()
