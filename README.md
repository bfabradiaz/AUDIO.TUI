```
 █████╗ ██╗   ██╗██████╗ ██╗ ██████╗      ████████╗██╗   ██╗██╗
██╔══██╗██║   ██║██╔══██╗██║██╔═══██╗     ╚══██╔══╝██║   ██║██║
███████║██║   ██║██║  ██║██║██║   ██║        ██║   ██║   ██║██║
██╔══██║██║   ██║██║  ██║██║██║   ██║        ██║   ██║   ██║██║
██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝ ██╗    ██║   ╚██████╔╝██║
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝  ╚═╝    ╚═╝    ╚═════╝ ╚═╝
```

> A beautiful, terminal-based audio player and visualizer with system audio integration.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

**Audio.TUI** is a modern terminal user interface (TUI) music player built with [Textual](https://github.com/Textualize/textual). It features a real-time audio visualizer, file browsing, and the unique ability to **visualize your system audio** (Spotify, YouTube, Browser) directly in the terminal.

---

## ✨ Features

- **🖥️ Beautiful TUI**: Built with Textual for a responsive, mouse-supported terminal interface.
- **📊 Real-time Visualizer**: Watch your music come to life with a smooth, reactive spectrum analyzer.
- **🌐 System Audio Capture**: Visualize audio from **any** source on your computer (Spotify, Chrome, etc.).
- **🖱️ Interactive Controls**: Clickable progress bar, volume control, and file browser.
- **💾 Persistence**: Remembers your track, position, and volume exactly where you left off.
- **⌨️ Keyboard Shortcuts**: Full keyboard control for power users.
- **🌈 Customization**: Rainbow ASCII art logo and customizable sensitivity.

---

## 🚀 Installation

We provide easy-to-use installation scripts for all major platforms.

### 🍎 macOS & 🐧 Linux

```bash
# Clone the repository
git clone https://github.com/yourusername/audio.tui.git
cd audio.tui

# Run the installer
./install.sh

# Start the app
aud
```

### 🪟 Windows

```powershell
# Clone the repository
git clone https://github.com/yourusername/audio.tui.git
cd audio.tui

# Run the installer
.\install.ps1

# Start the app
aud
```

*For manual installation details, see [docs/INSTALL.md](docs/INSTALL.md).*

---

## 📖 Usage

Once installed, simply type `aud` in your terminal to launch the app.

### Keyboard Shortcuts

| Key | Action |
| :--- | :--- |
| `Space` | Play / Pause |
| `n` | Next Track |
| `p` | Previous Track |
| `a` | Add Files (File Browser) |
| `m` | **Toggle Mode** (File Player / System Audio) |
| `i` | Cycle Input Device (in System Mode) |
| `[` / `]` | Decrease / Increase Sensitivity |
| `+` / `-` | Volume Up / Down |
| `q` | Quit |

---

## 🎧 System Audio Setup

To visualize audio from Spotify, YouTube, or your browser, you need to set up a virtual audio device.

### macOS
1. **Install BlackHole**: The installer tries to do this automatically (`brew install blackhole-2ch`).
2. **Create Multi-Output Device**:
   - Open **Audio MIDI Setup**.
   - Create a **Multi-Output Device**.
   - Check **BOTH** your speakers and **BlackHole 2ch**.
3. **Set Output**: Set your system output to this Multi-Output Device.
4. **In App**: Press `m` to switch to System Mode, then `i` to select BlackHole.

*Full Guide: [docs/SPEAKER_CAPTURE_EXPLAINED.md](docs/SPEAKER_CAPTURE_EXPLAINED.md)*

### Windows
1. Install **VB-Audio Virtual Cable**.
2. Set it as your default playback device (or use "Listen to this device").

*Full Guide: [docs/SYSTEM_AUDIO_SETUP.md](docs/SYSTEM_AUDIO_SETUP.md)*

---

## 📂 Documentation

- [Installation Guide](docs/INSTALL.md)
- [System Audio Setup (All OS)](docs/SYSTEM_AUDIO_SETUP.md)
- [Speaker Capture Explained (macOS)](docs/SPEAKER_CAPTURE_EXPLAINED.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
