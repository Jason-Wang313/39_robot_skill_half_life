# Claims

## Main claim
A robot skill's deployment value is incomplete without a decay statistic such as skill half-life.

## Supported claims
- Frozen skills can lose success probability under latent physical drift.
- Calendar recalibration and sentinel-triggered rehearsal lengthen the measured half-life in the toy model.
- Reporting only initial success hides long-horizon maintenance cost.

## Unsupported claims
- No claim is made that the numerical half-lives transfer to real robots.
- No claim is made that sentinel-triggered rehearsal is the best adaptation algorithm.
- No claim is made that all skills decay monotonically in practice.
- V2 boundary: the 61-day sentinel result is censored by the 60-day window. With a 120-day window, sentinel-triggered rehearsal crosses the half-success threshold at 89.0 days.
