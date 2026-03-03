# BrJoy WebP Optimizer

[![Version](https://img.shields.io/badge/version-1.2.1-blue.svg)](https://github.com/ibrumatte/brjoy-webp-optimizer/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Tests](https://github.com/ibrumatte/brjoy-webp-optimizer/workflows/Tests/badge.svg)](https://github.com/ibrumatte/brjoy-webp-optimizer/actions)

⚡ **4x faster** desktop pipeline to optimize images for web. Batch convert JPG/PNG to WebP with parallel processing, dark mode, preview, and **AI-powered code updates**.

## 🎯 Who Is This For

- Frontend developers (Next.js, Astro, Hugo, Vite)
- Web agencies optimizing client sites
- Freelancers reducing hosting costs
- Teams improving Core Web Vitals
- **Developers using AI coding assistants**

## ✨ Features V1.2.1

### 🔄 NEW: Replace in Place
- **Preserve Structure**: Convert images in their original folders
- **No Broken Paths**: Maintains directory structure automatically
- **Perfect for Projects**: Update existing codebases without moving files
- **Safe Warning**: Red indicator alerts about no automatic backup

### 📊 Automated Reports (V1.2)
- **HTML Report**: Beautiful visual dashboard with savings statistics
- **AI Code Update**: Structured report for AI to update your code automatically
- **CSV Export**: Spreadsheet-friendly data for analysis

### Performance
- ⚡ **Parallel Processing**: 4x faster with 4 threads (1000 images in ~2min)
- ⏸️ **Cancel Button**: Stop conversion anytime (Esc key)
- 📊 **Better Progress**: Live percentage and animated spinner

### Visual & Filters
- 👁️ **Preview Before/After**: See size reduction before converting
- 🌙 **Dark Mode**: Toggle with Ctrl+D
- 🎨 **Advanced Filters**: Sharpen and brightness controls

### Batch & History
- 📦 **Batch Multiple Sizes**: Generate 800px, 1200px, 1920px from one image
- 📜 **Conversion History**: Track all conversions (last 20)

### Quality of Life
- ⌨️ **9 Keyboard Shortcuts**: Ctrl+O, Ctrl+Enter, Ctrl+D, Esc, Del, Ctrl+Q, Ctrl+L
- ✅ **Input Validation**: Width 1-10000px
- 🚨 **Better Error Messages**: Specific errors for common issues

### V1.0 Features (Maintained)
- ✅ Recursive folder scan (ignores `node_modules`, `.git`, etc)
- ✅ 6 web presets (Hero, Blog, Thumbnail, Mobile, Avatar, Original)
- ✅ Quality slider 60-100% (default: 85%)
- ✅ Preserves directory structure
- ✅ Non-destructive mode (never overwrites originals)
- ✅ Drag & Drop files/folders

## 🚀 Quick Install

```bash
# 1. Clone repository
git clone https://github.com/ibrumatte/brjoy-webp-optimizer.git
cd brjoy-webp-optimizer

# 2. Install dependencies
pip3 install pillow  # Optional: for preview feature

# 3. Install ImageMagick
sudo apt install imagemagick

# 4. Run
python3 brjoy-converter
```

## ⌨️ Keyboard Shortcuts

- `Ctrl+O` - Add files
- `Ctrl+Enter` - Convert
- `Ctrl+D` - Toggle dark mode
- `Ctrl+L` - Clear list
- `Esc` - Cancel conversion
- `Del` - Remove selected
- `Ctrl+Q` - Quit

## 📖 Basic Usage

1. **Scan**: Click "📂 Scan Folder" and select root folder
2. **Preset**: Choose "Mobile Optimized" (recommended)
3. **Convert**: Click "✨ Convert (N)"
4. **Result**: View report and output folder

**Example:**
```
Input: /project/public (247 images, 156.8 MB)
Output: /brjoy-output (247 images, 42.3 MB)
Savings: 114.5 MB (73%) 🎉
```

## 📊 Web Presets

| Preset | Dimensions | Quality | Use Case |
|--------|-----------|---------|----------|
| Hero Image | 1920x1080 | 85% | Banners, headers |
| Blog Post | 1200x630 | 85% | Open Graph, articles |
| Thumbnail | 400x300 | 80% | Listings, grids |
| Mobile Optimized | 800px | 80% | Mobile-first ⭐ |
| Avatar/Icon | 256x256 | 90% | Profiles, icons |
| Original Quality | Keep | 95% | No visual loss |

## 🎓 Full Guide

See [GUIDE.md](GUIDE.md) for:
- Detailed use cases
- Advanced settings
- Troubleshooting
- Pro tips

## 📋 Roadmap

- **V1** (Current): Desktop Pro - batch conversion + reports ✅
- **V2** (Q2 2026): CLI for CI/CD
- **V3** (Q3 2026): `<picture>` snippet generator
- **V4** (Q4 2026): Cloud integrations (Cloudflare, S3)

## 🐛 Troubleshooting

**ImageMagick not found?**
```bash
sudo apt install imagemagick
```

**Drag & Drop not working?**
```bash
pip3 install tkinterdnd2
```

**Slow conversion?**
- Reduce quality to 80%
- Process smaller batches

## 🤝 Contributing

1. Fork the project
2. Create branch (`git checkout -b feature/new-feature`)
3. Commit (`git commit -m 'Add new feature'`)
4. Push (`git push origin feature/new-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 💬 Support

- 📧 Email: isac@brjoy.com.br
- 🐛 Issues: [GitHub Issues](https://github.com/brjoy/image-pipeline/issues)

---

**⭐ If this project helped you, leave a star on GitHub!**
