# 🚀 BrJoy WebP Optimizer V1.3.0 - Launch Checklist

## Release Readiness

### Code & Quality
- [x] Core conversion flow hardened
- [x] Thread-safety issues addressed
- [x] Cancelation semantics corrected (`skipped` vs `errors`)
- [x] Output collision handling implemented
- [x] Preserve-structure flow validated
- [x] Batch resize behavior validated

### Testing
- [x] `py_compile` on core scripts
- [x] Functional quick test (`./test.sh`)
- [x] Non-GUI unit tests (`test-core-logic.py`)
- [x] CI workflow updated (Python 3.8 + 3.12)

### Documentation
- [x] `CHANGELOG.md` updated
- [x] `README.md` updated
- [x] `RELEASE.md` updated
- [x] `RELEASE_V1.3.md` created

---

## Publish Steps (30 min)

1. GitHub Release
- [ ] Create tag `v1.3.0`
- [ ] Open release page and paste `RELEASE.md`
- [ ] Attach screenshots/demo GIF (optional)

2. Repository Push
- [ ] Push commits to `main`
- [ ] Push tag `v1.3.0`

3. Announcement
- [ ] LinkedIn post
- [ ] Dev.to update note
- [ ] X/Twitter thread
- [ ] Reddit post in relevant communities

---

## Post-Release Monitoring (48h)

- [ ] Watch GitHub issues
- [ ] Verify CI runs on main and PRs
- [ ] Collect first user feedback
- [ ] Triage potential regressions

---

## Suggested Commands

```bash
# local gate
./test.sh

# release
git tag v1.3.0
git push origin main
git push origin v1.3.0
```
