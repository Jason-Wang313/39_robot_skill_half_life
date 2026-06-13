# Submission Attack Log

Generated: 2026-06-13 08:09:10 +01:00

## Attack Rounds

1. Existing continual learning and calibration already study drift.
   - Action: narrowed the contribution to reporting protocol and lifetime diagnostic.
2. The toy simulator is not a deployment.
   - Action: marked workshop-only / strong-revise.
3. The half threshold is arbitrary.
   - Action: added threshold sensitivity at 80% and 50% of initial success.
4. The observation window can create a false non-crossing impression.
   - Action: added 120-day horizon stress; sentinel crosses at 89.0 days.
5. A single scalar hides curve shape.
   - Action: manuscript now requires reporting the full curve, threshold, window, and censoring rule.
6. Calendar recalibration and sentinel policies are hand-coded.
   - Action: stated no algorithmic optimality claim.
7. Artifact policy included tracked `main.pdf`.
   - Action: added canonical build script and removed local generated paper PDF.

## Honest Stopping Point

Recoverable overclaims are fixed. Remaining blockers require real deployment data, survival-analysis treatment, nonmonotonic curves, and measurement-cost modeling.
