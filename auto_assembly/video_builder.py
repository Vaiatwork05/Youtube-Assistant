#!/usr/bin/env python3
"""
Montage Vidéo avec Pillow pour le texte - Solution fiable GitHub
"""

import os
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip, CompositeAudioClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

class VideoBuilder:
    def __init__(self):
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_text_image(self, text, font_size=70, duration=5):
        """Crée une image avec texte using Pillow"""
        # Crée image noire 1080x1920
        img = Image.new('RGB', (1080, 1920), color='black')
        draw = ImageDraw.Draw(img)
        
        # Essaie différentes polices
        font = None
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            'Arial'
        ]
        
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        # Si aucune police trouvée, utilise la default
        if font is None:
            print("⚠️  Aucune police trouvée, utilisation police système")
            font = ImageFont.load_default()
        
        # Calcule position centrée
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1080 - text_width) // 2
        y = (1920 - text_height) // 2
        
        # Dessine texte en BLANC pour visibilité
        draw.text((x, y), text, fill='white', font=font)
        
        # Convertit en array numpy pour MoviePy
        img_array = np.array(img)
        
        # Crée le clip
        clip = ImageClip(img_array, duration=duration)
        return clip
    
    def create_video(self, audio_path, music_path, output_name):
        """Crée une vidéo avec texte via Pillow"""
        try:
            print(f"🎬 Chargement audio: {os.path.basename(audio_path)}")
            print(f"🎵 Chargement musique: {os.path.basename(music_path)}")
            
            # Charge audio
            voice_audio = AudioFileClip(audio_path)
            background_music = AudioFileClip(music_path)
            
            # Adapte musique
            music_duration = voice_audio.duration
            background_music = background_music.subclip(0, music_duration)
            background_music = background_music.volumex(0.3)
            
            print(f"⏱️ Durée audio: {music_duration:.1f}s")
            
            # Mixe audio
            final_audio = CompositeAudioClip([voice_audio, background_music])
            
            # Crée séquence vidéo
            video_clips = []
            current_time = 0
            
            # Titre (5 premières secondes)
            if music_duration > 5:
                print("🎨 Génération frame titre...")
                title_clip = self.create_text_image("3 RÉVÉLATIONS SURPRENANTES", font_size=70, duration=5)
                video_clips.append(title_clip)
                current_time += 5
            
            # Compte à rebours 3, 2, 1
            remaining_time = music_duration - current_time
            if remaining_time > 6:
                countdown_duration = min(2, remaining_time / 3)
                
                for number in [3, 2, 1]:
                    if remaining_time >= countdown_duration:
                        print(f"🎨 Génération frame {number}...")
                        number_clip = self.create_text_image(str(number), font_size=300, duration=countdown_duration)
                        video_clips.append(number_clip)
                        current_time += countdown_duration
                        remaining_time -= countdown_duration
            
            # Fond noir temps restant
            if remaining_time > 0:
                black_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=remaining_time)
                video_clips.append(black_clip)
            
            # Assemble vidéo
            final_video = CompositeVideoClip(video_clips)
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
    """Test du montage vidéo avec Pillow"""
    builder = VideoBuilder()
    
    test_audio = "output/audio/test_tts.wav"
    test_music = "assets_library/music/snowfall_ambiance_1.mp3"
    
    # Crée un audio test si besoin
    if not os.path.exists(test_audio):
        os.makedirs("output/audio", exist_ok=True)
        open(test_audio, 'wb').close()
    
    if os.path.exists(test_music):
        print("🧪 Test VideoBuilder Pillow...")
        result = builder.create_video(test_audio, test_music, "test_pillow")
        return result
    else:
        print("❌ Musique test manquante")
        return None

if __name__ == "__main__":
    test_video_builder()
