# 🎉 BrJoy WebP Optimizer V1.4.0

Release focada em **segurança de saída**, **recuperação de falhas** e **controle fino de scan** na nova UI desktop (WebView).

---

## 🚀 Destaques

- ✅ **Filtro de extensões no scan** (`png,jpg,webp`) em scan de pasta e ingestão por seleção.
- ✅ **Retry por item com falha** (`Reprocessar Erros`) sem reprocessar o lote inteiro.
- ✅ **Política de conflito de nome**: `Versionar`, `Sobrescrever`, `Pular`.
- ✅ **Backup automático** para `Substituir no lugar`:
  - `.bak`
  - `_backup`
- ✅ **Report tab** com botão **Copiar texto** no preview do relatório IA.

---

## 🧪 Qualidade

Validações locais executadas nesta release:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m py_compile app/core/conversion_engine.py app/bridge/desktop_api.py app/services/scan_service.py
node --check frontend/dist/assets/app.js
```

Resultado: **OK**.

---

## 📦 Upgrade

```bash
git pull
./test.sh
./brjoy-converter
```

---

## 📄 Changelog completo

Veja [CHANGELOG.md](CHANGELOG.md).
