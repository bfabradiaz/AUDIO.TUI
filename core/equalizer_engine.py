import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class EQPreset:
    name: str
    gains: List[float]

class EqualizerEngine:
    def __init__(self):
        # Frequency bands (in Hz)
        self.bands = [32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        self.sample_rate = 44100  # Will be updated based on audio
        
        # Default presets
        self.presets = {
            'flat': EQPreset('Flat', [0.0] * 10),
            'pop': EQPreset('Pop', [0.5, 0.3, 0.1, 0.2, 0.4, 0.6, 0.5, 0.3, 0.2, 0.1]),
            'rock': EQPreset('Rock', [0.8, 0.6, 0.4, 0.2, 0.1, 0.0, 0.1, 0.3, 0.5, 0.7]),
            'jazz': EQPreset('Jazz', [0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.0]),
            'classical': EQPreset('Classical', [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.2, 0.1]),
            'bass_boost': EQPreset('Bass Boost', [1.0, 0.8, 0.5, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            'treble_boost': EQPreset('Treble Boost', [0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0]),
            'vocal_boost': EQPreset('Vocal Boost', [0.0, 0.0, 0.0, 0.5, 0.7, 1.0, 0.7, 0.5, 0.0, 0.0]),
        }
        
        self.current_preset = 'flat'
        self.enabled = True
        
    def get_preset_names(self) -> List[str]:
        """Get list of available preset names."""
        return list(self.presets.keys())
        
    def set_preset(self, preset_name: str) -> bool:
        """Set the current EQ preset."""
        if preset_name in self.presets:
            self.current_preset = preset_name
            return True
        return False
        
    def get_current_bands(self) -> List[float]:
        """Get gains for current preset."""
        return self.presets[self.current_preset].gains.copy()
        
    def set_band_gain(self, band: int, gain: float) -> None:
        """Set gain for a specific band."""
        if 0 <= band < len(self.bands):
            self.presets['custom'] = EQPreset('Custom', self.get_current_bands())
            self.presets['custom'].gains[band] = max(-12.0, min(12.0, gain))
            self.current_preset = 'custom'
            
    def process(self, samples: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply EQ to audio samples."""
        if not self.enabled or len(samples) == 0:
            return samples
            
        self.sample_rate = sample_rate
        
        # Convert to frequency domain
        spectrum = np.fft.rfft(samples, axis=0)
        freqs = np.fft.rfftfreq(len(samples), 1.0/sample_rate)
        
        # Create interpolation of gains
        # We need to map freqs to gains based on bands
        # Handle frequencies below first band and above last band
        band_freqs = self.bands
        band_gains_db = self.get_current_bands()
        
        # Interpolate gains for all frequencies
        # Use linear interpolation in dB domain
        gains_db = np.interp(freqs, band_freqs, band_gains_db)
        
        # Convert dB to linear amplitude
        gains_linear = 10 ** (gains_db / 20.0)
        
        # Apply gains (handle stereo/mono)
        if len(samples.shape) > 1:
            # Broadcast gains to all channels
            gains_linear = gains_linear[:, np.newaxis]
            
        spectrum *= gains_linear
            
        # Convert back to time domain
        return np.fft.irfft(spectrum, n=len(samples), axis=0).astype(np.float32)
        
    def toggle(self) -> None:
        """Toggle EQ on/off."""
        self.enabled = not self.enabled
