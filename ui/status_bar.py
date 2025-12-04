from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Static, ProgressBar
from textual.message import Message
from rich.text import Text
from typing import Optional

class StatusBar(Horizontal):
    """Status bar showing current track and playback progress."""
    
    def compose(self) -> ComposeResult:
        """Create status bar components."""
        # Time elapsed
        yield Static("00:00", id="time-elapsed", classes="time-display")
        
        # Progress bar
        yield ProgressBar(
            total=100, 
            show_eta=False, 
            id="progress", 
            classes="progress-bar"
        )
        
        # Time remaining
        yield Static("00:00", id="time-remaining", classes="time-display")
        
        # Volume indicator
        yield Static("Vol: 100%", id="volume", classes="volume-display")

    def update_progress(self, current: float, duration: float) -> None:
        """Update progress bar and time displays."""
        if duration > 0:
            progress = min(current / duration, 1.0)
            progress_bar = self.query_one("#progress", ProgressBar)
            if progress_bar:
                progress_bar.progress = progress * 100
            
            # Update time displays
            elapsed = self.query_one("#time-elapsed", Static)
            remaining = self.query_one("#time-remaining", Static)
            
            if elapsed and remaining:
                elapsed.update(self._format_time(current))
                remaining.update(f"-{self._format_time(duration - current)}")

    def update_volume(self, volume: float) -> None:
        """Update volume display."""
        volume_display = self.query_one("#volume", Static)
        if volume_display:
            volume_display.update(f"Vol: {int(volume * 100)}%")
            
            # Update volume indicator class for styling
            volume_display.remove_class("volume-low")
            volume_display.remove_class("volume-medium")
            volume_display.remove_class("volume-high")
            
            if volume <= 0.3:
                volume_display.add_class("volume-low")
            elif volume <= 0.7:
                volume_display.add_class("volume-medium")
            else:
                volume_display.add_class("volume-high")

    def _format_time(self, seconds: float) -> str:
        """Format seconds as MM:SS."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def on_mount(self) -> None:
        """Set up the status bar when mounted."""
        self.add_class("status-bar")
        
    def on_click(self, event) -> None:
        """Handle clicks on the progress bar."""
        if hasattr(event.control, "id") and event.control.id == "progress":
            # Calculate the position clicked in the progress bar
            progress_bar = self.query_one("#progress", ProgressBar)
            if progress_bar and progress_bar.total > 0:
                # Get the click position relative to the progress bar
                click_x = event.screen_x - progress_bar.region.x
                progress = click_x / progress_bar.size.width
                self.post_message(self.ProgressBarClicked(progress))
    
    class ProgressBarClicked(Message):
        """Message sent when the progress bar is clicked."""
        def __init__(self, progress: float) -> None:
            self.progress = progress
            super().__init__()
