import csv
import math
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
POLICIES = ["frozen", "calendar_recalibration", "sentinel_rehearsal", "oracle_adapt"]


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


def crossing_summary(policy, threshold_fraction, horizon_days, trials=range(48)):
    crossings = []
    end_success = []
    for trial in trials:
        p0 = success_probability(policy, 0, trial)
        threshold = threshold_fraction * p0
        first_crossing = None
        for day in range(horizon_days + 1):
            p = success_probability(policy, day, trial)
            if first_crossing is None and p <= threshold:
                first_crossing = day
        crossings.append(first_crossing if first_crossing is not None else horizon_days + 1)
        end_success.append(success_probability(policy, horizon_days, trial))
    return {
        "policy": policy,
        "threshold_fraction": threshold_fraction,
        "horizon_days": horizon_days,
        "mean_crossing_days": sum(crossings) / len(crossings),
        "censored_fraction": sum(1 for x in crossings if x == horizon_days + 1) / len(crossings),
        "end_success": sum(end_success) / len(end_success),
    }


def write_threshold_sensitivity_stress():
    DOCS.mkdir(exist_ok=True)
    rows = []
    for horizon_days in [60, 120]:
        for threshold_fraction in [0.8, 0.5]:
            for policy in POLICIES:
                rows.append(crossing_summary(policy, threshold_fraction, horizon_days))

    with (DOCS / "threshold_sensitivity_stress.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "policy",
                "threshold_fraction",
                "horizon_days",
                "mean_crossing_days",
                "censored_fraction",
                "end_success",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in row.items()})

    by_key = {(row["policy"], row["threshold_fraction"], row["horizon_days"]): row for row in rows}
    table_rows = []
    labels = {
        "frozen": "Frozen skill",
        "calendar_recalibration": "Calendar recal.",
        "sentinel_rehearsal": "Sentinel rehearsal",
        "oracle_adapt": "Oracle adaptation",
    }
    for policy in POLICIES:
        h60 = by_key[(policy, 0.5, 60)]
        h120 = by_key[(policy, 0.5, 120)]
        h80 = by_key[(policy, 0.8, 60)]
        table_rows.append(
            f"{labels[policy]} & {h60['mean_crossing_days']:.1f} & {h60['censored_fraction']:.2f} & "
            f"{h120['mean_crossing_days']:.1f} & {h120['censored_fraction']:.2f} & "
            f"{h80['mean_crossing_days']:.1f} \\\\"
        )
    table = (
        "\\begin{table}[t]\n"
        "\\centering\n"
        "\\caption{V2 threshold and horizon sensitivity. Values of 61 or 121 are right-censored at the end of the 60- or 120-day observation window. Sentinel rehearsal is censored in the main 60-day half-life table, but crosses the half-success threshold when the window is extended.}\n"
        "\\label{tab:threshold-sensitivity}\n"
        "\\small\n"
        "\\begin{tabular}{@{}lrrrrr@{}}\n"
        "\\toprule\n"
        "Condition & $H_{0.5}^{60}$ & cens. & $H_{0.5}^{120}$ & cens. & $H_{0.8}^{60}$ \\\\\n"
        "\\midrule\n"
        + "\n".join(table_rows)
        + "\n\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
    )
    (DOCS / "threshold_sensitivity_stress_table.tex").write_text(table, encoding="utf-8")
    for row in rows:
        print(row)


def main():
    days = list(range(0, 61))
    trials = range(48)
    rows = []
    summary = []
    for policy in POLICIES:
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
    if "--stress-only" in sys.argv:
        write_threshold_sensitivity_stress()
    else:
        main()
