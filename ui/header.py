from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static
from rich.text import Text
from rich.style import Style
from pathlib import Path
from core.config import Config

class Header(Static):
    """Header component displaying the application title and status."""

    def compose(self) -> ComposeResult:
        """Create child widgets of the header."""
        yield Container(
            Static(self._get_ascii_title(), id="title"),
            Static("Press 'a' to add files, 'o' to open folder, Space to play", id="instructions"),
            Static("Stopped", id="status"),
            id="header-container"
        )

    def _get_ascii_title(self) -> Text:
        """Get rainbow styled ASCII art title."""
        # AUDIO.TUI
        ascii_art = """
 █████╗ ██╗   ██╗██████╗ ██╗ ██████╗      ████████╗██╗   ██╗██╗
██╔══██╗██║   ██║██╔══██╗██║██╔═══██╗     ╚══██╔══╝██║   ██║██║
███████║██║   ██║██║  ██║██║██║   ██║        ██║   ██║   ██║██║
██╔══██║██║   ██║██║  ██║██║██║   ██║        ██║   ██║   ██║██║
██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝ ██╗    ██║   ╚██████╔╝██║
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝  ╚═╝    ╚═╝    ╚═════╝ ╚═╝"""
        
        lines = ascii_art.strip().split('\n')
        title = Text()
        
        colors = [
            "#FF0000", "#FF7F00", "#FFFF00", "#00FF00", 
            "#0000FF", "#4B0082", "#9400D3"
        ]
        
        for line in lines:
            width = len(line)
            for i, char in enumerate(line):
                # Calculate color index based on horizontal position
                # Map x position (0 to width) to color index (0 to len(colors))
                if width > 0:
                    color_idx = int((i / width) * len(colors))
                    color_idx = min(color_idx, len(colors) - 1)
                    title.append(char, style=Style(color=colors[color_idx]))
                else:
                    title.append(char)
            title.append("\n")
            
        return title

    def update_status(self, status: str) -> None:
        """Update the status text in the header."""
        self.query_one("#status", Static).update(status)

    def on_mount(self) -> None:
        """Set up the header when mounted."""
        self.add_class("header")
