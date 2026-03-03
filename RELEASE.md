# 🚀 BrJoy WebP Optimizer V1.3.0 - Release Notes

**Date:** 2026-03-03  
**Status:** ✅ Ready to publish

---

## What Changed in V1.3.0

### Reliability & Correctness
- Unified file model across all ingestion paths (scan, picker, drag/drop).
- Thread-safe conversion flow with UI updates synchronized through Tk main loop.
- Fixed `Ctrl+L` clear-list shortcut.
- Responsive cancellation during batch processing.
- Canceled jobs are now reported as `skipped` (not errors).

### Output Safety
- Real preserve-structure behavior in output folders.
- Output collision protection (`_1`, `_2`, ... suffixes).
- Batch widths always apply resize rules.
- Replace-in-place no longer creates unnecessary session folders.

### UX & Platform
- Cross-platform open-path support (Linux/macOS/Windows).
- Better drag/drop behavior in dark mode.
- Recursive folder add with limits and ignored directories.
- Pre-flight validation for invalid resize/batch combinations.

### Reporting & Security
- HTML report now escapes file/folder values.
- CSV export hardening against formula injection.

### Tests & CI
- New non-GUI unit suite: `test-core-logic.py`.
- Stronger `test.sh` with functional script execution and strict shell mode.
- GitHub Actions updated to:
  - `checkout@v4`
  - `setup-python@v5`
  - Python matrix: 3.8 and 3.12

---

## Validation Snapshot

Executed locally on 2026-03-03:

```bash
python3 -m py_compile brjoy-converter conversor_gui.py test-conversion.py test-core-logic.py
python3 test-core-logic.py
bash ./test.sh
```

Result: ✅ All checks passed (including 9 unit tests in `test-core-logic.py`).

---

## Upgrade Notes

```bash
git pull
./test.sh
./brjoy-converter
```

---

## Files Added/Updated (V1.3.0)

- `brjoy-converter`
- `launcher.sh`
- `conversor_gui.py`
- `test-core-logic.py` (new)
- `test-conversion.py`
- `test.sh`
- `.github/workflows/test.yml`
- `README.md`
- `CHANGELOG.md`

---

## Known Follow-ups

- Optional: modernize `conversor_gui.py` legacy flow to share the same core engine.
- Optional: add integration test for cancelation race conditions.

