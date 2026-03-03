# 🚀 BrJoy WebP Optimizer - Roadmap V1.1 - V2.0

**Last Updated:** 03/03/2026  
**Current Version:** V1.0.0

---

## 🔥 V1.1 - Performance & Polish (Target: Week of March 10, 2026)

**Release Date:** March 10-14, 2026 (Next Week)  
**Focus:** Performance improvements and critical UX fixes

### 🚀 Performance (P0 - Critical)

#### #1 - Parallel Processing
**Priority:** P0  
**Effort:** 4h  
**Impact:** High

- Implement multi-threading for image conversion
- Process 4-8 images simultaneously (based on CPU cores)
- Expected: 3-4x faster conversion
- Target: 1000 images in <2min (currently ~5min)

**Technical:**
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(convert_image, img) for img in images]
```

---

#### #2 - Cancel Button
**Priority:** P0  
**Effort:** 2h  
**Impact:** High

- Add "Cancel" button during conversion
- Gracefully stop threads
- Show partial results (converted so far)
- Don't leave corrupted files

**UI:**
```
[████████░░░░] 65% Converting...  [Cancel]
```

---

#### #3 - Better Progress Feedback
**Priority:** P1  
**Effort:** 1h  
**Impact:** Medium

- Show current image being processed
- Estimated time remaining
- Images/second rate

**UI:**
```
Converting: /blog/hero-image.jpg (123/247)
Speed: 8.5 img/s | ETA: 2min 15s
```

---

### 🎨 UI/UX Improvements (P1 - High)

#### #4 - Loading Spinner During Scan
**Priority:** P1  
**Effort:** 1h  
**Impact:** Medium

- Show animated spinner while scanning folders
- Prevent "app frozen" feeling
- Display: "Scanning... found 247 images"

---

#### #5 - Preview Before/After
**Priority:** P1  
**Effort:** 6h  
**Impact:** High

- Side-by-side image comparison
- Zoom in/out
- Show file size difference
- Quality slider preview (real-time)

**UI:**
```
┌─────────────┬─────────────┐
│   Before    │    After    │
│  2.3 MB     │   0.6 MB    │
│  JPG        │   WebP      │
└─────────────┴─────────────┘
     [< Prev]  [Next >]
```

---

#### #6 - Tooltips for Presets
**Priority:** P2  
**Effort:** 30min  
**Impact:** Low

- Hover over preset → show tooltip
- Explain dimensions, quality, use case
- Example: "Hero Image: 1920x1080, 85% quality. Best for banners and headers."

---

#### #7 - Dark Mode
**Priority:** P2  
**Effort:** 3h  
**Impact:** Medium

- Toggle button in header
- Dark theme colors:
  - Background: #1a1a1a
  - Card: #2d2d2d
  - Text: #e5e5e5
  - Primary: #0a84ff
- Save preference to config file

---

### 🛠️ Features (P1 - High)

#### #8 - Advanced Filters
**Priority:** P1  
**Effort:** 2h  
**Impact:** Medium

- Checkbox: "Ignore images <50KB" (already optimized)
- Checkbox: "Ignore images >10MB" (too large, may crash)
- Text field: "Exclude folders" (comma-separated)
- Example: `thumbs, cache, temp`

**UI:**
```
Filters:
☑ Ignore <50KB
☐ Ignore >10MB
Exclude folders: [thumbs, cache    ]
```

---

#### #9 - Batch Multiple Sizes
**Priority:** P1  
**Effort:** 4h  
**Impact:** High

- Generate 3 versions in one pass:
  - Mobile: 640px
  - Tablet: 1024px
  - Desktop: 1920px
- Output structure:
  ```
  /output/
    /mobile/
    /tablet/
    /desktop/
  ```

**Preset:**
```
Responsive Set:
├─ 640px (mobile)
├─ 1024px (tablet)
└─ 1920px (desktop)
```

---

#### #10 - Conversion History
**Priority:** P2  
**Effort:** 3h  
**Impact:** Low

- Save last 10 conversions
- Show: date, folder, images count, savings
- Button: "Repeat Last Conversion"
- Stored in: `~/.brjoy/history.json`

**UI:**
```
Recent Conversions:
├─ 03/03 - /project/public - 247 imgs - 73% saved
├─ 02/03 - /blog/uploads - 89 imgs - 68% saved
└─ 01/03 - /ecommerce - 1,234 imgs - 75% saved
```

---

### 🐛 Bugs & Polish (P2 - Medium)

#### #11 - Input Validation
**Priority:** P2  
**Effort:** 1h  
**Impact:** Low

- Check if folder exists before scanning
- Validate quality slider (60-100)
- Validate width/height (positive integers)
- Show error messages clearly

---

#### #12 - Better Error Messages
**Priority:** P2  
**Effort:** 2h  
**Impact:** Medium

- Instead of: "Error converting image"
- Show: "Failed to convert hero.jpg: File corrupted or unsupported format"
- Log errors to: `~/.brjoy/errors.log`

---

#### #13 - Keyboard Shortcuts
**Priority:** P2  
**Effort:** 30min  
**Impact:** Low

- `Ctrl+S` - Scan folder
- `Ctrl+Q` - Quit app
- `Ctrl+H` - Show shortcuts help
- `Escape` - Cancel conversion

---

## 🚀 V2.0 - CLI & Automation (Target: Q2 2026)

### Core Features

#### #14 - Command Line Interface
**Priority:** P0  
**Effort:** 8h  
**Impact:** Critical

```bash
brjoy-img optimize ./public \
  --format webp \
  --quality 85 \
  --preset mobile \
  --output ./optimized \
  --report
