import csv
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def success_probability(policy, day, trial):
    rng = random.Random(39000 + trial)
    base = 0.91 + rng.uniform(-0.025, 0.025)
    floor = 0.035 + rng.uniform(0.0, 0.025)
    drift = 0.034 + rng.uniform(-0.004, 0.004)
    shock = 0.0
    if day >= 21:
        shock += 0.030
    if day >= 43:
        shock += 0.045

    if policy == "frozen":
        effective_age = day
        mitigation = 1.0
    elif policy == "calendar_recalibration":
        effective_age = (day % 21) + 0.18 * day
        mitigation = 0.78
    elif policy == "sentinel_rehearsal":
        effective_age = day * 0.34
        if day >= 18:
            effective_age -= 4.5
        if day >= 39:
            effective_age -= 5.5
        effective_age = max(0.0, effective_age)
        mitigation = 0.35
    elif policy == "oracle_adapt":
        effective_age = day * 0.13
        mitigation = 0.12
    else:
        raise ValueError(policy)

    p = floor + (base - floor) * math.exp(-drift * effective_age) - shock * mitigation
    return max(0.0, min(0.99, p))


def main():
    policies = ["frozen", "calendar_recalibration", "sentinel_rehearsal", "oracle_adapt"]
    days = list(range(0, 61))
    trials = range(48)
    rows = []
    summary = []
    for policy in policies:
        half_lives = []
        day60 = []
        aucs = []
        for trial in trials:
            p0 = success_probability(policy, 0, trial)
            half_threshold = 0.5 * p0
            first_half = None
            probs = []
            for day in days:
                p = success_probability(policy, day, trial)
                probs.append(p)
                rows.append({"policy": policy, "trial": trial, "day": day, "success_probability": f"{p:.6f}"})
                if first_half is None and p <= half_threshold:
                    first_half = day
            half_lives.append(first_half if first_half is not None else 61)
            day60.append(probs[-1])
            aucs.append(sum(probs) / len(probs))
        summary.append(
            {
                "policy": policy,
                "mean_half_life_days": sum(half_lives) / len(half_lives),
                "censored_fraction": sum(1 for x in half_lives if x == 61) / len(half_lives),
                "day60_success": sum(day60) / len(day60),
                "mean_success_auc": sum(aucs) / len(aucs),
            }
        )

    DOCS.mkdir(exist_ok=True)
    with (DOCS / "skill_half_life_timeseries.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["policy", "trial", "day", "success_probability"])
        writer.writeheader()
        writer.writerows(rows)
    with (DOCS / "skill_half_life_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["policy", "mean_half_life_days", "censored_fraction", "day60_success", "mean_success_auc"],
        )
        writer.writeheader()
        for row in summary:
            writer.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in row.items()})


if __name__ == "__main__":
    main()
