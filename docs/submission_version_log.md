# Submission Version Log

## v1

- Recovered literature sweep, deterministic toy drift simulator, manuscript, audit docs, and numbered PDF.
- Main result: frozen skill half-life 21.2 days; sentinel-triggered rehearsal censored at 61.0 days with day-60 success 0.62.

## v2

- Added explicit submission-hardening version marker in the paper.
- Removed final-copy marker.
- Added `--stress-only` simulator mode.
- Added `docs/threshold_sensitivity_stress.csv` and `docs/threshold_sensitivity_stress_table.tex`.
- Added 120-day horizon and 80% threshold sensitivity.
- Narrowed claim to threshold/window/censoring-aware reporting protocol.
- Added canonical Downloads-only PDF build script.

## v3

- Wrote `docs/full_scale_execution_plan.md` before changing the paper.
- Added `scripts/run_full_scale_skill_half_life_suite.py`.
- Generated 301,056 seed rows and 2,688 aggregate rows.
- Represented 8,706,539,520 deployment-success reporting checks.
- Compared 16 policies across 14 skills, 12 drift processes, and 112 seeds.
- Added threshold, cadence, shock recovery, cost, policy, skill, and drift stress artifacts.
- Added full-scale figures and tables under `figures/full_scale/` and `results/full_scale/`.
- Rewrote `main.tex` into a 25-page final manuscript with appendices.
- Exported canonical final PDF to `C:/Users/wangz/Downloads/39.pdf`.
- Verified final PDF hash, page count, log cleanliness, text markers, local `main.pdf` absence, and visual render.

Decision: final v3 full-scale verified.
