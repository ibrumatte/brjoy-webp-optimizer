# BrJoy WebP Optimizer V1.3.0

Release focused on hardening, correctness, and release-quality automation.

## Highlights
- Thread-safe conversion pipeline.
- Correct skip/error accounting under cancellation.
- Collision-safe output generation.
- Preserve-structure behavior fully implemented.
- Batch resize guaranteed for all configured widths.
- Cross-platform open-path support.
- Core non-GUI test suite + CI matrix (Python 3.8 and 3.12).

## Validation
- `python3 -m py_compile ...` ✅
- `python3 test-core-logic.py` ✅
- `bash ./test.sh` ✅

## Recommended Announcement Line
"V1.3.0 is out: safer conversions, better cancelation semantics, collision-proof output naming, and stronger CI/test coverage."
