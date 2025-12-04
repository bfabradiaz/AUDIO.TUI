# Quick Start Guide - Audio.TUI

## ✅ Installation Complete!

All necessary software has been installed:
- ✓ Python dependencies (textual, numpy, sounddevice, etc.)
- ✓ BlackHole 2ch (virtual audio driver)

## 🎵 Getting Started

### Step 1: Configure Audio Output (One-time setup)

**You need to create a Multi-Output Device so you can hear audio AND visualize it:**

1. **Open Audio MIDI Setup:**
   ```bash
   open "/System/Applications/Utilities/Audio MIDI Setup.app"
   ```

2. **Create Multi-Output Device:**
   - Click the **+** button at the bottom left
   - Select **"Create Multi-Output Device"**
   
3. **Configure the device:**
   - Check **both** boxes:
     - ☑ Your speakers/headphones (e.g., "MacBook Pro Speakers")
     - ☑ BlackHole 2ch
   
4. **Set as default output:**
   - Right-click on "Multi-Output Device"
   - Select **"Use This Device For Sound Output"**

### Step 2: Run Audio.TUI

```bash
cd /Applications/XAMPP/htdocs/audio.tui
source venv/bin/activate
python app.py
```

### Step 3: Add Music

Press **`a`** to open the file browser and navigate to your music files.

### Step 4: Enable System Audio Visualization

1. Press **`m`** - Switch to System Audio mode
2. Press **`i`** - Cycle until you see "BlackHole 2ch"
3. Press **`]`** - Increase sensitivity (5-10 times)
4. Play music from Spotify, YouTube, or any app!

## 🎹 Keyboard Shortcuts

### Essential Controls
- **Space** - Play/Pause
- **n** - Next track
- **p** - Previous track
- **+/-** - Volume up/down
- **a** - Add files (file browser)
- **q** - Quit

### Visualizer Controls
- **m** - Toggle File/System Audio mode
- **i** - Cycle input devices
- **]** - Increase sensitivity
- **[** - Decrease sensitivity

## 🔧 Troubleshooting

### "No visualization when pressing 'm'"
- Make sure you created the Multi-Output Device
- Press **`i`** to select "BlackHole 2ch"
- Press **`]`** multiple times to boost sensitivity

### "Can't hear audio"
- Check that Multi-Output Device is selected in System Settings > Sound
- Make sure you checked BOTH your speakers AND BlackHole in the Multi-Output Device

### "File browser doesn't open"
- Restart the app: `python app.py`
- Make sure you're running the latest version

## 📚 Full Documentation

- **README.md** - Complete feature list
- **SYSTEM_AUDIO_SETUP.md** - Detailed audio setup for all platforms
- **setup_system_audio.sh** - Interactive setup script

## 🎉 You're All Set!

Enjoy your terminal music player with real-time audio visualization! 🎵
