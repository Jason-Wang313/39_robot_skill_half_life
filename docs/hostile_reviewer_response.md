# Hostile Reviewer Response

## Short Response

The paper proposes a reporting diagnostic, not a new adaptation algorithm. The diagnostic is useful only when the drift process, threshold, observation window, and censoring rule are disclosed.

## Strongest Objection

The main sentinel result is censored at the end of a 60-day window, so the table could be misread as infinite durability.

## Response

Accepted. The v2 stress extends the window to 120 days. Sentinel-triggered rehearsal crosses the half-success threshold at 89.0 days, while oracle adaptation remains censored at 121.0 days. A stricter 80% threshold also crosses much earlier, showing why full curves and threshold sensitivity must be reported.

## Revised Claim

Skill half-life is a useful compact diagnostic when reported with its threshold, observation window, censoring flag, and full decay curve. It is not a universal scalar law of robot skill aging.

