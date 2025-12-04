from pathlib import Path
from typing import List, Optional

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.events import Click
from textual.message import Message
from textual.widgets import ListView, ListItem, Label
from textual.reactive import reactive

class TrackListItem(ListItem):
    """Custom ListItem that stores the track path."""
    def __init__(self, track_name: str, track_path: str, **kwargs):
        super().__init__(Label(track_name), **kwargs)
        self.track_path = track_path

class Playlist(VerticalScroll):
    """Playlist component showing current queue."""

    BINDINGS = [
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
        ("enter", "select", "Select"),
        ("d", "delete", "Delete"),
        ("a", "add_track", "Add Track"),
    ]

    current_track = reactive("")
    tracks: List[str] = []

    def compose(self) -> ComposeResult:
        """Create playlist view."""
        self.list_view = ListView(id="playlist")
        yield self.list_view

    def add_track(self, path: str) -> None:
        """Add a track to the playlist."""
        if path not in self.tracks:
            self.tracks.append(path)
            track_name = Path(path).stem
            # Create a valid ID from the path
            safe_id = f"track_{len(self.tracks)}"
            self.list_view.append(TrackListItem(track_name, path, id=safe_id))
            
            # If this is the first track, select it
            if len(self.tracks) == 1:
                self.current_track = path
                self.highlight_current_track()

    def set_current_track(self, path: str) -> None:
        """Set the currently playing track."""
        if path in self.tracks:
            self.current_track = path
            self.highlight_current_track()
            self.scroll_to_track(path)

    def highlight_current_track(self) -> None:
        """Highlight the currently playing track in the playlist."""
        if not hasattr(self, 'list_view'):
            return
            
        for item in self.list_view.query("TrackListItem"):
            item.remove_class("current")
            if item.track_path == self.current_track:
                item.add_class("current")

    def scroll_to_track(self, path: str) -> None:
        """Scroll the playlist to make the specified track visible."""
        for i, track in enumerate(self.tracks):
            if track == path:
                self.list_view.index = i
                break

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle track selection."""
        if event.item and isinstance(event.item, TrackListItem):
            self.current_track = event.item.track_path
            self.post_message(self.TrackSelected(self.current_track))

    def action_delete(self) -> None:
        """Delete the currently selected track."""
        if self.list_view.index is None:
            return
        
        # Remove from tracks list
        index = self.list_view.index
        if index < len(self.tracks):
            self.tracks.pop(index)
        
        # Remove from the ListView by clearing and rebuilding
        self.list_view.clear()
        for i, track in enumerate(self.tracks):
            track_name = Path(track).stem
            safe_id = f"track_{i+1}"
            self.list_view.append(TrackListItem(track_name, track, id=safe_id))
                
        # Update current track
        if self.tracks:
            new_index = min(index, len(self.tracks) - 1)
            self.current_track = self.tracks[new_index]
            self.list_view.index = new_index
            self.highlight_current_track()
            # self.post_message(self.TrackSelected(self.current_track)) # Don't auto-play on delete
        else:
            self.current_track = ""

    class TrackSelected(Message):
        """Message sent when a track is selected from the playlist."""
        def __init__(self, track_path: str) -> None:
            self.track_path = track_path
            super().__init__()

    class PlaylistUpdated(Message):
        """Message sent when the playlist is modified."""
        def __init__(self, tracks: List[str]) -> None:
            self.tracks = tracks
            super().__init__()
