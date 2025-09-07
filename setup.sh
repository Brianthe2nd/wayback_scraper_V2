#!/usr/bin/env bash
set -e

echo "=== Project Setup & Run Script ==="

# --- Helper function to check command existence ---
check_cmd() {
    command -v "$1" >/dev/null 2>&1
}

# --- Install Python if missing ---
if ! check_cmd python && ! check_cmd python3; then
    echo "Python not found. Installing..."
    if check_cmd winget; then
        winget install -e --id Python.Python.3
    elif check_cmd apt-get; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    elif check_cmd brew; then
        brew install python
    else
        echo "Please install Python manually."
        exit 1
    fi
else
    echo "Python is already installed."
fi

# Ensure 'python' command is available
if check_cmd python3 && ! check_cmd python; then
    alias python=python3
fi

# --- Install pip if missing ---
if ! check_cmd pip && ! check_cmd pip3; then
    echo "pip not found. Installing..."
    python -m ensurepip --upgrade || python3 -m ensurepip --upgrade
else
    echo "pip is already installed."
fi

# --- Install Ruby if missing ---
if ! check_cmd ruby; then
    echo "Ruby not found. Installing..."
    if check_cmd winget; then
        winget install -e --id RubyInstallerTeam.Ruby
    elif check_cmd apt-get; then
        sudo apt-get update && sudo apt-get install -y ruby-full
    elif check_cmd brew; then
        brew install ruby
    else
        echo "Please install Ruby manually."
        exit 1
    fi
else
    echo "Ruby is already installed."
fi

# --- Install Python dependencies ---
echo "Installing Python dependencies..."
pip install -r requirements.txt || pip3 install -r requirements.txt

# --- Install Ruby dependencies (only if not installed yet) ---
if [ ! -d "wayback-machine-downloader" ]; then
    echo "Cloning Ruby dependency..."
    git clone "https://github.com/ShiftaDeband/wayback-machine-downloader.git"
else
    echo "Ruby dependency already present, skipping clone."
fi

# --- Run main.py ---
echo "Starting project..."
python main.py || python3 main.py
