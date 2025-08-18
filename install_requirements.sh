#!/bin/bash

# Automatic Requirements Installer for Unix/Linux/macOS
# This script activates the virtual environment and runs the requirements installer

echo "🚀 Starting Automatic Requirements Installer..."
echo

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please create a virtual environment first by running:"
    echo "   python -m venv venv"
    echo
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Run the Python installer script
echo
echo "📦 Running requirements installer..."
python install_requirements.py

# Check exit status
if [ $? -eq 0 ]; then
    echo
    echo "✅ Installation completed successfully!"
else
    echo
    echo "⚠️  Installation completed with errors."
fi
