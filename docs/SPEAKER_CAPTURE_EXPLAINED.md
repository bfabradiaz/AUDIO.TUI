# Speaker Audio Capture - How It Works

## The Problem

You want to visualize audio that's **playing from your speakers** (e.g., Spotify, YouTube), not audio from your microphone.

**Why you're seeing the microphone:**
- By default, macOS only allows apps to access **input** devices (microphones)
- Your speakers are an **output** device
- Apps can't directly capture speaker output for security/privacy reasons

## The Solution: Multi-Output Device

A Multi-Output Device acts as a "splitter" that sends audio to multiple places:

```
┌─────────────────────────────────────────────────────────┐
│                    Your Music App                       │
│                  (Spotify, YouTube, etc.)               │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Multi-Output Device │
              │   (You create this)  │
              └──────────┬───────────┘
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
        ┌──────────────┐  ┌──────────────┐
        │   Speakers   │  │  BlackHole   │
        │  (You hear)  │  │ (App reads)  │
        └──────────────┘  └──────────────┘
                                  │
                                  ▼
                          ┌──────────────┐
                          │  Audio.TUI   │
                          │ (Visualizes) │
                          └──────────────┘
```

## Step-by-Step Setup

### 1. Create Multi-Output Device

**In Audio MIDI Setup:**
1. Click **+** (bottom left)
2. Select **"Create Multi-Output Device"**

### 2. Configure It

**Check BOTH boxes:**
- ☑ **Your Speakers** (e.g., "MacBook Pro Speakers", "External Headphones")
- ☑ **BlackHole 2ch**

**What this does:**
- Audio plays from your speakers → **You can hear it**
- Audio also goes to BlackHole → **App can read it**

### 3. Set as System Output

**Option A - Audio MIDI Setup:**
- Right-click "Multi-Output Device"
- Select "Use This Device For Sound Output"

**Option B - System Settings:**
- System Settings > Sound > Output
- Select "Multi-Output Device"

### 4. Use in Audio.TUI

1. **Press `m`** - Switch to System Audio mode
2. **Press `i`** - Cycle until you see **"BlackHole 2ch"**
   - NOT "Built-in Microphone"
   - NOT "External Microphone"
   - Look for "BlackHole 2ch"
3. **Press `]`** - Increase sensitivity (10-15 times)
4. **Play music** - Visualizer reacts!

## Common Mistakes

### ❌ Selecting Microphone
**Problem:** You're seeing "Built-in Microphone" when pressing `i`

**Why it's wrong:** Microphone captures ambient sound, not speaker output

**Solution:** Keep pressing `i` until you see "BlackHole 2ch"

### ❌ Only Checking BlackHole
**Problem:** You only checked BlackHole in Multi-Output Device

**Why it's wrong:** Audio only goes to BlackHole, not your speakers (no sound!)

**Solution:** Check BOTH your speakers AND BlackHole

### ❌ Not Setting Multi-Output as System Output
**Problem:** Created Multi-Output Device but didn't set it as output

**Why it's wrong:** macOS still uses your regular speakers, BlackHole gets no audio

**Solution:** Set Multi-Output Device as system output (Step 3 above)

## Verification Checklist

Before expecting it to work, verify:

- [ ] BlackHole 2ch is installed (`brew list | grep blackhole`)
- [ ] Multi-Output Device exists in Audio MIDI Setup
- [ ] Both speakers AND BlackHole are checked in Multi-Output Device
- [ ] Multi-Output Device is set as system output
- [ ] Audio.TUI is in System Audio mode (press `m`)
- [ ] BlackHole 2ch is selected as input (press `i`)
- [ ] Sensitivity is increased (press `]` 10+ times)
- [ ] Music is actually playing from another app

## Troubleshooting

### "I don't see BlackHole 2ch when pressing 'i'"

**Possible causes:**
1. Multi-Output Device not set as system output
2. BlackHole not properly installed
3. Need to restart Audio.TUI

**Solutions:**
```bash
# Verify BlackHole is installed
brew list blackhole-2ch

# Restart Core Audio
sudo killall coreaudiod

# Restart Audio.TUI
# Press Ctrl+C, then:
python app.py
```

### "I see BlackHole but no visualization"

**Solutions:**
1. Increase sensitivity more: Press `]` 15-20 times
2. Make sure music is actually playing
3. Check volume is not at 0
4. Try playing louder music

### "No sound from speakers"

**Problem:** You can't hear audio

**Cause:** Multi-Output Device not configured correctly

**Solution:**
1. Open Audio MIDI Setup
2. Click on Multi-Output Device
3. Make sure your speakers are checked
4. Make sure speakers are listed FIRST (drag to reorder)

## Alternative: Direct BlackHole (No Speakers)

If you just want to test visualization without hearing audio:

1. System Settings > Sound > Output
2. Select "BlackHole 2ch" (NOT Multi-Output Device)
3. In Audio.TUI: Press `m`, then `i` to select BlackHole
4. Play music - you won't hear it, but visualizer will work

**Use this for:**
- Testing if BlackHole works
- Silent visualization
- Recording/streaming scenarios

## Quick Reference

### Setup Script
```bash
./setup_speaker_capture.sh
```

### Manual Setup
1. Audio MIDI Setup → Create Multi-Output Device
2. Check: Speakers + BlackHole 2ch
3. Set as system output
4. Audio.TUI: `m` → `i` → `]`

### Key Concept
**Multi-Output Device = Hear audio + Visualize it**
**BlackHole only = Visualize only (no sound)**

---

**Remember:** You're not capturing from your microphone. You're capturing from a virtual audio device (BlackHole) that receives a copy of your speaker output!
