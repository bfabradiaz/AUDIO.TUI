import numpy as np
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static

from core.visualizer_engine import VisualizerEngine

class Visualizer(Static):
    """Audio visualizer component."""

    def __init__(self, num_bars: int = 32, **kwargs):
        super().__init__(**kwargs)
        self.num_bars = num_bars
        self.visualizer = VisualizerEngine(num_bars=num_bars)
        self.bars = ["│" * 8 for _ in range(num_bars)]
        self.peaks = [0] * num_bars  # Peak hold values
        self.peak_decay = 0.95  # Peak decay rate
        self.rms = 0.0  # RMS level
        self.peak_db = -60.0  # Peak in dB
        self.sample_rate = 44100
        self.frame_count = 0
        self.mode = "file"  # "file" or "system"
        self.input_stream = None
        self.input_devices = []
        self.current_device_index = None
        self.sensitivity = 1.0

    def compose(self) -> ComposeResult:
        """Create visualizer display."""
        yield Container(
            Static("AUDIO VISUALIZER", id="visualizer-title"),
            Static("Mode: File Player | Sens: 1.0x", id="visualizer-mode"),
            Container(
                Static("", id="visualizer-bars"),
                Static("", id="visualizer-peaks"),
                id="visualizer-display"
            ),
            Static("L: [      ] R: [      ]", id="vu-meter"),
            id="visualizer-container"
        )

    def update_visualization(self, samples: np.ndarray) -> None:
        """Update the visualization with new audio samples."""
        if samples.size == 0:
            return
            
        # Process samples through visualizer
        # Apply sensitivity
        processed_samples = samples * self.sensitivity
        state = self.visualizer.process(processed_samples)
        
        # Update bars display with more dynamic values
        bar_heights = []
        for i, (left, right) in enumerate(zip(state.left_channel, state.right_channel)):
            if i < self.num_bars:
                # Use absolute values and scale more aggressively
                amplitude = abs(left + right) * 2  # Increase sensitivity
                height = int(amplitude * 10)  # Scale to 0-10 characters
                height = max(1, min(height, 10))  # Ensure at least 1, max 10
                bar_heights.append(height)
        
        # Fill remaining bars if not enough data
        while len(bar_heights) < self.num_bars:
            bar_heights.append(1)
        
        # Update the display
        bar_lines = []
        for line in range(8, 0, -1):  # 8 lines high
            line_str = ""
            for height in bar_heights:
                if height >= line:
                    line_str += "█ "
                else:
                    line_str += "  "
            bar_lines.append(line_str)

        # Update the UI
        bars_display = "\n".join(bar_lines)
        try:
            bars_widget = self.query_one("#visualizer-bars", Static)
            bars_widget.update(bars_display)
            
            # Update VU Meter
            left_rms = np.sqrt(np.mean(state.left_channel**2)) if len(state.left_channel) > 0 else 0
            right_rms = np.sqrt(np.mean(state.right_channel**2)) if len(state.right_channel) > 0 else 0
            
            # Scale for display (0-10 chars)
            l_len = int(min(left_rms * 20, 10))
            r_len = int(min(right_rms * 20, 10))
            
            l_bar = "█" * l_len + " " * (10 - l_len)
            r_bar = "█" * r_len + " " * (10 - r_len)
            
            vu_widget = self.query_one("#vu-meter", Static)
            vu_widget.update(f"L: [{l_bar}] R: [{r_bar}]")
            
        except:
            pass  # Widget might not be ready yet

    def toggle_mode(self) -> None:
        """Toggle between file player and system audio input."""
        if self.mode == "file":
            self.mode = "system"
            self._update_mode_display()
            self._start_input_stream()
        else:
            self.mode = "file"
            self.sensitivity = 1.0  # Reset sensitivity for file mode
            self._update_mode_display()
            self._stop_input_stream()

    def adjust_sensitivity(self, delta: float) -> None:
        """Adjust visualizer sensitivity."""
        self.sensitivity = max(0.1, min(100.0, self.sensitivity + delta))
        self._update_mode_display()

    def cycle_input_device(self) -> None:
        """Cycle through available input devices."""
        if self.mode != "system":
            return
            
        import sounddevice as sd
        
        # Refresh devices list
        try:
            devices = sd.query_devices()
            self.input_devices = [
                (i, d['name']) 
                for i, d in enumerate(devices) 
                if d['max_input_channels'] > 0
            ]
            
            if not self.input_devices:
                self.query_one("#visualizer-mode", Static).update("No input devices found")
                return
                
            # Cycle index
            if self.current_device_index is None:
                self.current_device_index = self.input_devices[0][0]
            else:
                # Find current index in list
                current_pos = -1
                for i, (idx, _) in enumerate(self.input_devices):
                    if idx == self.current_device_index:
                        current_pos = i
                        break
                
                next_pos = (current_pos + 1) % len(self.input_devices)
                self.current_device_index = self.input_devices[next_pos][0]
            
            # Restart stream with new device
            self._stop_input_stream()
            self._start_input_stream()
            self._update_mode_display()
            
        except Exception as e:
            self.query_one("#visualizer-mode", Static).update(f"Error listing devices: {e}")

    def _update_mode_display(self) -> None:
        """Update the mode display with current device info."""
        sens_str = f" | Sens: {self.sensitivity:.1f}x"
        
        if self.mode == "system":
            import sounddevice as sd
            device_name = "Default"
            if self.current_device_index is not None:
                try:
                    device_info = sd.query_devices(self.current_device_index)
                    device_name = device_info['name']
                except:
                    pass
            self.query_one("#visualizer-mode", Static).update(f"Mode: System ({device_name}) [Press 'i' to cycle]{sens_str}")
        else:
            self.query_one("#visualizer-mode", Static).update(f"Mode: File Player{sens_str}")

    def _start_input_stream(self) -> None:
        """Start listening to system input."""
        import sounddevice as sd
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            # Send data to main thread for visualization
            if hasattr(self, 'app') and self.app and self.app.is_running:
                self.app.call_from_thread(self.update_visualization, indata.copy())

        try:
            # Query device info to get correct channel count
            device_index = self.current_device_index
            if device_index is None:
                device_index = sd.default.device[0]  # Default input device
            
            device_info = sd.query_devices(device_index, 'input')
            max_channels = device_info['max_input_channels']
            
            # Use the device's maximum channels, but prefer stereo (2) if available
            channels = min(2, max_channels) if max_channels > 0 else 1
            
            # Use specific device if selected, otherwise default
            kwargs = {
                'channels': channels,
                'callback': callback,
                'blocksize': 1024,
                'device': device_index
            }
                
            self.input_stream = sd.InputStream(**kwargs)
            self.input_stream.start()
            self._update_mode_display()
        except Exception as e:
            error_msg = str(e)
            if "Invalid number of channels" in error_msg:
                self.query_one("#visualizer-mode", Static).update(f"Error: Device doesn't support stereo. Try another device (press 'i')")
            else:
                self.query_one("#visualizer-mode", Static).update(f"Error: {e}")

    def _stop_input_stream(self) -> None:
        """Stop system input stream."""
        if self.input_stream:
            self.input_stream.stop()
            self.input_stream.close()
            self.input_stream = None

    def on_mount(self) -> None:
        """Set up the visualizer when mounted."""
        self.add_class("visualizer")
        print("Visualizer mounted successfully")

    def on_unmount(self) -> None:
        """Clean up when visualizer is unmounted."""
        self._stop_input_stream()
        print("Visualizer unmounted")
        
    def on_show(self) -> None:
        """Handle visualizer being shown."""
        self.display = True
        print("Visualizer shown")
        
    def on_hide(self) -> None:
        """Handle visualizer being hidden."""
        self.display = False
        print("Visualizer hidden")
