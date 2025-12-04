#!/bin/bash

# Audio.TUI Installer for macOS and Linux
# Installs dependencies, sets up virtual environment, and creates 'aud' command

set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/venv"
BIN_NAME="aud"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}       Audio.TUI Installer              ${NC}"
echo -e "${BLUE}========================================${NC}"

# 1. Detect OS
OS="$(uname -s)"
echo -e "${GREEN}Detected OS: $OS${NC}"

# 2. Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed.${NC}"
    if [[ "$OS" == "Darwin" ]]; then
        echo "Please install Python 3 (brew install python)"
    else
        echo "Please install Python 3 (sudo apt install python3 python3-venv python3-pip)"
    fi
    exit 1
fi

# 3. Setup Virtual Environment
echo -e "${GREEN}Setting up Python virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Created venv."
else
    echo "venv already exists."
fi

# 4. Install Dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip > /dev/null
pip install -r "$APP_DIR/requirements.txt"

# 5. OS Specific Setup (Audio Drivers)
if [[ "$OS" == "Darwin" ]]; then
    echo -e "${GREEN}Checking macOS Audio Setup...${NC}"
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}Homebrew not found. Skipping BlackHole auto-install.${NC}"
    else
        if ! brew list blackhole-2ch &> /dev/null; then
            echo -e "${YELLOW}Installing BlackHole 2ch for system audio capture...${NC}"
            brew install blackhole-2ch || echo -e "${RED}Failed to install BlackHole. You may need to install it manually.${NC}"
        else
            echo "BlackHole 2ch is already installed."
        fi
    fi
elif [[ "$OS" == "Linux" ]]; then
    echo -e "${GREEN}Checking Linux Audio Setup...${NC}"
    # Check for PortAudio (needed for sounddevice)
    if command -v apt-get &> /dev/null; then
        echo "Installing PortAudio development headers..."
        sudo apt-get update && sudo apt-get install -y libportaudio2 libasound2-dev || true
    fi
fi

# 6. Create 'aud' command
echo -e "${GREEN}Creating '$BIN_NAME' command...${NC}"

# Create a wrapper script
WRAPPER_PATH="$APP_DIR/$BIN_NAME"
cat > "$WRAPPER_PATH" <<EOF
#!/bin/bash
DIR="\$(cd "\$(dirname "\$0")" && pwd)"
cd "\$DIR"
source "venv/bin/activate"
python3 "app.py" "\$@"
EOF
chmod +x "$WRAPPER_PATH"

# Add to PATH (User's .bashrc or .zshrc)
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ] || [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if [ -n "$SHELL_CONFIG" ]; then
    if ! grep -q "alias $BIN_NAME=" "$SHELL_CONFIG"; then
        echo -e "${YELLOW}Adding alias to $SHELL_CONFIG...${NC}"
        echo "" >> "$SHELL_CONFIG"
        echo "# Audio.TUI alias" >> "$SHELL_CONFIG"
        echo "alias $BIN_NAME='$WRAPPER_PATH'" >> "$SHELL_CONFIG"
        echo -e "${GREEN}Alias added!${NC}"
    else
        echo "Alias already exists in $SHELL_CONFIG"
    fi
else
    echo -e "${YELLOW}Could not detect shell config file. You can run the app using: $WRAPPER_PATH${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Please restart your terminal or run: ${YELLOW}source $SHELL_CONFIG${NC}"
echo -e "Then type ${GREEN}$BIN_NAME${NC} to start the app."
