import pygame
import os
import numpy as np
from settings import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init(44100, -16, 2, 2048)
        self.sounds_dir = 'sounds'
        self.ensure_sounds_directory()
        self.load_sounds()
        
    def ensure_sounds_directory(self):
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
            
    def load_sounds(self):
        self.background_music = os.path.join(self.sounds_dir, 'background.wav')
        if not os.path.exists(self.background_music):
            self.create_8bit_music()
            
        # Sound effects
        self.collect_sound = self.create_collect_sound()
        self.power_up_sound = self.create_power_up_sound()
        self.game_over_sound = self.create_game_over_sound()
        
        # Start background music
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    
    def create_8bit_music(self):
        sample_rate = 44100
        duration = 0.1  # Duration of each note in seconds
        
        def generate_note(freq, duration):
            t = np.linspace(0, duration, int(sample_rate * duration))
            # Basic square wave
            wave = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))
            return wave
        
        # Simple melody sequence (frequencies for a simple 8-bit tune)
        melody = [
            440.00,  # A4
            493.88,  # B4
            523.25,  # C5
            587.33,  # D5
            659.25,  # E5
            587.33,  # D5
            523.25,  # C5
            493.88   # B4
        ]
        
        # Generate the complete melody
        music = np.array([])
        for freq in melody:
            note = generate_note(freq, duration)
            music = np.concatenate([music, note])
        
        # Convert to 16-bit integers
        music = (music * 32767).astype(np.int16)
        
        # Save as stereo
        stereo = np.ascontiguousarray(np.vstack((music, music)).T)
        
        # Save as WAV file
        from scipy.io import wavfile
        wavfile.write(self.background_music, sample_rate, stereo)
    
    def create_sound_effect(self, duration, freq_start, freq_end=None):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        if freq_end is None:
            freq_end = freq_start
        freq = np.linspace(freq_start, freq_end, len(t))
        wave = 0.4 * np.sign(np.sin(2 * np.pi * freq * t))
        sound_array = (wave * 32767).astype(np.int16)
        # Ensure the array is C-contiguous
        stereo = np.ascontiguousarray(np.vstack((sound_array, sound_array)).T)
        return pygame.sndarray.make_sound(stereo)
    
    def create_collect_sound(self):
        sound = self.create_sound_effect(0.1, 800)
        sound.set_volume(EFFECT_VOLUME)
        return sound
    
    def create_power_up_sound(self):
        sound = self.create_sound_effect(0.15, 400, 1000)
        sound.set_volume(EFFECT_VOLUME)
        return sound
    
    def create_game_over_sound(self):
        sound = self.create_sound_effect(0.5, 800, 200)
        sound.set_volume(EFFECT_VOLUME)
        return sound
    
    def play_collect_sound(self):
        self.collect_sound.play()
    
    def play_power_up_sound(self):
        self.power_up_sound.play()
    
    def play_game_over_sound(self):
        self.game_over_sound.play()