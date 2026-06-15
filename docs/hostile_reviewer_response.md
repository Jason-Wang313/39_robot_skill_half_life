# Hostile Reviewer Response

## Short Response

The paper is no longer a small toy drift note. V3 evaluates robot skill
half-life as a reporting diagnostic across 14 skill families, 12 drift
processes, 16 policies, 112 seeds, 5 thresholds, 4 horizons, and cadence,
shock-recovery, and cost stresses.

## Strongest Objection

"Half-life is just an arbitrary scalar. It depends on the threshold, horizon,
censoring, and evaluation cadence."

## Response

Accepted and tested. The paper's central claim is that half-life is meaningful
only when those quantities are reported. The suite explicitly varies threshold,
horizon, cadence, drift process, and maintenance cost. The result is a reporting
protocol, not a claim that one scalar replaces the full decay curve.

## Revised Claim

Robot skill half-life is a survival-style diagnostic for deployed manipulation
policies. It should be reported with full curve, censoring, threshold, horizon,
cadence, uncertainty, drift process, shock recovery, and cost. The analytic
numbers are stress-test evidence for the protocol, not hardware lifetime claims.
