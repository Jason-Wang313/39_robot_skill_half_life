# Novelty Decision

## Chosen Thesis

Robot manipulation skills should be reported as temporal deployment objects.
Initial success and final success are incomplete without a drift-aware lifetime
statistic, the full decay curve, censoring, horizon, cadence, maintenance, and
cost.

## Field Assumption Broken

The broken assumption is that a trained or adapted robot skill can be summarized
by a static benchmark score. Deployment turns a skill into a survival process:
it persists, decays, recovers, or expires under changing physical conditions.

## Central Mechanism

Use robot skill half-life as a survival-style diagnostic. The metric asks when a
policy's success under a named drift process first crosses a threshold relative
to its initial success, and it requires censoring, threshold, horizon, cadence,
curve, and cost metadata.

## Why This Is Novel Enough

Nearby work studies continual learning, robust manipulation, adaptation,
calibration, and sim-to-real transfer. This paper does not propose another
controller. It makes the deployment time axis reportable and adversarially tests
how threshold, horizon, cadence, drift, shock recovery, and maintenance cost
change the interpretation of a skill claim.

## Rejected Directions

- New adaptation algorithm as primary contribution.
- Static benchmark-only framing.
- Unscoped claim that one half-life scalar is sufficient.
- Hardware lifetime claim without hardware logs.
- Final-success-only evaluation.

## Final Direction

The final paper is a reporting and evaluation contribution:
1. Define thresholded skill lifetime, half-life, censoring, cadence, AUC, uptime, shock recovery, and cost-aware durability.
2. Prove that identical initial success does not identify deployment lifetime.
3. Evaluate the diagnostic across a full-scale deterministic survival suite.
4. Show where half-life helps and where it is unstable unless paired with the full curve and metadata.
5. Provide a reporting checklist for deployed robot skills.
