# Guia de Uso - BrJoy WebP Optimizer

## Instalação

```bash
./install.sh
./brjoy-converter
```

Dependências de runtime:

- Python 3.8+
- ImageMagick
- pywebview

## Fluxo do Conversor

1. Adicione arquivos (`Adicionar Arquivos`) ou escaneie pasta (`Escanear Pasta`).
2. (Opcional) Defina `Filtro de extensões no scan` (ex: `png,jpg,webp`).
3. Configure preset/formato/qualidade/opções avançadas.
4. Em estratégia de saída, defina:
   - `Manter estrutura de pastas`.
   - `Substituir no lugar` (opcional).
   - `Backup automático` (`.bak` ou `_backup`) quando substituir no lugar.
   - `Conflito de nome`: `Versionar`, `Sobrescrever` ou `Pular`.
5. Clique em `Converter`.
6. Acompanhe progresso por item e status geral.
7. Em caso de erros, use `Reprocessar Erros`.

## Aba Report

- Lista sessões de conversão recentes.
- Mostra preview do `AI-CODE-UPDATE.txt`.
- Ações rápidas:
  - Abrir HTML
  - Abrir AI TXT
  - Abrir CSV
  - Abrir pasta do report
  - Copiar texto

Reports são salvos em:

```text
~/.local/share/brjoy-image-converter/reports/
```

## Atalhos

- `Ctrl+O`: adicionar arquivos
- `Ctrl+Enter`: iniciar conversão
- `Esc`: cancelar conversão
- `Ctrl+L`: limpar lista

## Idioma, tema e densidade

- Locale detectado automaticamente (`pt-BR`/`en-US`).
- Toggle manual no header (persistido em `settings.json`).
- Tema `light`, `dark` ou `system`.
- Densidade padrão fixa em `compact`.

## Desenvolvimento Frontend

```bash
cd frontend
npm install
npm run dev
npm run build
npm run test
```

O app desktop usa o bundle estático em `frontend/dist`.
