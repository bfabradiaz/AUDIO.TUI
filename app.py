import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import numpy as np

from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.binding import Binding
from textual import work, on, events

# Import our components
from core.audio_engine import AudioEngine
from core.equalizer_engine import EqualizerEngine
from core.visualizer_engine import VisualizerEngine
from core.state import StateManager
from core.config import Config

# Import UI components
from ui.header import Header
from ui.player_controls import PlayerControls
from ui.playlist import Playlist
from ui.visualizer import Visualizer
from ui.equalizer import Equalizer
from ui.status_bar import StatusBar
from ui.file_browser import FileBrowser
from core.media_control import MediaController

class AudioTUI(App):
    """Main application class for Audio.TUI"""

    CSS_PATH = "style.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("space", "play_pause", "Play/Pause"),
        ("s", "stop", "Stop"),
        ("n", "next_track", "Next"),
        ("p", "prev_track", "Previous"),
        ("+", "volume_up", "Volume Up"),
        ("-", "volume_down", "Volume Down"),
        ("l", "seek_forward", "Seek Forward"),
        ("h", "seek_backward", "Seek Backward"),
        ("v", "toggle_visualizer", "Toggle Visualizer"),
        ("m", "toggle_visualizer_mode", "Toggle Vis Mode"),
        ("i", "cycle_input_device", "Cycle Input Device"),
        ("]", "increase_sensitivity", "Sens +"),
        ("[", "decrease_sensitivity", "Sens -"),
        ("a", "add_file", "Add File"),
        ("d", "select_directory", "Select Directory"),
        ("o", "open_folder", "Open Music Folder"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_engine = AudioEngine()
        self.equalizer_engine = EqualizerEngine()
        self.visualizer_engine = VisualizerEngine()
        self.state_manager = StateManager()
        self.media_controller = MediaController()
        self.current_track: Optional[str] = None
        self.playlist: List[str] = []
        self.current_track_index: int = 0
        self.is_playing: bool = False
        self.volume: float = 0.7
        self.show_visualizer: bool = True  

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # Set up the main layout
        yield Header()
        
        with Horizontal(id="main-content"):
            # Left sidebar with playlist
            with Vertical(id="sidebar", classes="panel"):
                yield Playlist()
            
            # Main content area
            with Vertical(id="content"):
                # Always show visualizer and equalizer
                yield Visualizer()
                yield Equalizer(equalizer_engine=self.equalizer_engine)
        
        # Bottom controls and status
        yield PlayerControls()
        yield StatusBar()

    def on_mount(self) -> None:
        """Called when app starts."""
        self.title = "Audio.TUI"
        self.sub_title = "Terminal Music Player"
        self.set_interval(1/30, self.update_ui)
        
        # Connect equalizer to audio engine
        self.audio_engine.set_equalizer(self.equalizer_engine)
        
        # Load initial state
        self.load_state()
        
        # Set initial volume
        self.audio_engine.set_volume(self.volume)
        
        # Start with focus on playlist
        self.query_one(Playlist).focus()

    def load_state(self) -> None:
        """Load application state from disk."""
        state = self.state_manager.state
        self.volume = state.volume
        self.playlist = state.playlist
        self.current_track_index = state.current_track_index
        self.equalizer_engine.set_preset(state.equalizer_preset)
        
        # Load playlist into UI
        playlist = self.query_one(Playlist)
        for track in self.playlist:
            playlist.add_track(track)
        
        # Restore last played track and position
        if self.playlist and 0 <= self.current_track_index < len(self.playlist):
            track_path = self.playlist[self.current_track_index]
            if Path(track_path).exists():
                self.load_track(track_path)
                # Seek to saved position
                if state.current_position > 0:
                    self.audio_engine.seek(state.current_position)
                    self.query_one(Header).update_status(f"Resumed: {Path(track_path).name} at {int(state.current_position)}s")

    def save_state(self) -> None:
        """Save current state to disk."""
        self.state_manager.state.volume = self.volume
        self.state_manager.state.playlist = self.playlist
        self.state_manager.state.current_track_index = self.current_track_index
        self.state_manager.state.equalizer_preset = self.equalizer_engine.current_preset or "flat"
        self.state_manager.state.current_position = self.audio_engine.get_current_time()
        self.state_manager.save()

    def load_track(self, file_path: str) -> None:
        """Load a track into the audio engine."""
        try:
            if self.audio_engine.load_file(Path(file_path)):
                self.current_track = file_path
                self.query_one(Header).update_status(f"Loaded: {Path(file_path).name}")
                
                # Update playlist highlighting
                playlist = self.query_one(Playlist)
                playlist.set_current_track(file_path)
                
                # Auto-play if already playing
                if self.is_playing:
                    self.audio_engine.play()
        except Exception as e:
            self.query_one(Header).update_status(f"Error loading track: {e}")

    def play_pause(self) -> None:
        """Toggle play/pause."""
        try:
            if not self.current_track and self.playlist:
                # Load the first track if none is loaded
                self.load_track(self.playlist[0])
            
            if self.current_track:
                if self.is_playing:
                    self.audio_engine.pause()
                    self.is_playing = False
                    self.query_one(Header).update_status("Paused")
                else:
                    # Try to load the track if not loaded
                    if not self.audio_engine.audio_data:
                        self.load_track(self.current_track)
                    
                    # Set up visualizer callback
                    self.audio_engine.callback = self.visualizer_callback
                    self.audio_engine.play()
                    self.is_playing = True
                    self.query_one(Header).update_status(f"Playing: {Path(self.current_track).name}")
            else:
                self.query_one(Header).update_status("No track selected")
        except Exception as e:
            self.query_one(Header).update_status(f"Error playing: {e}")
            print(f"Play/pause error: {e}")
            self.is_playing = not self.is_playing

    def visualizer_callback(self, chunk: np.ndarray) -> None:
        """Callback for audio data to feed visualizer."""
        try:
            # Update visualizer with real audio data
            visualizer = self.query_one(Visualizer)
            visualizer.update_visualization(chunk)
        except:
            pass  # Visualizer might not be ready

    def stop(self) -> None:
        """Stop playback."""
        self.audio_engine.stop()
        self.is_playing = False

    def next_track(self) -> None:
        """Play next track in playlist."""
        if not self.playlist:
            return
            
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.load_track(self.playlist[self.current_track_index])
        if not self.is_playing:
            self.play_pause()

    def prev_track(self) -> None:
        """Play previous track in playlist."""
        if not self.playlist:
            return
            
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.load_track(self.playlist[self.current_track_index])
        if not self.is_playing:
            self.play_pause()

    def update_ui(self) -> None:
        """Update UI elements with current state."""
        if not hasattr(self, "query_one"):
            return
            
        # Update status bar
        status_bar = self.query_one(StatusBar)
        if self.current_track:
            current_time = self.audio_engine.get_current_time()
            duration = self.audio_engine.get_duration()
            status_bar.update_progress(current_time, duration)
            
            # Update visualizer if visible
            if self.show_visualizer:
                # Get audio data for visualization
                if self.audio_engine.audio_data is not None:
                    samples = self.audio_engine.audio_data.data[
                        self.audio_engine.current_position:
                        min(self.audio_engine.current_position + 1024, 
                            len(self.audio_engine.audio_data.data))
                    ]
                    if samples.size > 0:
                        self.query_one(Visualizer).update_visualization(samples)
        
        # Update volume display
        status_bar.update_volume(self.volume)

    # Message Handlers
    @on(Playlist.TrackSelected)
    def on_track_selected(self, message: Playlist.TrackSelected) -> None:
        """Handle track selection from playlist."""
        self.load_track(message.track_path)
        if not self.is_playing:
            self.play_pause()

    @on(PlayerControls.PlayPause)
    def on_play_pause(self) -> None:
        try:
            if self.query_one(Visualizer).mode == "system":
                self.media_controller.play_pause()
            else:
                self.play_pause()
        except Exception as e:
            self.query_one(Header).update_status(f"System control error: {e}")
            self.play_pause()

    @on(PlayerControls.Stop)
    def on_stop(self) -> None:
        self.stop()

    @on(PlayerControls.NextTrack)
    def on_next_track(self) -> None:
        try:
            if self.query_one(Visualizer).mode == "system":
                self.media_controller.next_track()
            else:
                self.next_track()
        except Exception as e:
            self.query_one(Header).update_status(f"System control error: {e}")
            self.next_track()

    @on(PlayerControls.PreviousTrack)
    def on_prev_track(self) -> None:
        try:
            if self.query_one(Visualizer).mode == "system":
                self.media_controller.prev_track()
            else:
                self.prev_track()
        except Exception as e:
            self.query_one(Header).update_status(f"System control error: {e}")
            self.prev_track()

    @on(PlayerControls.ToggleShuffle)
    def on_toggle_shuffle(self) -> None:
        self.state_manager.toggle_shuffle()
        # Update UI to reflect shuffle state (not implemented in UI yet)

    @on(PlayerControls.ToggleRepeat)
    def on_toggle_repeat(self) -> None:
        self.state_manager.toggle_repeat()
        # Update UI to reflect repeat state (not implemented in UI yet)

    @on(StatusBar.ProgressBarClicked)
    def on_progress_bar_clicked(self, message: StatusBar.ProgressBarClicked) -> None:
        """Handle progress bar click."""
        duration = self.audio_engine.get_duration()
        if duration > 0:
            seek_time = duration * message.progress
            self.audio_engine.seek(seek_time)

    # Action handlers
    def action_play_pause(self) -> None:
        self.play_pause()

    def action_stop(self) -> None:
        self.stop()

    def action_next_track(self) -> None:
        self.next_track()

    def action_prev_track(self) -> None:
        self.prev_track()

    def action_volume_up(self) -> None:
        self.volume = min(1.0, self.volume + 0.05)
        self.audio_engine.set_volume(self.volume)

    def action_volume_down(self) -> None:
        self.volume = max(0.0, self.volume - 0.05)
        self.audio_engine.set_volume(self.volume)

    def action_seek_forward(self) -> None:
        if self.current_track:
            current = self.audio_engine.get_current_time()
            duration = self.audio_engine.get_duration()
            self.audio_engine.seek(min(current + 5, duration))

    def action_seek_backward(self) -> None:
        if self.current_track:
            current = self.audio_engine.get_current_time()
            self.audio_engine.seek(max(0, current - 5))

    def action_add_file(self) -> None:
        """Add a single audio file to the playlist."""
        self.push_screen(FileBrowser(start_path=str(Path.home())), self._handle_file_selection)
    
    def _handle_file_selection(self, files: List[str]) -> None:
        """Handle files selected from the browser."""
        if files:
            for file_path in files:
                self.add_track_to_playlist(file_path)
            self.query_one(Header).update_status(f"Added {len(files)} file(s)")
        else:
            self.query_one(Header).update_status("No files selected")

    def action_select_directory(self) -> None:
        """Select a directory and add all audio files from it."""
        self.push_screen(FileBrowser(start_path=str(Path.home())), self._handle_directory_selection)
    
    def _handle_directory_selection(self, files: List[str]) -> None:
        """Handle directory selection - add all audio files from selected path."""
        if files:
            # Get the directory of the first selected file
            if files[0]:
                directory = str(Path(files[0]).parent)
                self._add_files_from_directory(directory)
        else:
            self.query_one(Header).update_status("No directory selected")

    def action_open_folder(self) -> None:
        """Open Music folder specifically."""
        music_path = Path.home() / "Music"
        if music_path.exists():
            self.push_screen(FileBrowser(start_path=str(music_path)), self._handle_file_selection)
        else:
            self.query_one(Header).update_status("Music folder not found")

    def _add_files_from_directory(self, directory: str) -> None:
        """Add all audio files from a directory."""
        import os
        
        added = 0
        for file in os.listdir(directory):
            if file.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg')):
                full_path = os.path.join(directory, file)
                self.add_track_to_playlist(full_path)
                added += 1
        
        if added == 0:
            self.query_one(Header).update_status(f"No audio files found in {directory}")
        else:
            self.query_one(Header).update_status(f"Added {added} files from {directory}")

    def add_track_to_playlist(self, file_path: str) -> None:
        """Add a track to the playlist."""
        if file_path not in self.playlist:
            self.playlist.append(file_path)
            playlist_ui = self.query_one(Playlist)
            playlist_ui.add_track(file_path)
            self.state_manager.add_to_playlist(file_path)
            # Don't auto-load, just add to playlist

    def action_toggle_visualizer(self) -> None:
        self.show_visualizer = not self.show_visualizer
        visualizer = self.query_one(Visualizer)
        visualizer.display = self.show_visualizer

    def action_toggle_visualizer_mode(self) -> None:
        """Toggle visualizer input mode."""
        self.query_one(Visualizer).toggle_mode()

    def action_cycle_input_device(self) -> None:
        """Cycle visualizer input device."""
        self.query_one(Visualizer).cycle_input_device()

    def action_increase_sensitivity(self) -> None:
        """Increase visualizer sensitivity."""
        self.query_one(Visualizer).adjust_sensitivity(0.5)

    def action_decrease_sensitivity(self) -> None:
        """Decrease visualizer sensitivity."""
        self.query_one(Visualizer).adjust_sensitivity(-0.5)

    def on_unmount(self) -> None:
        """Called when app is closing."""
        self.save_state()
        self.audio_engine.cleanup()

def main():
    """Entry point for the application."""
    app = AudioTUI()
    app.run()

if __name__ == "__main__":
    main()
