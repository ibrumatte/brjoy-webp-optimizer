# BrJoy WebP Optimizer

[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](https://github.com/ibrumatte/brjoy-webp-optimizer/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Tests](https://github.com/ibrumatte/brjoy-webp-optimizer/actions/workflows/test.yml/badge.svg)](https://github.com/ibrumatte/brjoy-webp-optimizer/actions/workflows/test.yml)

Desktop image optimizer with a modern 2026 UI (`pywebview + React/Tailwind`) and a Python conversion engine.

Release atual: **v1.4.0 (2026-03-03)**.

## Destaques da V1.4.0

- Filtro de extensões no scan (`png,jpg,webp` etc.) aplicado em scan de pasta e ingestão por seleção.
- Reprocessamento de falhas por item (`Reprocessar Erros`) no fim da conversão.
- Política de conflito de nome na saída:
  - `Versionar`
  - `Sobrescrever`
  - `Pular`
- Backup automático ao usar `Substituir no lugar`:
  - arquivo `.bak`
  - pasta `_backup`
- Aba de reports com ação `Copiar texto` do preview IA.
- Densidade fixa em `Compacto` por padrão.

## Arquitetura (Desktop WebView)

- `app/core`: motor de conversão e regras de saída.
- `app/services`: scan, report, history e settings.
- `app/bridge`: `DesktopAPI` para comunicação Python ↔ UI.
- `app/desktop`: bootstrap da janela `pywebview`.
- `frontend`: fonte React + Vite + Tailwind.
- `frontend/dist`: bundle estático usado em runtime.

## Funcionalidades

- Conversão em lote (WebP/PNG) com progresso e cancelamento.
- Scan recursivo com filtros e limites.
- Presets web.
- Qualidade, resize, crop 1:1, sharpen, brilho.
- Batch de múltiplos tamanhos.
- Manter estrutura / substituir no lugar.
- Reports no app (HTML, AI TXT, CSV, pasta) + histórico.
- PT-BR/EN-US com detecção automática + troca manual.
- Tema `system/light/dark`.
- Drag-and-drop com fallback por botões.

## Instalação (Runtime)

Requisitos:

- Python 3.8+
- ImageMagick (`convert`)
- `pywebview`

Instalação rápida:

```bash
git clone https://github.com/ibrumatte/brjoy-webp-optimizer.git
cd brjoy-webp-optimizer
./install.sh
./brjoy-converter
```

## Uso Rápido

1. Adicione arquivos ou use `Escanear Pasta`.
2. (Opcional) Defina `Filtro de extensões no scan`.
3. Ajuste formato/qualidade/opções avançadas.
4. Escolha estratégia de saída:
   - Manter estrutura
   - Substituir no lugar (+ backup automático opcional)
   - Política de conflito de nome
5. Clique em `Converter`.
6. Se houver erros, use `Reprocessar Erros`.

## Desenvolvimento

Node é necessário apenas para desenvolvimento/build do frontend.

```bash
cd frontend
npm install
npm run dev
npm run build
npm run test
```

O app desktop carrega `frontend/dist/index.html` localmente (sem servidor externo em runtime).

## Testes

```bash
./test.sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Dados Locais

- `~/.local/share/brjoy-image-converter/settings.json`
- `~/.local/share/brjoy-image-converter/history.txt`
- `~/.local/share/brjoy-image-converter/reports/*`

## License

MIT - see [LICENSE](LICENSE)
