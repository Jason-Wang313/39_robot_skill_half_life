# Final Audit

Generated: 2026-06-13 08:14:22 +01:00

## Decision

Workshop-only / strong-revise. The metric is clear and the simulator is reproducible, but the paper remains a deterministic toy drift model with no real robot deployment, no survival-analysis baseline, no nonmonotonic curves, and no empirical estimate of measurement cost.

## Thesis

Robot skill reports should include a drift-aware lifetime statistic, not only initial benchmark success.

## Positive Evidence

- Frozen skill mean half-life: 21.2 days.
- Calendar recalibration mean half-life: 21.8 days, day-60 success 0.31.
- Sentinel-triggered rehearsal main-table result: censored at 61.0 days with day-60 success 0.62.
- Oracle adaptation main-table result: censored at 61.0 days with day-60 success 0.70.

## V2 Negative Evidence

- The half threshold and observation window matter.
- Sentinel-triggered rehearsal is not infinite durability: under a 120-day window, half-success crossing is 89.0 days with no censoring.
- A stricter 80% threshold crosses much earlier: frozen 7.4 days, calendar recalibration 6.3 days, sentinel rehearsal 32.8 days, oracle adaptation 50.8 days.
- The supported claim is therefore a reporting protocol with threshold/window/censoring disclosure, not a universal scalar metric.

## Remaining Weaknesses

- Hand-coded deterministic drift law.
- No real manipulation skill or measured deployment drift.
- No statistical survival model or confidence intervals.
- No nonmonotonic recovery curves.
- No cost model for repeated evaluation.

## Reproducibility Artifacts

- `scripts/skill_half_life_sim.py`
- `docs/skill_half_life_timeseries.csv`
- `docs/skill_half_life_summary.csv`
- `docs/threshold_sensitivity_stress.csv`
- `docs/threshold_sensitivity_stress_table.tex`
- `scripts/build_pdf.ps1`

## Artifact Policy

- Canonical PDF path: `C:/Users/wangz/Downloads/39.pdf`
- GitHub URL: `https://github.com/Jason-Wang313/39_robot_skill_half_life`
- Visible Desktop copy: intentionally absent in v2.
- Local generated paper PDF: removed after v2 build.
