# 🚀 BrJoy WebP Optimizer V1.4.0 - Release Notes

**Date:** 2026-03-03  
**Status:** ✅ Ready to publish

---

## What Changed in V1.4.0

### Safety & Recovery
- Added backup support for `replace in place`:
  - `.bak` file strategy
  - `_backup` folder strategy
- Added output name conflict policies:
  - `version` (default)
  - `overwrite`
  - `skip`

### Conversion Flow
- Added `Retry Errors` button to reprocess only failed items.
- Retry starts a new conversion job with only errored entries.

### Scan Quality
- Added extension filter for scan and collected paths.
- Input accepts `png,jpg,webp` or `.png,.jpg,.webp`.

### Report UX
- AI report preview now includes `Copy Text` action in Report tab.

### Tests & Contract Coverage
- Added `tests/test_scan_service.py`.
- Added new conversion engine scenarios for conflict/backup behavior.
- Added desktop API validation tests for invalid extension payloads.
- Local validation snapshot:
  - `python3 -m unittest discover -s tests -p 'test_*.py'` ✅ (`30 tests`)
  - `python3 -m py_compile app/core/conversion_engine.py app/bridge/desktop_api.py app/services/scan_service.py` ✅
  - `node --check frontend/dist/assets/app.js` ✅

---

## Upgrade Notes

```bash
git pull
./test.sh
./brjoy-converter
```

---

## Files Added/Updated (V1.4.0)

- `app/services/scan_service.py`
- `app/bridge/desktop_api.py`
- `app/core/conversion_engine.py`
- `frontend/dist/index.html`
- `frontend/dist/assets/app.js`
- `tests/test_scan_service.py` (new)
- `tests/test_conversion_engine.py`
- `tests/test_desktop_api.py`
- `README.md`
- `CHANGELOG.md`
- `GITHUB_RELEASE.md`
- `QUICKSTART.md`
- `GUIDE.md`

---

## Known Follow-ups

- Mirror these runtime (`frontend/dist`) changes back to `frontend/src` to keep source and bundle 100% synchronized.
- Add E2E smoke covering `Retry Errors` with mixed success/failure set.
