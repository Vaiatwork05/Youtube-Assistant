#!/usr/bin/env python3
"""
Montage Vidéo avec ImageMagick pour le texte
"""

import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, CompositeAudioClip, TextClip

class VideoBuilder:
    def __init__(self):
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_video(self, audio_path, music_path, output_name):
        """Crée une vidéo avec texte via ImageMagick"""
        try:
            print(f"🎬 Chargement audio: {os.path.basename(audio_path)}")
            print(f"🎵 Chargement musique: {os.path.basename(music_path)}")
            
            # Charge les fichiers audio
            voice_audio = AudioFileClip(audio_path)
            background_music = AudioFileClip(music_path)
            
            # Adapte la musique
            music_duration = voice_audio.duration
            background_music = background_music.subclip(0, music_duration)
            background_music = background_music.volumex(0.3)
            
            print(f"⏱️ Durée audio: {music_duration:.1f}s")
            
            # Mixe les pistes audio
            final_audio = CompositeAudioClip([voice_audio, background_music])
            
            # Crée la séquence vidéo avec texte
            video_clips = []
            
            # Titre (5 premières secondes)
            if music_duration > 5:
                title_clip = TextClip(
                    "3 RÉVÉLATIONS SURPRENANTES",
                    fontsize=70,
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=2
                )
                title_clip = title_clip.set_position('center').set_duration(5)
                video_clips.append(title_clip)
            
            # Compte à rebours 3, 2, 1
            remaining_time = music_duration - 5
            countdown_duration = min(2, remaining_time / 3) if remaining_time > 0 else 0
            
            start_time = 5
            for number in [3, 2, 1]:
                if remaining_time >= countdown_duration:
                    number_clip = TextClip(
                        str(number),
                        fontsize=300,
                        color='white',
                        font='Arial-Bold',
                        stroke_color='black', 
                        stroke_width=4
                    )
                    number_clip = number_clip.set_position('center').set_start(start_time).set_duration(countdown_duration)
                    video_clips.append(number_clip)
                    start_time += countdown_duration
                    remaining_time -= countdown_duration
            
            # Fond noir principal
            main_video = ColorClip(
                size=(1080, 1920),
                color=(0, 0, 0),
                duration=music_duration
            )
            
            # Assemble tout
            final_video = CompositeVideoClip([main_video] + video_clips)
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
    """Test du montage vidéo avec ImageMagick"""
    builder = VideoBuilder()
    
    test_audio = "output/audio/voiceover_20251105_1303.wav"
    test_music = "assets_library/music/snowfall_ambiance_1.mp3"
    
    if os.path.exists(test_audio) and os.path.exists(test_music):
        print("🧪 Test VideoBuilder avec ImageMagick...")
        result = builder.create_video(test_audio, test_music, "test_video_imagemagick")
        return result
    else:
        print("❌ Fichiers de test manquants")
        return None

if __name__ == "__main__":
    test_video_builder()
