# Troubleshooting Guide - Audio.TUI

## Common Issues and Solutions

### 1. "Invalid number of channels" Error

**Problem:** When pressing 'm' to switch to System Audio mode, you get an error about invalid channels.

**Solution:**
- The app now automatically detects the correct number of channels
- **Restart the app** to load the fix:
  ```bash
  # Press Ctrl+C to stop the app
  python app.py
  ```
- Press **`m`** to switch to System Audio mode
- Press **`i`** to cycle through devices until you find one that works

**Why this happens:** Some audio devices only support mono (1 channel) while others support stereo (2 channels). The app now adapts automatically.

---

### 2. No Visualization in System Audio Mode

**Checklist:**
1. ✓ Created Multi-Output Device in Audio MIDI Setup?
2. ✓ Set Multi-Output Device as system output?
3. ✓ Pressed **`m`** to switch to System Audio mode?
4. ✓ Pressed **`i`** to select "BlackHole 2ch"?
5. ✓ Pressed **`]`** multiple times (5-10x) to increase sensitivity?
6. ✓ Actually playing audio from another app?

**If still not working:**
- Try selecting a different input device with **`i`**
- Increase sensitivity even more with **`]`** (try 20x)
- Check System Settings > Sound > Input - make sure BlackHole is visible

---

### 3. Can't Hear Audio After Setup

**Problem:** After creating Multi-Output Device, no sound from speakers.

**Solution:**
1. Open Audio MIDI Setup
2. Find your Multi-Output Device
3. Make sure **BOTH** boxes are checked:
   - ☑ Your speakers/headphones
   - ☑ BlackHole 2ch
4. Go to System Settings > Sound > Output
5. Select "Multi-Output Device"

**Alternative:** Use BlackHole only for visualization (no speaker output):
- System Settings > Sound > Output > BlackHole 2ch
- You won't hear audio, but visualization will work

---

### 4. File Browser Doesn't Open (Press 'a')

**Problem:** Pressing 'a' doesn't show the file browser.

**Solution:**
- **Restart the app** to load the new file browser feature:
  ```bash
  python app.py
  ```
- Make sure you're running from the correct directory
- Check that `ui/file_browser.py` exists

---

### 5. Mode Toggle ('m') Doesn't Work

**Problem:** Pressing 'm' doesn't change the mode display.

**Solution:**
- This was a bug that's now fixed
- **Restart the app:**
  ```bash
  python app.py
  ```
- Press **`m`** - you should see "Mode: System (Device Name)"
- Press **`m`** again - should switch back to "Mode: File Player"

---

### 6. App Crashes or Freezes

**Quick Fixes:**
1. **Restart the app:**
   ```bash
   # Press Ctrl+C
   python app.py
   ```

2. **Check dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt --upgrade
   ```

3. **Clear state file:**
   ```bash
   rm ~/.config/audio-tui/state.json
   python app.py
   ```

---

### 7. "No audio files found" When Adding Music

**Problem:** Pressing 'a', 'o', or 'd' says no files found.

**Solution:**
- Use the **new file browser** (press 'a')
- Navigate to your music folder using arrow keys
- Press Enter on audio files to add them
- Supported formats: MP3, WAV, FLAC, M4A, OGG, AAC, WMA

---

### 8. Visualizer Shows No Activity During Playback

**For File Playback:**
- Make sure a track is actually playing (press Space)
- Check volume is not at 0 (press +)
- Try a different audio file

**For System Audio:**
- Increase sensitivity: Press **`]`** many times (10-20x)
- Make sure audio is actually playing from another app
- Try cycling input devices with **`i`**

---

### 9. BlackHole Not Showing in Device List

**Problem:** When pressing 'i', BlackHole 2ch doesn't appear.

**Solution:**
1. **Verify BlackHole is installed:**
   ```bash
   ls /Library/Audio/Plug-Ins/HAL/
   ```
   Should show: `BlackHole2ch.driver`

2. **Restart Core Audio:**
   ```bash
   sudo killall coreaudiod
   ```

3. **Check Audio MIDI Setup:**
   - Open Audio MIDI Setup
   - BlackHole 2ch should be listed in devices

4. **Reinstall if needed:**
   ```bash
   brew reinstall blackhole-2ch
   ```

---

### 10. Permission Errors

**Problem:** "Permission denied" when running scripts.

**Solution:**
```bash
chmod +x setup_system_audio.sh
chmod +x configure_audio.sh
```

---

## Getting Help

If none of these solutions work:

1. **Check the logs:**
   - Look for error messages in the terminal where you ran `python app.py`

2. **Restart everything:**
   ```bash
   # Stop the app (Ctrl+C)
   # Restart terminal
   cd /Applications/XAMPP/htdocs/audio.tui
   source venv/bin/activate
   python app.py
   ```

3. **Verify installation:**
   ```bash
   # Check Python version (should be 3.11+)
   python --version
   
   # Check dependencies
   pip list | grep -E "textual|numpy|sounddevice"
   ```

4. **Read documentation:**
   - QUICKSTART.md - Getting started guide
   - SYSTEM_AUDIO_SETUP.md - Detailed audio setup
   - README.md - Full feature list

---

## Quick Reference

### Restart App
```bash
# Press Ctrl+C to stop
python app.py
```

### Reload Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Reset Configuration
```bash
rm ~/.config/audio-tui/state.json
```

### Check BlackHole Status
```bash
system_profiler SPAudioDataType | grep BlackHole
```
