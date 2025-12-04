import json
import os
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Dict, Optional, Any

@dataclass
class State:
    """Represents the application state."""
    current_track: Optional[str] = None
    current_position: float = 0.0
    is_playing: bool = False
    volume: float = 0.7
    is_muted: bool = False
    repeat: bool = False
    shuffle: bool = False
    playlist: List[str] = field(default_factory=list)
    current_track_index: int = -1
    equalizer_preset: str = "Default"
    equalizer_bands: Dict[str, float] = field(default_factory=lambda: {str(i): 0.0 for i in range(10)})
    theme: str = "dark"
    last_played: List[str] = field(default_factory=list)
    favorites: List[str] = field(default_factory=list)

class StateManager:
    """Manages loading and saving application state."""
    
    def __init__(self, state_file: str = None):
        """Initialize the state manager.
        
        Args:
            state_file: Path to the state file. If None, uses default location.
        """
        if state_file is None:
            # Default location: ~/.config/audio-tui/state.json
            config_dir = os.path.expanduser("~/.config/audio-tui")
            os.makedirs(config_dir, exist_ok=True)
            state_file = os.path.join(config_dir, "state.json")
            
        self.state_file = Path(state_file)
        self.state = State()
        self.load()
    
    def load(self) -> None:
        """Load state from file if it exists."""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self.state, key):
                            setattr(self.state, key, value)
        except Exception as e:
            print(f"Warning: Could not load state: {e}")
    
    def save(self) -> None:
        """Save current state to file."""
        try:
            # Ensure directory exists
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert state to dict and save
            state_dict = asdict(self.state)
            with open(self.state_file, 'w') as f:
                json.dump(state_dict, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save state: {e}")
    
    def update(self, **kwargs) -> None:
        """Update state with given key-value pairs and save."""
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
        self.save()
    
    def add_to_playlist(self, file_path: str) -> None:
        """Add a file to the playlist if it's not already there."""
        if file_path not in self.state.playlist:
            self.state.playlist.append(file_path)
            self.save()
    
    def remove_from_playlist(self, file_path: str) -> None:
        """Remove a file from the playlist."""
        if file_path in self.state.playlist:
            self.state.playlist.remove(file_path)
            # Adjust current track index if needed
            if self.state.current_track_index >= len(self.state.playlist):
                self.state.current_track_index = len(self.state.playlist) - 1
            self.save()
    
    def add_to_favorites(self, file_path: str) -> None:
        """Add a track to favorites."""
        if file_path not in self.state.favorites:
            self.state.favorites.append(file_path)
            self.save()
    
    def remove_from_favorites(self, file_path: str) -> None:
        """Remove a track from favorites."""
        if file_path in self.state.favorites:
            self.state.favorites.remove(file_path)
            self.save()
    
    def set_equalizer_band(self, band: int, value: float) -> None:
        """Set equalizer band value."""
        band_str = str(band)
        if band_str in self.state.equalizer_bands:
            self.state.equalizer_bands[band_str] = max(-1.0, min(1.0, value))
            self.save()
    
    def set_equalizer_preset(self, preset_name: str, bands: Dict[int, float]) -> None:
        """Set equalizer preset."""
        self.state.equalizer_preset = preset_name
        for band, value in bands.items():
            self.set_equalizer_band(band, value)
    
    def next_track(self) -> Optional[str]:
        """Move to the next track in the playlist."""
        if not self.state.playlist:
            return None
            
        if self.state.shuffle:
            import random
            self.state.current_track_index = random.randint(0, len(self.state.playlist) - 1)
        else:
            self.state.current_track_index = (self.state.current_track_index + 1) % len(self.state.playlist)
            
        self.state.current_track = self.state.playlist[self.state.current_track_index]
        self.state.current_position = 0.0
        self.save()
        return self.state.current_track
    
    def previous_track(self) -> Optional[str]:
        """Move to the previous track in the playlist."""
        if not self.state.playlist:
            return None
            
        if self.state.shuffle:
            import random
            self.state.current_track_index = random.randint(0, len(self.state.playlist) - 1)
        else:
            self.state.current_track_index = (self.state.current_track_index - 1) % len(self.state.playlist)
            
        self.state.current_track = self.state.playlist[self.state.current_track_index]
        self.state.current_position = 0.0
        self.save()
        return self.state.current_track
    
    def toggle_play_pause(self) -> bool:
        """Toggle play/pause state."""
        self.state.is_playing = not self.state.is_playing
        self.save()
        return self.state.is_playing
    
    def toggle_mute(self) -> bool:
        """Toggle mute state."""
        self.state.is_muted = not self.state.is_muted
        self.save()
        return self.state.is_muted
    
    def toggle_repeat(self) -> bool:
        """Toggle repeat mode."""
        self.state.repeat = not self.state.repeat
        self.save()
        return self.state.repeat
    
    def toggle_shuffle(self) -> bool:
        """Toggle shuffle mode."""
        self.state.shuffle = not self.state.shuffle
        self.save()
        return self.state.shuffle
    
    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)."""
        self.state.volume = max(0.0, min(1.0, volume))
        self.save()
    
    def set_position(self, position: float) -> None:
        """Set playback position in seconds."""
        self.state.current_position = max(0.0, position)
        self.save()
    
    def set_theme(self, theme_name: str) -> None:
        """Set the application theme."""
        if theme_name in ["light", "dark"]:
            self.state.theme = theme_name
            self.save()
    
    def get_state(self) -> State:
        """Get the current state object."""
        return self.state
    
    def set_playlist(self, playlist: List[str]) -> None:
        """Set the entire playlist."""
        self.state.playlist = playlist
        self.state.current_track_index = 0 if playlist else -1
        self.state.current_track = playlist[0] if playlist else None
        self.state.current_position = 0.0
        self.save()
    
    def clear_playlist(self) -> None:
        """Clear the current playlist."""
        self.state.playlist = []
        self.state.current_track_index = -1
        self.state.current_track = None
        self.state.current_position = 0.0
        self.save()

# Create a global state manager instance
state_manager = StateManager()
