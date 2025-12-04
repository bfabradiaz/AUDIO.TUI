from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static
from textual.message import Message
from core.config import Config

class PlayerControls(Container):
    """Player control buttons."""
    
    def compose(self) -> ComposeResult:
        """Create control buttons with labels."""
        with Horizontal(classes="controls"):
            # Previous button
            with Vertical(classes="control-group"):
                yield Button("⏮", id="prev", classes="control-btn")
                yield Static("Prv", classes="control-label")
            
            # Play/Pause button
            with Vertical(classes="control-group"):
                yield Button("⏯", id="play-pause", classes="control-btn")
                yield Static("Ply", classes="control-label")
            
            # Next button
            with Vertical(classes="control-group"):
                yield Button("⏭", id="next", classes="control-btn")
                yield Static("Nxt", classes="control-label")
            
            # Stop button
            with Vertical(classes="control-group"):
                yield Button("⏹", id="stop", classes="control-btn")
                yield Static("Stp", classes="control-label")
            
            # Shuffle button
            with Vertical(classes="control-group"):
                yield Button("🔀", id="shuffle", classes="control-btn")
                yield Static("Shf", classes="control-label")
            
            # Repeat button
            with Vertical(classes="control-group"):
                yield Button("🔁", id="repeat", classes="control-btn")
                yield Static("Rpt", classes="control-label")
        
        # Help section with keyboard shortcuts
        yield Static(
            "Space=Play n=Next p=Prev s=Stop +/-=Vol m=VisMode i=Input []=Sens a=Add o=Folder",
            id="help-text",
            classes="help-section"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        if button_id == "play-pause":
            self.post_message(self.PlayPause())
        elif button_id == "stop":
            self.post_message(self.Stop())
        elif button_id == "next":
            self.post_message(self.NextTrack())
        elif button_id == "prev":
            self.post_message(self.PreviousTrack())
        elif button_id == "shuffle":
            self.post_message(self.ToggleShuffle())
        elif button_id == "repeat":
            self.post_message(self.ToggleRepeat())
    
    class PlayPause(Message):
        """Message sent when play/pause is toggled."""
        def __init__(self) -> None:
            super().__init__()
        
    class Stop(Message):
        """Message sent when stop is pressed."""
        def __init__(self) -> None:
            super().__init__()
        
    class NextTrack(Message):
        """Message sent when next track is requested."""
        def __init__(self) -> None:
            super().__init__()
        
    class PreviousTrack(Message):
        """Message sent when previous track is requested."""
        def __init__(self) -> None:
            super().__init__()
        
    class ToggleShuffle(Message):
        """Message sent when shuffle is toggled."""
        def __init__(self) -> None:
            super().__init__()
        
    class ToggleRepeat(Message):
        """Message sent when repeat is toggled."""
        def __init__(self) -> None:
            super().__init__()
