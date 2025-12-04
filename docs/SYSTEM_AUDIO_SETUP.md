# System Audio Capture Setup for Audio.TUI

This guide will help you set up system audio capture so the visualizer can display audio from web browsers, Spotify, or any other application.

## macOS Setup

### Option 1: BlackHole (Recommended - Free)
BlackHole is a modern, free virtual audio driver for macOS.

1. **Install BlackHole:**
   ```bash
   brew install blackhole-2ch
   ```
   Or download from: https://existential.audio/blackhole/

2. **Create Multi-Output Device:**
   - Open **Audio MIDI Setup** (Applications > Utilities > Audio MIDI Setup)
   - Click the **+** button at bottom left
   - Select **Create Multi-Output Device**
   - Check both:
     - Your speakers/headphones (e.g., "MacBook Pro Speakers")
     - BlackHole 2ch
   - Right-click the Multi-Output Device and select "Use This Device For Sound Output"

3. **Run Audio.TUI:**
   - Start the app: `python app.py`
   - Press **`m`** to switch to System Audio mode
   - Press **`i`** to cycle input devices until you see "BlackHole 2ch"
   - Press **`]`** multiple times to increase sensitivity (try 5-10x)
   - Play audio from any app - the visualizer should now react!

### Option 2: Soundflower (Legacy)
If you prefer Soundflower:

1. Install from: https://github.com/mattingalls/Soundflower/releases
2. Follow similar steps as BlackHole above

### Option 3: Loopback (Paid - Most Powerful)
Rogue Amoeba's Loopback ($99) offers the most control:
- Download from: https://rogueamoeba.com/loopback/
- Create a virtual device that captures system audio
- Select it in Audio.TUI with **`i`**

## Linux Setup

### Using PulseAudio
1. **Install pavucontrol:**
   ```bash
   sudo apt install pavucontrol  # Debian/Ubuntu
   sudo dnf install pavucontrol  # Fedora
   ```

2. **Create Loopback:**
   ```bash
   pactl load-module module-loopback latency_msec=1
   ```

3. **In Audio.TUI:**
   - Press **`m`** for System Audio mode
   - Press **`i`** to select "Monitor of [your output]"

### Using PipeWire
PipeWire automatically provides monitor devices:
- Press **`m`** in Audio.TUI
- Press **`i`** to cycle to your output's monitor device

## Windows Setup

### Using VB-Audio Virtual Cable
1. Download from: https://vb-audio.com/Cable/
2. Install VB-CABLE Driver
3. Set VB-Cable as default playback device in Windows Sound settings
4. In Audio.TUI:
   - Press **`m`** for System Audio mode
   - Press **`i`** to select "VB-Cable"

## Troubleshooting

### No Visualization
- **Increase Sensitivity:** Press **`]`** multiple times (try 10-20x)
- **Check Input Device:** Press **`i`** to cycle through devices
- **Verify Audio is Playing:** Make sure audio is actually playing from another app

### Choppy/Laggy Visualization
- **Decrease Sensitivity:** Press **`[`**
- **Close Other Apps:** Free up CPU resources
- **Check Sample Rate:** Ensure your audio device is set to 44.1kHz or 48kHz

### No Audio Output (when using loopback)
- Make sure you created a **Multi-Output Device** (macOS) or enabled loopback (Linux)
- Don't just set the virtual device as output - you won't hear anything!

## Quick Reference
- **`m`** - Toggle between File Player and System Audio mode
- **`i`** - Cycle through available input devices
- **`]`** - Increase sensitivity (boost visualization)
- **`[`** - Decrease sensitivity
- **`v`** - Toggle visualizer on/off

Enjoy visualizing your system audio! 🎵
