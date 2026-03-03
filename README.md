# BrJoy Web Optimizer

Desktop pipeline to optimize images for web. Batch convert JPG/PNG to WebP, preserve directory structure, and generate savings reports.

## 🎯 Who Is This For

- Frontend developers (Next.js, Astro, Hugo, Vite)
- Web agencies optimizing client sites
- Freelancers reducing hosting costs
- Teams improving Core Web Vitals

## ✨ Features V1

- ✅ Recursive folder scan (ignores `node_modules`, `.git`, etc)
- ✅ 6 web presets (Hero, Blog, Thumbnail, Mobile, Avatar, Original)
- ✅ Quality slider 60-100% (default: 85%)
- ✅ Preserves directory structure
- ✅ HTML report with space savings
- ✅ Non-destructive mode (never overwrites originals)
- ✅ Drag & Drop files/folders
- ✅ Keyboard shortcuts (Ctrl+O, Delete, Ctrl+Enter)

## 🚀 Quick Install

```bash
# 1. Clone repository
git clone https://github.com/brjoy/image-pipeline.git
cd image-pipeline

# 2. Install dependencies
pip3 install tkinterdnd2

# 3. Install ImageMagick
sudo apt install imagemagick

# 4. Run
python3 brjoy-converter
```

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
- **V4** (Q4 2026): WordPress plugin + CDN integrations

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
