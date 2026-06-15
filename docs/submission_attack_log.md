# Submission Attack Log

Generated: 2026-06-15 21:02:16 +01:00

## Attack Rounds

1. The original result was too small.
   - Action: expanded to 14 skills, 12 drift processes, 16 policies, 112 seeds, 301,056 seed rows, and 8,706,539,520 represented checks.
2. The half threshold is arbitrary.
   - Action: added 80%, 70%, 50%, 40%, and 30% threshold sensitivity.
3. The observation window can censor results.
   - Action: added horizon sensitivity and explicit censoring metrics.
4. Sparse observation cadence can delay detection.
   - Action: added 1-, 7-, 14-, and 30-day cadence stress.
5. Static success and final success can hide decay shape.
   - Action: added AUC, uptime, day-60/120/180/240 success, representative curves, and nonmonotonic discussion.
6. Maintenance cost can reverse rankings.
   - Action: added maintenance and evaluation cost metrics plus cost-aware uptime frontier.
7. Shock events require separate reporting.
   - Action: added shock loss and recovery lag metrics.
8. A policy can game half-life.
   - Action: added overfit rapid adaptation negative control.
9. Hardware evidence is missing.
   - Action: states analytic scope and adds a hardware deployment plan rather than overclaiming.
10. Visual/layout defects could hide problems.
   - Action: rendered the final Downloads PDF to PNGs and inspected contact sheet and figure pages.

## Final Stopping Point

The paper is final under the requested analytic full-scale standard. Remaining
future work is hardware deployment logs, trained policy implementations, and
statistical survival confidence intervals, all named as limitations.
