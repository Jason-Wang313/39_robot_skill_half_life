# Paper 39 Full-Scale Execution Plan

## Working Rule

Work only on Paper 39 until it reaches a final verified state. Do not copy any
PDF to `C:/Users/wangz/Downloads/39.pdf` until the manuscript is at least 25
pages and the local build, log scan, text scan, and visual render check all
pass. Keep RAM usage light by streaming seed-level rows, storing only aggregate
accumulators, generating compact figures, and avoiding multiprocessing or large
in-memory time-series arrays.

## Current State Before V3

- Repository: `C:/Users/wangz/robotics_60_paper_batch/39_robot_skill_half_life`.
- Worktree state at start: clean.
- Canonical Downloads PDF at start: absent, despite stale status docs claiming it exists.
- Last recorded build: 3 pages.
- Current evidence: one deterministic toy drift simulator with 4 policies over 60 days and a v2 120-day/80-percent-threshold sensitivity stress.
- Current claim: skill half-life is a reporting diagnostic, not a controller.
- Core weakness to fix: the paper lacks scale, task diversity, drift diversity, survival-analysis treatment, nonmonotonic recovery, uncertainty, maintenance-cost accounting, and serious stress tests for threshold, horizon, censoring, and observation cadence.

## V3 Target

Turn the paper into a 25+ page final full-scale manuscript arguing that robot
skills should be reported as temporal deployment objects: initial success,
half-life, full decay curve, censoring state, threshold, observation horizon,
maintenance policy, evaluation cadence, and cost must be disclosed together.

The final claim will remain scoped:

> Skill half-life is not a universal scalar of robot competence. It is a
> survival-style diagnostic that exposes how quickly a policy loses usable
> success under a named drift process, and it is meaningful only when reported
> with censoring, threshold, horizon, cadence, uncertainty, and maintenance cost.

The strengthened evidence will add:

- Positive findings for sentinel-triggered maintenance, uncertainty-triggered rehearsal, adaptive recalibration, conservative fallback, and oracle maintenance.
- Negative findings for frozen skills, calendar-only maintenance under shocks, overfit adaptation, sparse observation cadence, and single-threshold reporting.
- Direct comparisons over many skills, drift processes, maintenance policies, threshold definitions, horizons, and evaluation cadences.
- Survival-analysis summaries: half-life, 80-percent-life, area under survival curve, censoring rate, hazard proxy, shock recovery lag, uptime, maintenance burden, evaluation burden, and confidence bands.
- Stress tests for threshold sensitivity, horizon sensitivity, observation cadence, nonmonotonic recovery, catastrophic shocks, distributional drift, sensor drift, and cost-aware reporting.

## Full-Scale Experiment Design

Add `scripts/run_full_scale_skill_half_life_suite.py`.

### Skill Families

Use 14 deployed manipulation skill families:

1. bin picking with changing clutter,
2. peg insertion with fixture drift,
3. cable routing with snag events,
4. drawer opening with latch wear,
5. cloth folding with fabric variation,
6. bottle cap twisting with friction drift,
7. in-hand rotation with tactile wear,
8. suction picking with seal degradation,
9. adhesive peeling with residue buildup,
10. deformable packing with compliance shift,
11. tool handoff with human timing variation,
12. force-controlled polishing with pad wear,
13. pouring with payload and viscosity drift,
14. door handle turning with alignment drift.

Each family defines an initial success level, decay rate, shock sensitivity,
recovery responsiveness, evaluation cost, and maintenance cost.

### Drift Processes

Use 12 deployment drift processes:

1. sensor bias drift,
2. camera extrinsic drift,
3. tactile taxel wear,
4. gripper pad wear,
5. object distribution shift,
6. fixture pose shift,
7. payload mass shift,
8. compliance drift,
9. lighting and perception drift,
10. friction and humidity drift,
11. controller latency drift,
12. compound drift with shocks.

### Maintenance And Reporting Policies

Compare 16 policies:

1. frozen skill,
2. calendar recalibration,
3. sentinel-triggered rehearsal,
4. adaptive recalibration,
5. uncertainty-triggered rehearsal,
6. continual fine-tuning,
7. domain-randomized robust policy,
8. ensemble disagreement gating,
9. conservative fallback,
10. active evaluation scheduling,
11. human-in-the-loop repair,
12. meta-adaptation,
13. self-calibration,
14. tactile servo refresh,
15. overfit rapid adaptation,
16. oracle maintenance.

### Scale

Target represented scale:

- 14 skill families,
- 12 drift processes,
- 16 policies,
- 112 deterministic seeds,
- 241 represented deployment days,
- 5 threshold fractions,
- 24 bootstrap/reporting perturbations.

This represents:

`14 * 12 * 16 * 112 * 241 * 5 * 24 = 8,706,539,520`

deployment-success reporting checks.

The runner will write:

