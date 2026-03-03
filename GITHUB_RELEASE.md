# 🎉 BrJoy WebP Optimizer V1.0.0

**First stable release** - Desktop pipeline to optimize images for web performance.

---

## 🚀 What's New

Transform your website images in 3 steps:
1. **Scan** your project folder
2. **Choose** a web preset
3. **Convert** and see savings report

### ✨ Key Features

- 🔍 **Smart Recursive Scan** - Ignores `node_modules`, `.git`, processes up to 10k images
- 🎨 **6 Web Presets** - Hero, Blog Post, Thumbnail, Mobile, Avatar, Original Quality
- 📊 **Savings Report** - HTML report showing exactly how much space you saved
- 📁 **Preserves Structure** - Maintains your directory hierarchy
- 🛡️ **Non-Destructive** - Never overwrites original files
- ⚡ **Drag & Drop** - Drop files or folders directly
- ⌨️ **Keyboard Shortcuts** - Ctrl+O, Delete, Ctrl+Enter

### 📊 Real Results

```
Test 1: Next.js site (347 images)
├─ Original: 156.8 MB
├─ Final: 42.3 MB
└─ Savings: 114.5 MB (73%) ✅

Test 2: E-commerce (2,147 images)
├─ Original: 1.2 GB
├─ Final: 298 MB
└─ Savings: 902 MB (75%) ✅
```

---

## 📥 Installation

### Linux

```bash
# 1. Clone repository
git clone https://github.com/ibrumatte/brjoy-webp-optimizer.git
cd brjoy-webp-optimizer

# 2. Install dependencies
pip3 install tkinterdnd2
sudo apt install imagemagick

# 3. Run
python3 brjoy-converter
```

### Requirements

- Python 3.8+
- ImageMagick 7+
- tkinterdnd2 (optional, for drag & drop)

---

## 🎯 Use Cases

### Optimize Next.js Site
```
Folder: /project/public
Preset: Mobile Optimized
Result: 73% smaller, LCP improved 2.3s
```

### Prepare Blog Images
```
Folder: /blog/uploads
Preset: Blog Post (1200x630 Open Graph)
Result: SEO-optimized social media images
```

### Reduce CDN Costs
```
Folder: /ecommerce/products
Preset: Thumbnail (400x300)
Result: 75% bandwidth savings
```

---

## 📊 Web Presets

| Preset | Dimensions | Quality | Best For |
|--------|-----------|---------|----------|
| **Hero Image** | 1920x1080 | 85% | Banners, headers |
| **Blog Post** | 1200x630 | 85% | Open Graph, articles |
| **Thumbnail** | 400x300 | 80% | Listings, grids |
| **Mobile Optimized** | 800px | 80% | Mobile-first ⭐ |
| **Avatar/Icon** | 256x256 | 90% | Profiles, icons |
| **Original Quality** | Keep | 95% | No visual loss |

---

## 🐛 Known Issues

- Conversion can be slow with >1000 images (will be optimized in V1.1 with threads)
- HTML report may not open in some environments (TXT fallback in V1.1)

---

## 📈 What's Next

### V1.1 (April 2026)
- Parallel processing (threads)
- Cancel button during conversion
- Advanced filters

### V2.0 (Q2 2026)
- CLI: `brjoy-img optimize ./public`
- CI/CD integration (GitHub Actions)
- Watch mode

### V3.0 (Q3 2026)
- `<picture>` snippet generator
- Responsive variants (srcset)
- Hash deduplication

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 💬 Support

- 📧 Email: isac@brjoy.com.br
- 🐛 Issues: [GitHub Issues](https://github.com/ibrumatte/brjoy-webp-optimizer/issues)
- ⭐ Star this repo if it helped you!

---

## 🙏 Acknowledgments

Built for developers who care about web performance.

Special thanks to:
- ImageMagick team
- Python community
- Early beta testers

---

**Full Changelog**: https://github.com/ibrumatte/brjoy-webp-optimizer/commits/v1.0.0
