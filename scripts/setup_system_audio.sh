#!/bin/bash

echo "=================================="
echo "Audio.TUI - System Audio Setup"
echo "=================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script is for macOS only."
    echo "For Linux/Windows, see SYSTEM_AUDIO_SETUP.md"
    exit 1
fi

echo "This script will help you set up system audio capture for Audio.TUI"
echo ""
echo "What would you like to do?"
echo "1) Install BlackHole (recommended - free)"
echo "2) Open Audio MIDI Setup to create Multi-Output Device"
echo "3) Show manual setup instructions"
echo "4) Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Installing BlackHole via Homebrew..."
        if command -v brew &> /dev/null; then
            brew install blackhole-2ch
            echo ""
            echo "✓ BlackHole installed successfully!"
            echo ""
            echo "Next steps:"
            echo "1. Run this script again and choose option 2"
            echo "2. Or manually open Audio MIDI Setup and create a Multi-Output Device"
        else
            echo "Homebrew not found. Please install it first:"
            echo "Visit: https://brew.sh"
            echo ""
            echo "Or download BlackHole manually from:"
            echo "https://existential.audio/blackhole/"
        fi
        ;;
    2)
        echo ""
        echo "Opening Audio MIDI Setup..."
        open "/System/Applications/Utilities/Audio MIDI Setup.app"
        echo ""
        echo "In Audio MIDI Setup:"
        echo "1. Click the '+' button at bottom left"
        echo "2. Select 'Create Multi-Output Device'"
        echo "3. Check BOTH:"
        echo "   - Your speakers/headphones"
        echo "   - BlackHole 2ch"
        echo "4. Right-click the Multi-Output Device"
        echo "5. Select 'Use This Device For Sound Output'"
        echo ""
        echo "Then in Audio.TUI:"
        echo "- Press 'm' to switch to System Audio mode"
        echo "- Press 'i' to select BlackHole 2ch as input"
        echo "- Press ']' to increase sensitivity"
        ;;
    3)
        echo ""
        cat SYSTEM_AUDIO_SETUP.md
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
echo "Setup complete! Run 'python app.py' to start Audio.TUI"
