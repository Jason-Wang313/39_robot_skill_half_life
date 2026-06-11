# Hostile Prior Work

## Continual and lifelong robot learning
This line can argue that robots already adapt over time. The paper's boundary is different: it asks for a scalar decay diagnostic that can be reported even for frozen or rarely updated skills.

## Sim-to-real and domain adaptation
These methods reduce the initial deployment gap. They do not remove post-deployment drift caused by tool wear, sensor calibration changes, payload shifts, surface aging, or updated fixtures.

## Calibration and maintenance
Calibration procedures are direct competitors. The paper positions skill half-life as a trigger and reporting metric for when such procedures are needed, not as a replacement.

## Robust policies
Robust policies can lengthen the half-life. The diagnostic is still useful because it measures whether that promise survives over calendar time under a repeated drift process.

## Continual reinforcement learning forgetting
Forgetting focuses on loss of old tasks while learning new ones. Skill half-life focuses on loss of the same task under physical and distributional drift.
