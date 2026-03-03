# Quick Start Guide

## Installation (2 minutes)

```bash
# Clone and install
git clone https://github.com/ibrumatte/brjoy-webp-optimizer.git
cd brjoy-webp-optimizer
./install.sh

# Run
./brjoy-converter
```

## First Conversion (30 seconds)

1. **Add Images**
   - Click "📂 Escanear Pasta" or press `Ctrl+O`
   - Select folder with JPG/PNG images
   - Wait for scan to complete

2. **Configure** (optional)
   - Choose preset: "Blog Post" (1200x630)
   - Adjust quality: 85% (default)
   - Enable filters: Sharpen, Brightness

3. **Preview** (optional)
   - Click "👁️" button
   - See before/after comparison
   - Check file size reduction

4. **Convert**
   - Press `Ctrl+Enter` or click "✨ Converter"
   - Watch progress (percentage + spinner)
   - Cancel anytime with `Esc`

5. **Done!**
   - Output folder opens automatically
   - Check conversion history with "📜"

## Common Workflows

### Workflow 1: Blog Images
```
1. Scan blog/images folder
2. Select "Blog Post" preset (1200x630)
3. Quality: 85%
4. Convert
→ Result: Optimized images for social sharing
```

### Workflow 2: Responsive Images
```
1. Scan assets folder
2. Enable "Batch Multiple Sizes"
3. Enter: 800,1200,1920
4. Convert
→ Result: 3 sizes per image (image_800w.webp, etc)
```

### Workflow 3: Quick Optimization
```
1. Drag & drop images
2. Select "Original Quality" preset
3. Convert
→ Result: WebP with minimal quality loss
```

## Keyboard Shortcuts Cheatsheet

| Action | Shortcut |
|--------|----------|
| Add files | `Ctrl+O` |
| Convert | `Ctrl+Enter` |
| Dark mode | `Ctrl+D` |
| Clear list | `Ctrl+L` |
| Cancel | `Esc` |
| Remove selected | `Del` |
| Quit | `Ctrl+Q` |

## Tips & Tricks

### Tip 1: Batch Processing
Process entire website at once:
```bash
# Scan your project root
# App ignores: node_modules, .git, dist, build
```

### Tip 2: Quality Settings
- **95%**: Photography, portfolios
- **85%**: General web use (recommended)
- **75%**: Thumbnails, previews
- **60%**: Icons, small images

### Tip 3: Dark Mode
Work at night? Press `Ctrl+D` for dark mode.

### Tip 4: History
Track all conversions with "📜" button. Clear anytime.

### Tip 5: Multiple Sizes
Generate responsive images in one go:
```
Input: hero.jpg (3000x2000)
Sizes: 800,1200,1920
Output: 
  - hero_800w.webp
  - hero_1200w.webp
  - hero_1920w.webp
```

## Troubleshooting

### Issue: "ImageMagick not found"
```bash
sudo apt install imagemagick
```

### Issue: Preview not working
```bash
pip install pillow
```

### Issue: Slow conversion
- Check CPU usage (app uses 4 threads)
- Reduce image count per batch
- Lower quality setting

### Issue: Out of memory
- Process smaller batches
- Close other applications
- Reduce max workers in code

## Performance Tips

1. **Use SSD**: 2x faster than HDD
2. **Close apps**: Free up RAM
3. **Batch sizes**: 1000 images optimal
4. **Quality**: 85% is sweet spot

## Next Steps

- Read full documentation: `README.md`
- Check roadmap: `ROADMAP.md`
- Report issues: GitHub Issues
- Contribute: `CONTRIBUTING.md`

## Support

- Email: isac@brjoy.com.br
- GitHub: https://github.com/ibrumatte/brjoy-webp-optimizer
- Issues: https://github.com/ibrumatte/brjoy-webp-optimizer/issues

---

**Happy optimizing!** 🚀
