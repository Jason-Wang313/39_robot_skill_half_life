# Claims

## Main Claim

A robot skill's deployment value is incomplete without a temporal decay report.
Initial success must be paired with half-life, full decay curve, threshold,
censoring, horizon, cadence, maintenance policy, and cost.

## Strengthened V3 Claim

Robot skill half-life is not a universal scalar of robot competence. It is a
survival-style reporting diagnostic that exposes how quickly a policy loses
usable success under a named drift process. It is meaningful only when reported
with censoring, threshold, horizon, cadence, uncertainty, and maintenance cost.

## Supporting Findings

- Full-scale suite: 14 skills, 12 drift processes, 16 policies, 112 seeds, 301,056 seed rows, and 8,706,539,520 represented reporting checks.
- Frozen skills have mean restricted half-life 39.6 days and day-240 success 0.014.
- Calendar recalibration reaches 59.1 days but remains brittle to shocks.
- Sentinel rehearsal reaches 70.6 days.
- Uncertainty-triggered rehearsal reaches 101.7 days.
- Meta-adaptation reaches 128.6 days.
- Human-in-loop repair reaches 168.5 days but with high maintenance cost.
- Oracle maintenance is right-censored at 241.0 days and serves only as an upper bound.
- Threshold, cadence, drift, shock recovery, and cost stresses change interpretation.

## Formal Claim Status

- The paper includes a proposition showing that identical initial success does not identify deployment lifetime.
- The empirical suite evaluates the reporting diagnostic across policy, skill, drift, threshold, cadence, and cost variation.
- The paper does not claim that analytic lifetimes transfer numerically to real robots.

## Honest Limits

- The suite is deterministic and analytic rather than hardware deployment.
- Policies are controlled proxies, not trained robot policies.
- The results support a reporting protocol and stress-test standard, not a new deployed controller.
