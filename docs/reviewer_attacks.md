# Reviewer Attacks

1. The experiment is a toy simulation, not a robot deployment.
2. The half-life threshold is arbitrary.
3. Existing lifelong learning and calibration work already studies drift.
4. The diagnostic may be expensive to estimate for slow physical processes.
5. Nonmonotonic learning curves can make a single half-life ambiguous.
6. The half threshold and observation window can change the conclusion.

## Planned responses
The paper explicitly frames half-life as a reporting diagnostic. The threshold can be changed, but the core requirement remains: deployment papers should report how quickly competence decays, not only how high it starts.

V2 response: add threshold/horizon sensitivity. The main sentinel value of 61.0 is censored at 60 days, while a 120-day window yields 89.0 days. The paper now requires reporting threshold, observation window, censoring flag, and full curve.
