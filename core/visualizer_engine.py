import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class VisualizerState:
    left_channel: np.ndarray
    right_channel: np.ndarray
    mono_channel: np.ndarray
    sample_rate: int

class VisualizerEngine:
    def __init__(self, num_bars: int = 20, sample_rate: int = 44100):
        self.num_bars = num_bars
        self.sample_rate = sample_rate
        self.history_length = 10
        self.history = []
        
        # Frequency bands for visualization
        self.bands = self._create_frequency_bands()
        
    def _create_frequency_bands(self) -> list:
        """Create frequency bands for visualization."""
        # Logarithmic scale for better frequency distribution
        min_freq = 20  # 20Hz
        max_freq = 20000  # 20kHz
        
        # Create logarithmically spaced frequency bands
        bands = np.logspace(
            np.log10(min_freq), 
            np.log10(max_freq), 
            num=self.num_bars + 1
        )
        
        # Convert to list of tuples (start, end) frequencies
        return [(bands[i], bands[i+1]) for i in range(len(bands)-1)]
    
    def process(self, samples: np.ndarray, sample_rate: Optional[int] = None) -> VisualizerState:
        """Process audio samples and return visualization data."""
        if sample_rate is not None:
            self.sample_rate = sample_rate
            
        if len(samples) == 0 or samples.size == 0:
            # Return empty state if no samples
            empty = np.zeros(self.num_bars)
            return VisualizerState(empty, empty, empty, self.sample_rate)
        
        # Ensure samples is at least 1D
        if samples.ndim == 0:
            samples = np.array([samples])
            
        # Handle different input formats
        if samples.ndim == 1:
            # Mono input - use same data for both channels
            mono = samples.flatten()
            left = right = mono
        elif samples.ndim == 2:
            if samples.shape[1] == 2:
                # Stereo input
                left = samples[:, 0]
                right = samples[:, 1]
                mono = (left + right) / 2
            elif samples.shape[1] == 1:
                # Mono stored as 2D with 1 channel
                mono = samples[:, 0]
                left = right = mono
            else:
                # Multi-channel - take first two
                left = samples[:, 0]
                right = samples[:, 1] if samples.shape[1] > 1 else samples[:, 0]
                mono = (left + right) / 2
        else:
            # Unexpected format - flatten and use as mono
            mono = samples.flatten()
            left = right = mono
            
        # Process each channel
        left_bars = self._process_channel(left)
        right_bars = self._process_channel(right)
        mono_bars = (left_bars + right_bars) / 2
        
        # Update history for smoothing
        self.history.append(mono_bars)
        if len(self.history) > self.history_length:
            self.history.pop(0)
            
        # Apply smoothing using history
        if len(self.history) > 0:
            mono_bars = np.mean(self.history, axis=0)
            
        return VisualizerState(
            left_channel=left_bars,
            right_channel=right_bars,
            mono_channel=mono_bars,
            sample_rate=self.sample_rate
        )
        
    def _process_channel(self, samples: np.ndarray) -> np.ndarray:
        """Process a single audio channel and return frequency bands."""
        # Apply FFT
        fft_data = np.abs(np.fft.rfft(samples))
        freqs = np.fft.rfftfreq(len(samples), 1.0/self.sample_rate)
        
        # Calculate energy in each frequency band
        bands = np.zeros(self.num_bars)
        
        for i, (low, high) in enumerate(self.bands):
            # Find indices in FFT that correspond to this frequency band
            mask = (freqs >= low) & (freqs < high)
            if np.any(mask):
                # Calculate RMS of this frequency band
                bands[i] = np.sqrt(np.mean(fft_data[mask] ** 2))
                
        # Apply log scale and normalize
        bands = 20 * np.log10(bands + 1e-10)  # Add small value to avoid log(0)
        bands = (bands + 60) / 60  # Normalize to 0-1 range (assuming -60dB to 0dB)
        bands = np.clip(bands, 0, 1)  # Clip to [0, 1]
        
        # Apply some smoothing between adjacent bands
        bands = np.convolve(bands, [0.2, 0.6, 0.2], mode='same')
        
        return bands
    
    def reset(self) -> None:
        """Reset the visualizer state."""
        self.history = []
