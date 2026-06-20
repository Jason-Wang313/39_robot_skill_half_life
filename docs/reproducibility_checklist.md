# Reproducibility Checklist

- [x] Full-scale command: `python scripts/run_full_scale_skill_half_life_suite.py`
- [x] Build command: `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`
- [x] Seed-level CSV: `results/full_scale/seed_survival_metrics.csv`
- [x] Aggregate CSV: `results/full_scale/aggregate_survival_metrics.csv`
- [x] Threshold CSV: `results/full_scale/threshold_sensitivity.csv`
- [x] Cadence CSV: `results/full_scale/cadence_sensitivity.csv`
- [x] Shock recovery CSV: `results/full_scale/shock_recovery_metrics.csv`
- [x] Summary JSON: `results/full_scale/experiment_summary.json`
- [x] Runner validation JSON: `results/full_scale/experiment_validation.json`
- [x] Final artifact validation JSON: `results/full_scale/validation.json`
- [x] Representative decay curve CSV: `results/full_scale/representative_decay_curve.csv`
- [x] LaTeX tables: `results/full_scale/full_scale_*.tex`
- [x] Figures: `figures/full_scale/*.pdf`
- [x] Canonical PDF path: `C:/Users/wangz/Downloads/39.pdf`
- [x] Canonical PDF page count: 25
- [x] Canonical PDF SHA256: `A8A9CCC28B8996DF055CE60037828F3513107585CE1BADB5C867D332ADB08B2E`
- [x] Local generated `main.pdf` removed after build.
- [x] Final PDF rendered to PNGs and visually checked.
- [x] VLA-style link-box QA passed on pages 2, 5, 6, 7, 8, 16, 21, and 22.
- [x] Log scan passed for fatal errors, undefined references, unresolved citations, citation-change warnings, and overfull boxes.
- [ ] Pinned package environment.
- [ ] Continuous integration.

The experiment is deterministic and RAM-light: seed rows are streamed to disk,
aggregate accumulators are kept compact, and dense daily trajectories are stored
only for representative curves.
