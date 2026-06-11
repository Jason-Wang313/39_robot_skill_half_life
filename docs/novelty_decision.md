# Novelty Decision

## Chosen thesis
Robot skills should be reported with a half-life: the time until the deployed success probability falls below half of its initial value under a specified drift process.

## Field assumption broken
The broken assumption is that a learned robot skill is a static artifact once it clears a benchmark. In deployment, the embodiment and workspace continue to change.

## Mechanism
Define an evaluation protocol over repeated days or cycles. Estimate initial success, track the decay curve, and report the first time the curve crosses half of the initial success.

## Why this is worth keeping
The idea is small but sharp. It makes maintenance, rehearsal, recalibration, and robust policy claims comparable in the same units: extra days or cycles of usable skill life.

## Scope limits
The paper gives a diagnostic and a simulation, not a universal law about real robot aging. A real deployment study would be the next step.
