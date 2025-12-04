from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os

@dataclass
class ColorTheme:
    primary: str
    secondary: str
    accent: str
    background: str
    text: str
    highlight: str

class Config:
    """Application configuration and constants."""
    
    # Color themes
    THEMES = {
        'default': ColorTheme(
            primary='#1DB954',  # Spotify green
            secondary='#191414',  # Spotify black
            accent='#1ED760',  # Brighter green
            background='#121212',  # Dark background
            text='#FFFFFF',  # White text
            highlight='#535353'  # Gray highlight
        ),
        'dark': ColorTheme(
            primary='#BB86FC',  # Purple
            secondary='#121212',
            accent='#03DAC6',  # Teal
            background='#121212',
            text='#E1E1E1',
            highlight='#2A2A2A'
        ),
        'light': ColorTheme(
            primary='#1E88E5',  # Blue
            secondary='#F5F5F5',
            accent='#FF4081',  # Pink
            background='#FAFAFA',
            text='#212121',
            highlight='#E0E0E0'
        )
    }
    
    # Default theme
    current_theme = THEMES['default']
    
    # Audio settings
    SAMPLE_RATE = 44100
    CHANNELS = 2
    CHUNK_SIZE = 1024
    
    # UI settings
    VISUALIZER_BARS = 20
    VISUALIZER_HEIGHT = 10
    
    # Paths
    CONFIG_DIR = Path.home() / '.config' / 'audio-tui'
    STATE_FILE = CONFIG_DIR / 'state.json'
    
    # Create config directory if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    @classmethod
    def get_color(cls, color_name: str) -> str:
        """Get a color from the current theme."""
        return getattr(cls.current_theme, color_name, '#FFFFFF')
    
    @classmethod
    def set_theme(cls, theme_name: str) -> bool:
        """Set the current theme."""
        if theme_name in cls.THEMES:
            cls.current_theme = cls.THEMES[theme_name]
            return True
        return False
    
    @classmethod
    def get_theme_names(cls) -> List[str]:
        """Get available theme names."""
        return list(cls.THEMES.keys())

# Default export
config = Config()
