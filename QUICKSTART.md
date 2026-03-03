# Quick Start

## 1) Install

```bash
git clone https://github.com/ibrumatte/brjoy-webp-optimizer.git
cd brjoy-webp-optimizer
./install.sh
```

## 2) Run

```bash
./brjoy-converter
```

## 3) First conversion

1. Click `Adicionar Arquivos` or `Escanear Pasta`.
2. (Optional) Use `Filtro de extensões no scan` (ex: `png,jpg,webp`).
3. Keep default `WebP` + quality `85%`.
4. Choose output strategy:
   - `Manter estrutura de pastas`
   - `Substituir no lugar` (with optional backup)
   - `Conflito de nome` (`Versionar`, `Sobrescrever`, `Pular`)
5. Click `Converter`.
6. If failures happen, click `Reprocessar Erros`.

## 4) Check reports

Open tab `Report` and use:

- `Abrir HTML`
- `Abrir AI TXT`
- `Abrir CSV`
- `Abrir Pasta`
- `Copiar texto`

Reports are stored in:

```text
~/.local/share/brjoy-image-converter/reports/
```

## Shortcuts

- `Ctrl+O` add files
- `Ctrl+Enter` convert
- `Esc` cancel
- `Ctrl+L` clear list

## Troubleshooting

`ImageMagick not found`:

```bash
sudo apt install imagemagick
```

`pywebview not found`:

```bash
python3 -m pip install --user pywebview
```