```

**Options:**
- `--format` - webp, png, jpg
- `--quality` - 60-100
- `--preset` - hero, blog, thumbnail, mobile, avatar, original
- `--width` - custom width
- `--height` - custom height
- `--keep-original` - don't delete originals
- `--report` - generate HTML report
- `--dry-run` - show what would happen
- `--threads` - number of parallel threads

---

#### #15 - CI/CD Integration
**Priority:** P0  
**Effort:** 4h  
**Impact:** High

**GitHub Actions Example:**
```yaml
name: Optimize Images
on: [push]
jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Optimize images
        run: |
          pip install brjoy-img
          brjoy-img optimize ./public --format webp --quality 85
      - name: Commit optimized
        run: |
          git add .
          git commit -m "chore: optimize images"
          git push
```

---

#### #16 - Watch Mode
**Priority:** P1  
**Effort:** 3h  
**Impact:** Medium

```bash
brjoy-img watch ./public --format webp --quality 85
```

- Monitors folder for new images
- Auto-converts on file add/change
- Perfect for development workflow

---

#### #17 - Config File
**Priority:** P1  
**Effort:** 2h  
**Impact:** Medium

**`.brjoy.yml`:**
```yaml
format: webp
quality: 85
preset: mobile
output: ./optimized
keep_original: true
ignore:
  - "*.svg"
  - "node_modules/**"
  - "dist/**"
threads: 4
```

---

## 🎨 V3.0 - Advanced Features (Target: Q3 2026)

### #18 - Picture Snippet Generator
**Priority:** P0  
**Effort:** 6h  
**Impact:** High

Generate HTML snippets with fallbacks:

```html
<picture>
  <source type="image/webp" srcset="hero.webp">
  <source type="image/jpeg" srcset="hero.jpg">
  <img src="hero.jpg" alt="Hero image" width="1920" height="1080">
</picture>
```

---

### #19 - Responsive Variants (srcset)
**Priority:** P0  
**Effort:** 8h  
**Impact:** High

Generate multiple sizes + srcset:

```html
<img 
  srcset="hero-640.webp 640w,
          hero-1024.webp 1024w,
          hero-1920.webp 1920w"
  sizes="(max-width: 640px) 640px,
         (max-width: 1024px) 1024px,
         1920px"
  src="hero-1920.webp"
  alt="Hero">
```

---

### #20 - Hash Deduplication
**Priority:** P1  
**Effort:** 4h  
**Impact:** Medium

- Calculate MD5 hash of each image
- Skip duplicates (same content, different name)
- Report: "Found 23 duplicate images, saved 45MB"

---

## 🏢 V4.0 - Integrations (Target: Q4 2026)

### #21 - WordPress Plugin
**Priority:** P0  
**Effort:** 20h  
**Impact:** Critical

- Auto-optimize on upload
- Bulk optimize existing media library
- Serve WebP with fallback
- Settings page in WP admin

---

### #22 - Cloudflare Images Integration
**Priority:** P1  
**Effort:** 12h  
**Impact:** High

- Upload optimized images to Cloudflare
- Generate URLs with transformations
- Automatic CDN distribution

---

### #23 - REST API
**Priority:** P1  
**Effort:** 16h  
**Impact:** High

```bash
POST /api/optimize
{
  "images": ["url1", "url2"],
  "format": "webp",
  "quality": 85
}

Response:
{
  "optimized": ["url1_opt", "url2_opt"],
  "savings": "73%"
}
```

---

## 📊 Effort Summary

### V1.1 - Next Week Sprint (Total: ~30h over 5 days = 6h/day)
**Days:** March 10-14, 2026

**Monday (6h):**
- #1 Parallel Processing (4h)
- #2 Cancel Button (2h)

**Tuesday (6h):**
- #3 Better Progress (1h)
- #4 Loading Spinner (1h)
- #8 Advanced Filters (2h)
- #11 Input Validation (1h)
- #13 Keyboard Shortcuts (1h)

**Wednesday (6h):**
- #5 Preview Before/After (6h)

**Thursday (6h):**
- #9 Batch Multiple Sizes (4h)
- #12 Better Error Messages (2h)

**Friday (6h):**
- #7 Dark Mode (3h)
- #10 History (3h)

**Weekend:**
- Testing & bug fixes
- Update documentation
- Release V1.1

### V2.0 (Total: ~17h)
- CLI: 8h
- CI/CD: 4h
- Watch: 3h
- Config: 2h

### V3.0 (Total: ~18h)
- Snippets: 6h
- Srcset: 8h
- Dedup: 4h

### V4.0 (Total: ~48h)
- WordPress: 20h
- Cloudflare: 12h
- API: 16h

---

## 🎯 Priority Matrix

### Must Have (V1.1)
1. Parallel Processing
2. Cancel Button
3. Advanced Filters
4. Batch Multiple Sizes

### Should Have (V1.1)
5. Loading Spinner
6. Preview Before/After
7. Better Progress

### Nice to Have (V1.1)
8. Dark Mode
9. Tooltips
10. History

### Future (V2.0+)
11. CLI
12. CI/CD
13. Watch Mode
14. WordPress Plugin

---

## 📅 Release Schedule

- **V1.1** - March 10-14, 2026 (Next Week) ⚡
- **V2.0** - April 2026 (1 month)
- **V3.0** - June 2026 (Q2)
- **V4.0** - September 2026 (Q3)

---

## 🤝 Contributing

Want to help? Pick an issue from the roadmap and submit a PR!

**Good First Issues:**
- #6 - Tooltips (30min)
- #11 - Input Validation (1h)
- #13 - Keyboard Shortcuts (30min)

---

**Last Updated:** 03/03/2026  
**Maintainer:** isac@brjoy.com.br