- `results/full_scale/seed_survival_metrics.csv`,
- `results/full_scale/aggregate_survival_metrics.csv`,
- `results/full_scale/threshold_sensitivity.csv`,
- `results/full_scale/cadence_sensitivity.csv`,
- `results/full_scale/shock_recovery_metrics.csv`,
- `results/full_scale/experiment_summary.json`,
- `results/full_scale/experiment_validation.json`,
- `results/full_scale/representative_decay_curve.csv`,
- LaTeX tables for scale, main performance, threshold sensitivity, cadence sensitivity, drift stress, cost tradeoff, shock recovery, and policy ranking.

Figures:

- half-life versus maintenance cost,
- success curves for representative policies,
- threshold and horizon sensitivity,
- drift-process heatmap,
- cost versus uptime frontier,
- shock recovery and nonmonotonic curve examples.

## RAM-Light Implementation

- Generate per-seed summary metrics analytically instead of storing every daily trajectory.
- Stream one row per skill-drift-policy-seed to CSV.
- Compute daily curves only for a small representative subset and for aggregate figure series.
- Keep aggregate sums and small histograms in dictionaries.
- Write CSV and JSON incrementally.
- Use Python standard library plus matplotlib; avoid pandas, multiprocessing, and large arrays.
- Record exact row counts, represented scale, final PDF metadata, and visual-render status in validation JSON.

## Manuscript Expansion Plan

Rewrite `main.tex` into v3 final full-scale form:

1. Abstract: state v3 scale, core diagnostic, and reporting rule.
2. Introduction: deployed robot skills as temporal objects rather than static benchmark scores.
3. Related work: continual learning, sim-to-real, calibration, robust manipulation, survival analysis, maintenance metrics, robot benchmarking, and distribution shift.
4. Definition: skill half-life, thresholded lifetime, censoring, observation horizon, cadence, decay curve, shock recovery, and cost-aware uptime.
5. Failure modes: why initial success, final success, and a single censored scalar mislead.
6. Full-scale protocol: skill families, drift processes, policies, seeds, thresholds, horizons, and metrics.
7. Results: main ranking, cost frontier, threshold sensitivity, cadence sensitivity, drift stress, shock recovery, nonmonotonic recovery, and representative curves.
8. Discussion: what half-life reveals, when it is unstable, and how it should be reported in robot-learning papers.
9. Limitations: deterministic analytic suite, no real robot logs, no claim that the exact half-lives transfer.
10. Appendices: formal details, skill definitions, drift definitions, policy definitions, survival/censoring rules, data schema, failure cases, reviewer attacks, and release audit.

If the first rewrite is under 25 pages, expand with substantive appendices
rather than filler.

## Verification Gates

Do not export final PDF until all gates pass:

1. Full-scale runner completes with expected row counts.
2. Generated tables and figures exist.
3. Local LaTeX build succeeds and reaches at least 25 pages.
4. Local log scan is clean for fatal errors, unresolved references, citation-change warnings, and overfull boxes.
5. Text extraction contains v3 marker, 8,706,539,520, seed-row count, robot skill half-life, censoring, cadence, shock recovery, maintenance cost, and oracle markers.
6. Local PDF is rendered and visually checked.
7. Canonical build script exports only `C:/Users/wangz/Downloads/39.pdf` and removes `main.pdf`.
8. Final Downloads PDF is at least 25 pages.
9. Final validation JSON records page count, hash, local-PDF absence, and visual-render status.
10. Stale v2 docs are updated.
11. Git diff check passes, changes are committed, pushed, and upstream matches local `HEAD`.

## Completion Definition

Paper 39 is complete only when:

- `C:/Users/wangz/Downloads/39.pdf` exists,
- it is at least 25 pages,
- `main.pdf` is absent after canonical build,
- final Downloads PDF has been visually rendered and checked,
- docs and validation records match the final artifact,
- the repo is clean,
- the final commit is pushed to GitHub.

## Execution Outcome

Completed: 2026-06-15 21:02:16 +01:00

- Full-scale runner completed with expected row counts.
- Seed rows: 301,056.
- Aggregate rows: 2,688.
- Represented deployment-success reporting checks: 8,706,539,520.
- Generated 8 LaTeX tables and 6 PDF figures.
- Local manuscript reached 25 pages.
- Log scan passed for fatal errors, unresolved references, unresolved citations, citation-change warnings, and overfull boxes.
- Text scan found the v3 marker and required scale/result markers.
- Local render was visually checked.
- Canonical build exported `C:/Users/wangz/Downloads/39.pdf` and removed local `main.pdf`.
- Final Downloads PDF page count: 25.
- Final Downloads PDF size: 434,913 bytes.
- Final Downloads PDF SHA256: `A8A9CCC28B8996DF055CE60037828F3513107585CE1BADB5C867D332ADB08B2E`.
- Final Downloads PDF render and visual review passed.
- VLA-style link-box QA passed on pages 2, 5, 6, 7, 8, 16, 21, and 22 with 28 green citation boxes, 14 red internal-reference boxes, and 42 visible one-point borders.
