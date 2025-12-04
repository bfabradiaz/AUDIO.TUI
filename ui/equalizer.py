from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Select, Button
from rich.panel import Panel
from typing import List, Dict, Any

from core.equalizer_engine import EqualizerEngine

class Equalizer(Vertical):
    """Equalizer component with presets and band controls."""

    def __init__(self, equalizer_engine: EqualizerEngine = None, **kwargs):
        super().__init__(**kwargs)
        self.equalizer = equalizer_engine if equalizer_engine else EqualizerEngine()
        self.bands = [1.0] * 10
        self.presets = self.equalizer.get_preset_names()
        self.bands_display = ""
        self._update_bands_display()

    def compose(self) -> ComposeResult:
        """Create equalizer interface."""
        yield Static("Equalizer", classes="eq-title")
        yield Select(
            [(preset, preset) for preset in self.presets],
            prompt="Select preset",
            id="eq-preset"
        )
        # yield Static(self.bands_display, id="bands-display") # Removed to save space
        
        # Band adjustment buttons
        with Horizontal(id="band-controls"):
            for i in range(len(self.bands)):
                with Container(classes="band-control"):
                    # Simplify label to save space (e.g. 1k instead of 1000Hz)
                    freq = self.equalizer.bands[i]
                    label = f"{freq/1000:.0f}k" if freq >= 1000 else str(freq)
                    yield Static(label, classes="band-label")
                    yield Button("-", id=f"band-{i}-down", classes="band-btn")
                    yield Static(f"{self.bands[i]:.1f}", id=f"band-{i}-value")
                    yield Button("+", id=f"band-{i}-up", classes="band-btn")

    def _update_bands_display(self) -> None:
        """Update the visual representation of the equalizer bands."""
        self.bands_display = "\n".join(
            f"{self.equalizer.bands[i]:4}Hz: {'█' * int(band * 10)}"
            for i, band in enumerate(self.bands)
        )

    def set_preset(self, preset_name: str) -> None:
        """Set equalizer preset."""
        if self.equalizer.set_preset(preset_name):
            self.bands = self.equalizer.get_current_bands()
            # self._update_bands_display()
            self._update_band_displays()
            
    def _update_band_displays(self) -> None:
        """Update the numeric display of band values."""
        for i, value in enumerate(self.bands):
            band_value = self.query_one(f"#band-{i}-value", Static)
            if band_value:
                band_value.update(f"{value:.1f}")

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle preset selection change."""
        if event.select.id == "eq-preset":
            self.set_preset(event.value)
            
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle band adjustment button presses."""
        button_id = event.button.id
        if not button_id:
            return
            
        if button_id.endswith("-up") or button_id.endswith("-down"):
            band_index = int(button_id.split("-")[1])
            if band_index < 0 or band_index >= len(self.bands):
                return
                
            # Adjust band value
            if button_id.endswith("-up"):
                self.bands[band_index] = min(2.0, self.bands[band_index] + 0.1)
            else:
                self.bands[band_index] = max(0.0, self.bands[band_index] - 0.1)
                
            # Update display
            self._update_band_displays()
            # self._update_bands_display()
            
            # Apply changes
            self.equalizer.set_band_gain(band_index, (self.bands[band_index] - 1.0) * 12.0)
            
    def on_mount(self) -> None:
        """Set up the equalizer when mounted."""
        self.add_class("equalizer")
        # Set initial preset
        self.set_preset("flat")
