#!/bin/bash
# Quick Test Script for BrJoy WebP Optimizer

echo "🧪 BrJoy WebP Optimizer - Quick Tests"
echo "====================================="
echo ""

# Test 1: Python syntax
echo "Test 1: Python syntax check..."
if python3 -m py_compile brjoy-converter; then
    echo "✅ Syntax OK"
else
    echo "❌ Syntax error"
    exit 1
fi

# Test 2: Dependencies
echo ""
echo "Test 2: Checking dependencies..."

if command -v python3 &> /dev/null; then
    echo "✅ Python 3 installed"
else
    echo "❌ Python 3 not found"
    exit 1
fi

if command -v convert &> /dev/null; then
    echo "✅ ImageMagick installed"
else
    echo "❌ ImageMagick not found"
    exit 1
fi

if python3 -c "import tkinter" &> /dev/null; then
    echo "✅ Tkinter available"
else
    echo "❌ Tkinter not found"
    exit 1
fi

if python3 -c "import PIL" &> /dev/null; then
    echo "✅ Pillow installed (preview enabled)"
else
    echo "⚠️  Pillow not found (preview disabled)"
fi

# Test 3: File structure
echo ""
echo "Test 3: Checking file structure..."

required_files=(
    "brjoy-converter"
    "README.md"
    "CHANGELOG.md"
    "ROADMAP.md"
    "PRD.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Test 4: Executable permissions
echo ""
echo "Test 4: Checking permissions..."
if [ -x "brjoy-converter" ]; then
    echo "✅ brjoy-converter is executable"
else
    echo "⚠️  brjoy-converter not executable (run: chmod +x brjoy-converter)"
fi

# Test 5: Git status
echo ""
echo "Test 5: Git repository status..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "✅ Git repository initialized"
    COMMITS=$(git log --oneline | wc -l)
    echo "   Commits: $COMMITS"
    TAGS=$(git tag | wc -l)
    echo "   Tags: $TAGS"
else
    echo "❌ Not a git repository"
fi

# Summary
echo ""
echo "================================"
echo "✅ All tests passed!"
echo ""
echo "Ready to run: ./brjoy-converter"
echo ""
