#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     CRITICAL: Multi-Output Device Not Set as System Output      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "The diagnostic test shows BlackHole is receiving NO audio."
echo "This means the Multi-Output Device is NOT set as your system output."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SOLUTION: Set Multi-Output Device as System Output"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Opening System Sound Settings..."
sleep 2

# Open System Sound Settings
open "x-apple.systempreferences:com.apple.preference.sound"

echo ""
echo "In the Sound Settings window that just opened:"
echo ""
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ STEP 1: Click the 'Output' tab                                │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ STEP 2: Select 'Multi-Output Device'                          │"
echo "│                                                                │"
echo "│ You should see:                                                │"
echo "│   ○ MacBook Pro Speakers (or your current output)             │"
echo "│   ● Multi-Output Device  ← SELECT THIS!                       │"
echo "│   ○ BlackHole 2ch                                             │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "⚠️  IMPORTANT: If you don't see 'Multi-Output Device':"
echo "   → You need to CREATE it first in Audio MIDI Setup"
echo "   → Run: ./setup_speaker_capture.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter after you've selected Multi-Output Device..."

echo ""
echo "Testing if it worked..."
echo ""

# Play a test sound
afplay /System/Library/Sounds/Glass.aiff &

echo "You should have just heard a sound."
echo ""
echo "Now let's test if BlackHole is receiving audio:"
echo ""
echo "Running diagnostic test..."
echo "Play some music from your browser while this runs."
echo ""
sleep 2

python test_audio_input.py &
TEST_PID=$!

echo ""
echo "Watch the 'Level' bar above."
echo "If it moves, BlackHole is working!"
echo ""
echo "Press Ctrl+C when done testing..."

wait $TEST_PID

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "If the bars were moving:"
echo "  ✓ BlackHole is now receiving audio!"
echo "  → Restart Audio.TUI: python app.py"
echo "  → Press 'm' to switch to System Audio mode"
echo "  → Press 'i' to select BlackHole 2ch"
echo "  → Press ']' to increase sensitivity"
echo ""
echo "If the bars were NOT moving:"
echo "  ✗ Multi-Output Device not configured correctly"
echo "  → Open Audio MIDI Setup"
echo "  → Make sure Multi-Output Device has BOTH:"
echo "    ☑ Your speakers"
echo "    ☑ BlackHole 2ch"
echo ""
