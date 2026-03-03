# CHANGELOG

## [1.2.1] - 2026-03-03

### 🔄 Replace in Place

New option to convert images in their original folders, preserving project structure.

### ✨ New Features

- **Replace in Place Option**: Checkbox to convert images without moving them
  - Saves converted files in same folder as originals
  - Preserves directory structure automatically
  - Perfect for updating existing projects
  - No broken code references
  - Warning indicator (red text) alerts about no backup

### 🔧 Technical Changes

- Modified `convert_single()` to support dual output modes
- Added `self.substituir_no_lugar` BooleanVar (line 121)
- Dynamic output path: `arquivo_path.parent` vs `pasta_final`
- UI checkbox added in configuration panel

### 📖 Use Cases

**Before (V1.2.0):**
```
src/images/hero.png → output/BrJoy_2026-03-03/hero.webp
```

**After (V1.2.1):**
```
src/images/hero.png → src/images/hero.webp  ✓ Same folder!
```

---

## [1.2.0] - 2026-03-03

### 📊 Reports & AI Integration

Automatic report generation for visual analysis and AI-powered code updates.

### ✨ New Features

#### Automated Reports
- **HTML Report**: Beautiful visual report with statistics
  - Total savings (MB and %)
  - Before/after sizes
  - Conversion duration
  - Top 10 images with most savings
  - Auto-opens in browser
  - Saved as `conversion-report.html`

- **AI Code Update Report**: Structured report for AI assistants
  - File mapping: `old.png → new.webp`
  - Examples for HTML, CSS, JS, React, Markdown
  - Suggested prompts for AI
  - Perfect for Claude, ChatGPT, Copilot
  - Saved as `AI-CODE-UPDATE.txt`

- **CSV Export**: Spreadsheet-friendly format
  - Columns: ANTES, DEPOIS, sizes, savings
  - Easy to import and analyze
  - Saved as `conversions.csv`

### 🤖 AI Workflow
1. Convert images with BrJoy
2. Get `AI-CODE-UPDATE.txt` report
3. Send to AI: "Update all image URLs from this report"
4. AI automatically replaces URLs in your codebase

### 🔧 Technical
- File-by-file tracking with sizes
- Responsive HTML design
- UTF-8 encoding for international support

---

## [1.1.0] - 2026-03-03

### 🚀 Performance & UX Update

Major performance improvements and quality-of-life features.

### ✨ New Features

#### Performance
- **#1 Parallel Processing**: 4x faster with ThreadPoolExecutor (4 threads)
  - 1000 images: ~2min (was ~5min)
- **#2 Cancel Button**: Stop conversion gracefully (Esc key)
  - Shows partial results, no corrupted files

#### Progress & Feedback
- **#3 Better Progress**: Percentage display next to progress bar
- **#4 Loading Spinner**: Animated spinner during conversion

#### Visual & Filters
- **#5 Preview Before/After**: Side-by-side comparison with 👁️ button
  - Shows dimensions, file size, reduction %
- **#7 Dark Mode**: Toggle with 🌙 button or Ctrl+D
- **#8 Advanced Filters**: Sharpen and brightness controls

#### Batch & History
- **#9 Batch Multiple Sizes**: Generate multiple widths from one image
  - Example: 800,1200,1920 → image_800w.webp, image_1200w.webp, image_1920w.webp
- **#10 History**: Track conversions with 📜 button (last 20)
  - Timestamp, success/errors, output folder

#### Quality of Life
- **#11 Input Validation**: Width accepts only 1-10000px
- **#12 Better Error Messages**: Specific errors for common issues
  - ImageMagick not installed, cannot read file, out of memory
- **#13 Keyboard Shortcuts**: 
  - Ctrl+O: Add files
  - Ctrl+L: Clear list
  - Ctrl+Enter: Convert
  - Ctrl+D: Dark mode
  - Esc: Cancel
  - Del: Remove selected
  - Ctrl+Q: Quit

### 📦 Dependencies
- Optional: `pip install pillow` for preview feature

### 🔧 Technical
- Concurrent image processing with ThreadPoolExecutor
- Thread-safe UI updates
- Graceful cancellation with cleanup
- History saved to `~/.local/share/brjoy-image-converter/history.txt`

---

## [1.0.0] - 2026-03-03

### 🎉 Lançamento Inicial - BrJoy Web Optimizer V1

Pipeline desktop de otimização de imagens para websites.

### ✨ Features

#### Core
- **Scan Recursivo**: Escaneia pastas até 10 níveis, ignora `node_modules`, `.git`, `dist`, etc
- **Manter Estrutura**: Preserva hierarquia de diretórios na saída
- **Modo Não-Destrutivo**: Nunca sobrescreve arquivos originais
- **Processamento em Lote**: Até 10.000 imagens por vez

#### Presets Web
- Hero Image (1920x1080, 85%)
- Blog Post (1200x630, 85%)
- Thumbnail (400x300, 80%)
- Mobile Optimized (800px, 80%)
- Avatar/Icon (256x256, 90%)
- Original Quality (95%)

#### Configurações
- Slider de qualidade 60-100%
- Formatos: WebP, PNG
- Recorte 1:1 (quadrado)
- Redimensionamento customizado

#### UX
- Drag & Drop de arquivos e pastas
- Atalhos: Ctrl+O (escanear), Delete (remover), Ctrl+Enter (converter)
- Barra de progresso em tempo real
- Relatório HTML com estatísticas

#### Relatório
- Total de arquivos processados
- Tamanho original vs final
- Economia em MB e %
- Status por arquivo (✓/✗)
- Top 10 maiores economias

### 🐛 Bugs Conhecidos
- Conversão pode ser lenta com >1000 imagens (será otimizado em V1.1)
- Relatório HTML não abre em alguns ambientes (fallback para TXT em V1.1)

### 📦 Dependências
- Python 3.8+
- ImageMagick 7+
- tkinterdnd2 (opcional, para drag & drop)

### 🚀 Instalação
```bash
pip3 install tkinterdnd2
sudo apt install imagemagick
python3 brjoy-converter
```

### 📊 Performance
- 1000 imagens: ~3-5min
- Economia média: 60-80%
- Formatos suportados: JPG, PNG, HEIC, BMP, TIFF, GIF, WebP, AVIF

### 🎯 Público-Alvo
- Desenvolvedores frontend (Next.js, Astro, Hugo, Vite)
- Agências web
- Freelancers

### 📝 Notas
- Primeira versão estável
- Testado com até 5.000 imagens
- Economia média de 73% em testes reais

---

## Roadmap

### V1.1 (Próxima)
- [ ] Processamento paralelo (threads)
- [ ] Botão "Cancelar" durante conversão
- [ ] Fallback TXT para relatório
- [ ] Filtros: ignorar <50KB, >10MB

### V2.0 (Q2 2026)
- [ ] CLI: `brjoy-img optimize ./public`
- [ ] Integração CI/CD (GitHub Actions)
- [ ] Modo watch (auto-convert)

### V3.0 (Q3 2026)
- [ ] Gerador de snippets `<picture>`
- [ ] Responsive variants (srcset)
- [ ] Deduplicação por hash

### V4.0 (Q4 2026)
- [ ] Plugin WordPress
- [ ] Integração Cloudflare Images
- [ ] API REST
