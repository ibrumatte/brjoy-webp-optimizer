# BrJoy WebP Optimizer V1.4.0

Release focada em robustez operacional na UI desktop WebView.

## Highlights
- Filtro de extensões no scan (scan de pasta e ingestão por seleção).
- Reprocessamento de falhas por item (`Reprocessar Erros`).
- Política de conflito de nome (`version`, `overwrite`, `skip`).
- Backup automático para `substituir no lugar` (`.bak` ou `_backup`).
- Report tab com ação `Copiar texto` no preview IA.

## Validation
- `python3 -m unittest discover -s tests -p 'test_*.py'` ✅ (`30 tests`)
- `python3 -m py_compile app/core/conversion_engine.py app/bridge/desktop_api.py app/services/scan_service.py` ✅
- `node --check frontend/dist/assets/app.js` ✅

## Recommended Announcement Line
"V1.4.0 saiu: retry de falhas, backup automático para replace-in-place, política de conflito de nomes e filtro de extensões no scan."
