from pathlib import Path
from typing import List, Optional
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import DirectoryTree, Static, Button
from textual.screen import ModalScreen
from textual.message import Message

class FileBrowser(ModalScreen):
    """A modal file browser for selecting audio files."""
    
    BINDINGS = [
        ("escape", "dismiss", "Cancel"),
        ("enter", "select", "Select"),
    ]
    
    def __init__(self, start_path: str = None, **kwargs):
        super().__init__(**kwargs)
        self.start_path = Path(start_path) if start_path else Path.home()
        self.selected_files: List[str] = []
    
    def compose(self) -> ComposeResult:
        """Create file browser UI."""
        with Vertical(id="file-browser-container"):
            yield Static("Select Audio Files (Enter=Add, Space=Select, Esc=Done)", id="browser-title")
            yield DirectoryTree(str(self.start_path), id="file-tree")
            with Horizontal(id="browser-buttons"):
                yield Button("Add Selected", id="add-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn", variant="default")
            yield Static(f"Selected: 0 files", id="selection-count")
    
    def on_mount(self) -> None:
        """Set up the browser when mounted."""
        self.query_one(DirectoryTree).focus()
    
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection."""
        file_path = str(event.path)
        
        # Check if it's an audio file
        if file_path.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac', '.wma')):
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                self._update_count()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "add-btn":
            self.action_select()
        elif event.button.id == "cancel-btn":
            self.action_dismiss()
    
    def action_select(self) -> None:
        """Add selected files and close."""
        if self.selected_files:
            self.dismiss(self.selected_files)
        else:
            # If no files selected, try to add the currently highlighted file
            tree = self.query_one(DirectoryTree)
            if tree.cursor_node and tree.cursor_node.data:
                path = str(tree.cursor_node.data.path)
                if path.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac', '.wma')):
                    self.dismiss([path])
                else:
                    self.dismiss([])
            else:
                self.dismiss([])
    
    def action_dismiss(self) -> None:
        """Cancel and close."""
        self.dismiss([])
    
    def _update_count(self) -> None:
        """Update the selection count display."""
        count_widget = self.query_one("#selection-count", Static)
        count_widget.update(f"Selected: {len(self.selected_files)} files")
