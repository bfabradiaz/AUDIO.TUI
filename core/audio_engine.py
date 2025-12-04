import os
import numpy as np
from pydub import AudioSegment
import sounddevice as sd
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Any
from .equalizer_engine import EqualizerEngine

@dataclass
class AudioData:
    data: np.ndarray
    channels: int
    sample_rate: int
    sample_width: int

class AudioEngine:
    def __init__(self):
        self.audio_data: Optional[AudioData] = None
        self.stream: Optional[sd.OutputStream] = None
        self.current_position: int = 0
        self.volume: float = 0.7
        self.is_playing: bool = False
        self.callback = None
        self.equalizer: Optional[EqualizerEngine] = None

    def load_file(self, file_path: Path) -> bool:
        try:
            # Load audio file
            ext = file_path.suffix.lower()
            
            if ext == '.mp3':
                audio = AudioSegment.from_mp3(file_path)
            elif ext == '.wav':
                audio = AudioSegment.from_wav(file_path)
            elif ext == '.flac':
                audio = AudioSegment.from_file(file_path, 'flac')
            elif ext in ('.m4a', '.mp4'):
                audio = AudioSegment.from_file(file_path, 'm4a')
            elif ext == '.ogg':
                audio = AudioSegment.from_ogg(file_path)
            else:
                return False

            # Convert to numpy array
            samples = np.array(audio.get_array_of_samples())
            
            # Handle stereo/mono
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
            else:
                # Reshape mono to (N, 1)
                samples = samples.reshape((-1, 1))
            
            self.audio_data = AudioData(
                data=samples,
                channels=audio.channels,
                sample_rate=audio.frame_rate,
                sample_width=audio.sample_width
            )
            
            self.current_position = 0
            return True
            
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False

    def play(self) -> None:
        if not self.audio_data or self.is_playing:
            return
            
        self.is_playing = True
        
        def callback(outdata: np.ndarray, frames: int, time: Any, status: Any) -> None:
            if not self.is_playing or not self.audio_data:
                outdata.fill(0)
                return
                
            start = self.current_position
            end = min(start + frames, len(self.audio_data.data))
            
            if start >= len(self.audio_data.data):
                outdata.fill(0)
                self.stop()
                return
                
            # Get audio chunk and apply volume
            chunk = self.audio_data.data[start:end]
            
            # Apply Equalizer if enabled
            if self.equalizer and self.equalizer.enabled:
                chunk = self.equalizer.process(chunk, self.audio_data.sample_rate)
            
            # Apply volume
            chunk = chunk * self.volume
            
            # Normalize to [-1, 1] range for sounddevice
            if self.audio_data.data.dtype == np.int16:
                chunk = chunk.astype(np.float32) / 32768.0
            elif self.audio_data.data.dtype == np.int32:
                chunk = chunk.astype(np.float32) / 2147483648.0
            else:
                chunk = chunk.astype(np.float32)
            
            # Pad if needed
            if len(chunk) < frames:
                padding = np.zeros((frames - len(chunk), *chunk.shape[1:]))
                chunk = np.vstack((chunk, padding))
                
            outdata[:] = chunk.astype(np.float32)
            self.current_position += frames
            
            # Call visualizer callback if set
            if self.callback:
                self.callback(chunk)
        
        self.stream = sd.OutputStream(
            samplerate=self.audio_data.sample_rate,
            channels=self.audio_data.channels,
            callback=callback,
            finished_callback=self._on_playback_finished
        )
        self.stream.start()

    def pause(self) -> None:
        if self.stream and self.is_playing:
            self.stream.stop()
            self.is_playing = False

    def stop(self) -> None:
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.is_playing = False
        self.current_position = 0

    def seek(self, time_seconds: float) -> None:
        if not self.audio_data:
            return
            
        sample = int(time_seconds * self.audio_data.sample_rate)
        self.current_position = max(0, min(sample, len(self.audio_data.data)))

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))

    def get_current_time(self) -> float:
        if not self.audio_data:
            return 0.0
        return self.current_position / self.audio_data.sample_rate

    def get_duration(self) -> float:
        if not self.audio_data:
            return 0.0
        return len(self.audio_data.data) / self.audio_data.sample_rate

    def set_callback(self, callback) -> None:
        self.callback = callback

    def set_equalizer(self, equalizer: EqualizerEngine) -> None:
        self.equalizer = equalizer

    def _on_playback_finished(self) -> None:
        self.is_playing = False
        self.current_position = 0

    def cleanup(self) -> None:
        self.stop()
        if self.stream:
            self.stream.close()
            self.stream = None
