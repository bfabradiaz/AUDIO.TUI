# Installation Guide

Audio.TUI supports macOS, Linux, and Windows.

## 🚀 Quick Install

Open your terminal and run the command for your operating system.

### 🍎 macOS & 🐧 Linux

You can install Audio.TUI with a single command:

```bash
# Clone and install
git clone https://github.com/yourusername/audio.tui.git
cd audio.tui
chmod +x install.sh
./install.sh
```

After installation, restart your terminal and type:
```bash
aud
```

### 🪟 Windows (PowerShell)

1. Open PowerShell as Administrator (optional, but recommended for PATH updates).
2. Run the following commands:

```powershell
# Clone (requires Git)
git clone https://github.com/yourusername/audio.tui.git
cd audio.tui
.\install.ps1
```

After installation, restart PowerShell and type:
```powershell
aud
```

---

## 📦 Manual Installation

If you prefer to install manually without the helper scripts:

### Prerequisites
- Python 3.8 or higher
- Git

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/audio.tui.git
   cd audio.tui
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```

---

## 🔊 System Audio Setup

To use the visualizer with system audio (Spotify, Browser, etc.), you need a virtual audio driver.

### macOS
The installer attempts to install **BlackHole 2ch** via Homebrew.
If it fails, install manually: `brew install blackhole-2ch`
*See `SPEAKER_CAPTURE_EXPLAINED.md` for configuration details.*

### Windows
Install **VB-Audio Virtual Cable**:
[Download VB-CABLE](https://vb-audio.com/Cable/)

### Linux
Usually works out of the box with PulseAudio/PipeWire.
If needed, install PulseAudio tools: `sudo apt install pavucontrol`
