#!/bin/bash
# BrJoy WebP Optimizer - Quick Install Script

set -e

echo "🚀 BrJoy WebP Optimizer - Quick Install"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"

# Check ImageMagick
if ! command -v convert &> /dev/null; then
    echo "⚠️  ImageMagick not found"
    read -p "Install ImageMagick? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update
        sudo apt install -y imagemagick
        echo "✅ ImageMagick installed"
    else
        echo "❌ ImageMagick required. Install manually: sudo apt install imagemagick"
        exit 1
    fi
else
    echo "✅ ImageMagick found"
fi

# Install Pillow (optional)
if ! python3 -c "import PIL" &> /dev/null; then
    echo "⚠️  Pillow not found (optional for preview feature)"
    read -p "Install Pillow? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install pillow
        echo "✅ Pillow installed"
    else
        echo "⏭️  Skipping Pillow (preview feature disabled)"
    fi
else
    echo "✅ Pillow found"
fi

# Make executable
chmod +x brjoy-converter
echo "✅ Made brjoy-converter executable"

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📖 Quick Start:"
echo "   ./brjoy-converter"
echo ""
echo "⌨️  Keyboard Shortcuts:"
echo "   Ctrl+O      - Add files"
echo "   Ctrl+Enter  - Convert"
echo "   Ctrl+D      - Dark mode"
echo "   Esc         - Cancel"
echo ""
echo "📚 Documentation: README.md"
echo "🐛 Issues: https://github.com/ibrumatte/brjoy-webp-optimizer/issues"
echo ""
