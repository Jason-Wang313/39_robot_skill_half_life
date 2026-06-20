# Final Audit

Generated: 2026-06-15 21:02:16 +01:00

## Decision

Final v3 full-scale verified. The manuscript is now a 25-page analytic
submission-scale paper with a deterministic survival suite, expanded protocol,
figures, tables, stress tests, limitations, appendices, reproducibility records,
and visual PDF verification.

## Thesis

Robot skills should be reported as temporal deployment objects. Initial success
does not identify how quickly a skill expires under drift; reports must include
half-life, full decay curve, threshold, horizon, censoring, cadence, shock
recovery, maintenance policy, and cost.

## Positive Evidence

- Full-scale suite covers 14 skills, 12 drift processes, 16 policies, and 112 seeds.
- Runner generated 301,056 seed rows and 2,688 aggregate rows.
- Represented reporting checks: 8,706,539,520.
- Frozen skill: mean half-life 39.6 days, day-240 success 0.014.
- Calendar recalibration: mean half-life 59.1 days.
- Sentinel rehearsal: mean half-life 70.6 days.
- Uncertainty rehearsal: mean half-life 101.7 days.
- Meta-adaptation: mean half-life 128.6 days.
- Human-in-loop repair: mean half-life 168.5 days, high maintenance cost.
- Oracle maintenance: censored at 241.0 days.

## Remaining Weaknesses

- No real robot deployment data.
- No trained policy implementations for the analytic proxies.
- No hardware-derived survival confidence intervals.
- Cost units are normalized analytic proxies.
- The exact lifetimes are not physical claims.

## Reproducibility Artifacts

- `scripts/run_full_scale_skill_half_life_suite.py`
- `results/full_scale/seed_survival_metrics.csv`
- `results/full_scale/aggregate_survival_metrics.csv`
- `results/full_scale/threshold_sensitivity.csv`
- `results/full_scale/cadence_sensitivity.csv`
- `results/full_scale/shock_recovery_metrics.csv`
- `results/full_scale/experiment_summary.json`
- `results/full_scale/experiment_validation.json`
- `results/full_scale/validation.json`
- `results/full_scale/*.tex`
- `figures/full_scale/*.pdf`
- `scripts/build_pdf.ps1`

## Artifact Policy

- Canonical PDF path: `C:/Users/wangz/Downloads/39.pdf`
- Pages: 25
- File size: 434,913 bytes
- SHA256: `A8A9CCC28B8996DF055CE60037828F3513107585CE1BADB5C867D332ADB08B2E`
- Local generated paper PDF: absent after canonical build.
- Visual render check: passed on the final Downloads PDF.
- VLA-style link-box check: passed on pages 2, 5, 6, 7, 8, 16, 21, and 22 with 28 green citation boxes, 14 red internal-reference boxes, and 42 visible one-point borders.
