# 🚀 BrJoy WebP Optimizer V1.1 - Performance & UX Update

Major performance improvements and quality-of-life features for faster, smarter image optimization.

## 🎯 Highlights

### ⚡ 4x Faster Conversions
- **Parallel Processing**: Uses 4 threads to convert multiple images simultaneously
- **Real-time Progress**: Live percentage and animated spinner
- **Cancel Anytime**: Stop conversion gracefully with Esc key

### 🎨 Visual Improvements
- **Preview Before/After**: See size reduction before converting (👁️ button)
- **Dark Mode**: Easy on the eyes with Ctrl+D toggle (🌙 button)
- **Advanced Filters**: Sharpen and brightness controls

### 📦 Batch Features
- **Multiple Sizes**: Generate 800px, 1200px, 1920px from one image
- **Conversion History**: Track all conversions with 📜 button

### ⌨️ Keyboard Shortcuts
- `Ctrl+O` - Add files
- `Ctrl+Enter` - Convert
- `Ctrl+D` - Dark mode
- `Ctrl+L` - Clear list
- `Esc` - Cancel conversion
- `Del` - Remove selected
- `Ctrl+Q` - Quit

## 📊 Performance

**Before V1.1:**
- 1000 images: ~5 minutes (single-threaded)

**After V1.1:**
- 1000 images: ~2 minutes (4 threads)
- **4x faster** on multi-core systems

## ✨ All Features (13/13)

1. ✅ Parallel Processing (4 threads)
2. ✅ Cancel Button (Esc)
3. ✅ Better Progress (percentage)
4. ✅ Loading Spinner (animated)
5. ✅ Preview Before/After (👁️)
6. ✅ Dark Mode (Ctrl+D, 🌙)
7. ✅ Advanced Filters (sharpen, brightness)
8. ✅ Batch Multiple Sizes (800,1200,1920)
9. ✅ History (📜, last 20)
10. ✅ Input Validation (1-10000px)
11. ✅ Better Error Messages
12. ✅ Keyboard Shortcuts (9 shortcuts)
13. ✅ All V1.0 features maintained

## 📦 Installation

### Requirements
- Python 3.8+
- ImageMagick 7+
- Optional: `pip install pillow` (for preview feature)

### Install
```bash
git clone https://github.com/ibrumatte/brjoy-webp-optimizer.git
cd brjoy-webp-optimizer
chmod +x brjoy-converter
./brjoy-converter
```

## 🔧 What's Changed

### Performance
- Implemented ThreadPoolExecutor for parallel image conversion
- Added cancel functionality with graceful shutdown
- Thread-safe UI updates during conversion

### UI/UX
- Added progress percentage display
- Added animated loading spinner
- Added dark mode with full theme switching
- Added preview window with before/after comparison
- Added history tracking (saved to `~/.local/share/brjoy-image-converter/history.txt`)

### Features
- Batch multiple sizes: generate 3+ sizes from one image
- Advanced filters: sharpen and brightness controls
- Input validation: prevents invalid width values
- Better error messages: specific errors for common issues

### Keyboard Shortcuts
- 9 new keyboard shortcuts for faster workflow
- Esc key cancels conversion
- Ctrl+D toggles dark mode

## 🐛 Bug Fixes
- Fixed error handling with specific messages
- Improved thread cleanup on cancellation
- Better validation for numeric inputs

## 📝 Documentation
- Updated README with all V1.1 features
- Updated ROADMAP with V1.2-V4.0 plans
- Complete CHANGELOG with all changes

## 🙏 Credits

Developed by **BrJoy** (isac@brjoy.com.br)

## 📄 License

MIT License - See LICENSE file for details

---

**Full Changelog**: https://github.com/ibrumatte/brjoy-webp-optimizer/compare/v1.0.0...v1.1.0
