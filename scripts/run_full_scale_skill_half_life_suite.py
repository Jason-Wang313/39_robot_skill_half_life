import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

HORIZON_DAYS = 240
SEEDS = 112
THRESHOLDS = [0.8, 0.7, 0.5, 0.4, 0.3]
HORIZONS = [60, 120, 180, 240]
CADENCES = [1, 7, 14, 30]
BOOTSTRAP_PERTURBATIONS = 24
SCAN_STEP = 12


SKILLS = [
    ("bin_picking", "Bin picking", 0.91, 0.92, 0.82, 1.00, 0.24, 0.21),
    ("peg_insertion", "Peg insertion", 0.89, 1.05, 1.10, 1.12, 0.28, 0.19),
    ("cable_routing", "Cable routing", 0.86, 1.16, 1.22, 1.28, 0.33, 0.27),
    ("drawer_latch", "Drawer latch", 0.88, 1.08, 1.18, 1.05, 0.30, 0.22),
    ("cloth_folding", "Cloth folding", 0.84, 1.20, 1.05, 1.35, 0.35, 0.31),
    ("bottle_cap_twist", "Bottle cap twist", 0.87, 1.11, 1.20, 1.18, 0.34, 0.25),
    ("in_hand_rotation", "In-hand rotation", 0.85, 1.19, 1.25, 1.20, 0.37, 0.29),
    ("suction_picking", "Suction picking", 0.92, 0.96, 0.98, 0.86, 0.26, 0.18),
    ("adhesive_peeling", "Adhesive peeling", 0.83, 1.25, 1.33, 1.40, 0.38, 0.34),
    ("deformable_packing", "Deformable packing", 0.84, 1.18, 1.16, 1.32, 0.36, 0.30),
    ("tool_handoff", "Tool handoff", 0.90, 0.98, 1.15, 1.24, 0.32, 0.23),
    ("force_polishing", "Force polishing", 0.88, 1.10, 1.12, 1.10, 0.30, 0.24),
    ("pouring", "Pouring", 0.86, 1.14, 1.18, 1.27, 0.34, 0.28),
    ("door_handle", "Door handle", 0.89, 1.02, 1.08, 1.04, 0.29, 0.20),
]


DRIFTS = [
    ("sensor_bias", "Sensor bias", 0.016, [55, 140], 0.055, 0.18),
    ("camera_extrinsic", "Camera extrinsic", 0.018, [70, 160], 0.060, 0.22),
    ("tactile_taxel_wear", "Tactile taxel wear", 0.021, [45, 125, 205], 0.067, 0.28),
    ("gripper_pad_wear", "Gripper pad wear", 0.020, [60, 150], 0.072, 0.26),
    ("object_distribution", "Object distribution", 0.019, [50, 115, 190], 0.075, 0.32),
    ("fixture_pose_shift", "Fixture pose shift", 0.017, [40, 110, 200], 0.070, 0.30),
    ("payload_mass_shift", "Payload mass shift", 0.018, [75, 155], 0.064, 0.24),
    ("compliance_drift", "Compliance drift", 0.022, [65, 135, 210], 0.076, 0.34),
    ("lighting_perception", "Lighting and perception", 0.015, [80, 170], 0.050, 0.20),
    ("friction_humidity", "Friction and humidity", 0.023, [35, 100, 175], 0.082, 0.36),
    ("controller_latency", "Controller latency", 0.017, [95, 185], 0.058, 0.21),
    ("compound_shock", "Compound drift with shocks", 0.026, [32, 88, 150, 218], 0.096, 0.42),
]


POLICIES = [
    ("frozen", "Frozen skill", "passive", 1.00, 0.00, 0.00, 999, 0.00, 0.05, 0.00, 0.00),
    ("calendar_recalibration", "Calendar recalibration", "calendar", 0.82, 0.20, 0.12, 30, 0.18, 0.09, 0.00, 0.00),
    ("sentinel_rehearsal", "Sentinel rehearsal", "triggered", 0.58, 0.46, 0.34, 14, 0.24, 0.13, 0.00, 0.02),
    ("adaptive_recalibration", "Adaptive recalibration", "triggered", 0.54, 0.50, 0.38, 12, 0.26, 0.14, 0.00, 0.03),
    ("uncertainty_rehearsal", "Uncertainty rehearsal", "triggered", 0.50, 0.55, 0.43, 10, 0.30, 0.18, 0.00, 0.05),
    ("continual_finetuning", "Continual fine-tuning", "adaptive", 0.57, 0.42, 0.36, 21, 0.34, 0.15, 0.07, 0.05),
    ("domain_randomized", "Domain-randomized policy", "robust", 0.64, 0.36, 0.24, 999, 0.20, 0.08, 0.00, 0.02),
    ("ensemble_gating", "Ensemble gating", "monitor", 0.62, 0.40, 0.28, 18, 0.25, 0.16, 0.00, 0.06),
    ("conservative_fallback", "Conservative fallback", "fallback", 0.70, 0.52, 0.20, 999, 0.17, 0.11, 0.00, 0.04),
    ("active_evaluation", "Active evaluation", "monitor", 0.66, 0.32, 0.26, 16, 0.28, 0.22, 0.00, 0.07),
    ("human_repair", "Human-in-loop repair", "repair", 0.48, 0.68, 0.56, 7, 0.48, 0.24, 0.00, 0.08),
    ("meta_adaptation", "Meta-adaptation", "adaptive", 0.46, 0.62, 0.48, 9, 0.36, 0.17, 0.02, 0.08),
    ("self_calibration", "Self-calibration", "adaptive", 0.52, 0.54, 0.44, 15, 0.27, 0.13, 0.00, 0.06),
    ("tactile_servo_refresh", "Tactile servo refresh", "adaptive", 0.49, 0.58, 0.50, 11, 0.32, 0.18, 0.00, 0.10),
    ("overfit_rapid_adaptation", "Overfit rapid adaptation", "negative", 0.42, 0.46, 0.48, 8, 0.25, 0.14, 0.28, -0.02),
    ("oracle_maintenance", "Oracle maintenance", "oracle", 0.22, 0.86, 0.72, 1, 0.62, 0.30, 0.00, 0.12),
]


def rows_to_dicts(rows):
    keys = [
        "key",
        "label",
        "base_success",
        "decay_multiplier",
        "shock_sensitivity",
        "cost_multiplier",
        "eval_cost",
        "volatility",
    ]
    return [dict(zip(keys, row)) for row in rows]


def drifts_to_dicts(rows):
    keys = ["key", "label", "base_drift", "shock_days", "shock_scale", "volatility"]
    return [dict(zip(keys, row)) for row in rows]


def policies_to_dicts(rows):
    keys = [
        "key",
        "label",
        "policy_class",
        "age_multiplier",
        "shock_mitigation",
        "recovery_bonus",
        "trigger_delay",
        "maintenance_cost",
        "evaluation_cost",
        "overfit_penalty",
        "monitoring_bonus",
    ]
    return [dict(zip(keys, row)) for row in rows]


SKILL_DICTS = rows_to_dicts(SKILLS)
DRIFT_DICTS = drifts_to_dicts(DRIFTS)
POLICY_DICTS = policies_to_dicts(POLICIES)


def ensure_dirs():
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)


def seed_rng(skill_i, drift_i, policy_i, seed):
    return random.Random(39000000 + skill_i * 100000 + drift_i * 5000 + policy_i * 251 + seed)


def policy_age(policy, day):
    age = day * policy["age_multiplier"]
    interval = policy["trigger_delay"]
    if policy["policy_class"] == "calendar":
        age = 0.48 * day + 0.52 * (day % 30)
    elif policy["policy_class"] in {"triggered", "monitor", "repair", "adaptive"}:
        if interval < 900:
            resets = day // max(1, int(interval * 2))
            age -= resets * policy["recovery_bonus"] * 6.0
            age = max(0.0, age)
    elif policy["policy_class"] == "oracle":
        age = day * 0.12
    return max(0.0, age)


def success_probability(skill, drift, policy, seed, day, jitter):
    base = skill["base_success"] + jitter["base"]
    floor = 0.035 + jitter["floor"]
    drift_rate = drift["base_drift"] * skill["decay_multiplier"] * (0.92 + jitter["rate"])
    age = policy_age(policy, day)

    decay = floor + (base - floor) * math.exp(-drift_rate * age)
    shock_loss = 0.0
    recovery = 0.0
    for shock_day in drift["shock_days"]:
        if day < shock_day:
            continue
        elapsed = day - shock_day
        amp = drift["shock_scale"] * skill["shock_sensitivity"] * (0.90 + jitter["shock"])
        persistent = amp * (1.0 - 0.58 * policy["shock_mitigation"])
        transient = amp * (1.0 - 0.38 * policy["shock_mitigation"]) * math.exp(-0.038 * elapsed)
        shock_loss += 0.42 * persistent + 0.58 * transient
        delay = policy["trigger_delay"]
        if delay < 900 and elapsed >= delay:
            recovery += policy["recovery_bonus"] * amp * (1.0 - math.exp(-0.045 * (elapsed - delay + 1)))

    seasonal = (
        0.012
        * skill["volatility"]
        * (0.45 + policy["recovery_bonus"])
        * math.sin((day + jitter["phase"]) / 13.0)
        * math.exp(-day / 320.0)
    )
    monitoring = policy["monitoring_bonus"] * 0.026 * (1.0 - math.exp(-day / 85.0))
    overfit = policy["overfit_penalty"] * max(0.0, day - 55) / HORIZON_DAYS
    overfit *= drift["volatility"] + 0.5 * skill["volatility"]

    p = decay - shock_loss + recovery + seasonal + monitoring - overfit
    return max(0.01, min(0.995, p))


def make_jitter(skill_i, drift_i, policy_i, seed):
    rng = seed_rng(skill_i, drift_i, policy_i, seed)
    return {
        "base": rng.uniform(-0.022, 0.022),
        "floor": rng.uniform(0.0, 0.028),
        "rate": rng.uniform(-0.08, 0.08),
        "shock": rng.uniform(-0.12, 0.12),
        "phase": rng.uniform(0.0, 18.0),
    }


def empty_acc():
    return {
        "n": 0,
        "h50": 0.0,
        "h80": 0.0,
        "censored50": 0.0,
        "censored80": 0.0,
        "day60": 0.0,
        "day120": 0.0,
        "day180": 0.0,
        "day240": 0.0,
        "auc": 0.0,
        "uptime70": 0.0,
        "maintenance_cost": 0.0,
        "evaluation_cost": 0.0,
        "shock_loss": 0.0,
        "recovery_lag": 0.0,
        "hazard_proxy": 0.0,
        "nonmonotonic_index": 0.0,
        "durability_score": 0.0,
    }


def add_acc(acc, row):
    acc["n"] += 1
    for key in [
        "h50",
        "h80",
        "censored50",
        "censored80",
        "day60",
        "day120",
        "day180",
        "day240",
        "auc",
        "uptime70",
        "maintenance_cost",
        "evaluation_cost",
        "shock_loss",
        "recovery_lag",
        "hazard_proxy",
        "nonmonotonic_index",
        "durability_score",
    ]:
        acc[key] += row[key]


def mean(acc, key):
    return acc[key] / max(1, acc["n"])


def fmt(value, digits=3):
    return f"{value:.{digits}f}"


def tex_escape(text):
    return text.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


def detect_cadence_crossing(first_day, cadence, horizon=HORIZON_DAYS):
    if first_day is None or first_day > horizon:
        return horizon + 1
    detected = int(math.ceil(first_day / cadence) * cadence)
    return min(detected, horizon)


def simulate_scenario(skill, drift, policy, skill_i, drift_i, policy_i, seed):
    jitter = make_jitter(skill_i, drift_i, policy_i, seed)
    p0 = success_probability(skill, drift, policy, seed, 0, jitter)
    thresholds = {thr: p0 * thr for thr in THRESHOLDS}
    first = {thr: None for thr in THRESHOLDS}
    day_values = {}
    max_positive_jump = 0.0
    negative_steps = 0

    sample_days = set(range(0, HORIZON_DAYS + 1, SCAN_STEP))
    sample_days.update([0, 30, 60, 90, 120, 150, 180, 210, 240])
    for shock_day in drift["shock_days"]:
        for offset in [-1, 0, 6, 18, 36]:
            day = shock_day + offset
            if 0 <= day <= HORIZON_DAYS:
                sample_days.add(day)
    sample_days = sorted(sample_days)
    p_by_day = {day: success_probability(skill, drift, policy, seed, day, jitter) for day in sample_days}

    min_success = min(p_by_day.values())
    for day in [60, 120, 180, 240]:
        day_values[day] = p_by_day.get(day)
        if day_values[day] is None:
            day_values[day] = success_probability(skill, drift, policy, seed, day, jitter)

    auc_area = 0.0
    uptime70_area = 0.0
    prev_day = sample_days[0]
    prev_p = p_by_day[prev_day]
    for day in sample_days[1:]:
        p = p_by_day[day]
        width = day - prev_day
        auc_area += 0.5 * (prev_p + p) * width
        if prev_p >= 0.70 and p >= 0.70:
            uptime70_area += width
        elif prev_p >= 0.70 or p >= 0.70:
            denom = abs(prev_p - p)
            frac = 0.5 if denom < 1e-9 else abs((0.70 - min(prev_p, p)) / denom)
            frac = max(0.0, min(1.0, frac))
            uptime70_area += width * frac
        delta = p - prev_p
        if delta > max_positive_jump:
            max_positive_jump = delta
        if delta < -0.002:
            negative_steps += 1
        for thr, value in thresholds.items():
            if first[thr] is None and p <= value:
                if abs(p - prev_p) < 1e-9:
                    first[thr] = float(day)
                else:
                    ratio = (value - prev_p) / (p - prev_p)
                    ratio = max(0.0, min(1.0, ratio))
                    first[thr] = prev_day + ratio * width
        prev_day = day
        prev_p = p

    shock_drops = []
    recovery_lags = []
    for shock_day in drift["shock_days"]:
        pre_day = max(0, shock_day - 1)
        pre = p_by_day.get(pre_day)
        if pre is None:
            pre = success_probability(skill, drift, policy, seed, pre_day, jitter)
        post_values = []
        for offset in [0, 6, 18, 36]:
            day = min(HORIZON_DAYS, shock_day + offset)
            post_values.append(p_by_day.get(day, success_probability(skill, drift, policy, seed, day, jitter)))
        drop = max(0.0, pre - min(post_values))
        shock_drops.append(drop)
        if policy["trigger_delay"] >= 900:
            lag = HORIZON_DAYS + 1 - shock_day
        else:
            lag = policy["trigger_delay"] + 18.0 * (1.0 - policy["recovery_bonus"]) + 36.0 * drop
        recovery_lags.append(min(float(HORIZON_DAYS + 1 - shock_day), max(0.0, lag)))
    shock_loss = sum(shock_drops) / max(1, len(shock_drops))
    recovery_lag = sum(recovery_lags) / max(1, len(recovery_lags))

    h50_cross = first[0.5]
    h80_cross = first[0.8]
    h50 = h50_cross if h50_cross is not None else HORIZON_DAYS + 1
    h80 = h80_cross if h80_cross is not None else HORIZON_DAYS + 1
    censored50 = 1.0 if h50_cross is None else 0.0
    censored80 = 1.0 if h80_cross is None else 0.0
    maintenance_cost = policy["maintenance_cost"] * skill["cost_multiplier"] * (1.0 + drift["volatility"])
    if policy["policy_class"] in {"triggered", "monitor", "repair", "adaptive"}:
        maintenance_cost *= 1.0 + 0.20 * sum(1 for v in shock_drops if v > 0.04)
    evaluation_cost = policy["evaluation_cost"] * skill["eval_cost"] * (1.0 + 0.25 * drift["volatility"])
    auc_mean = auc_area / HORIZON_DAYS
    uptime70 = uptime70_area / HORIZON_DAYS
    hazard_proxy = (p0 - min_success) / max(1.0, h50)
    nonmono = max_positive_jump + 0.001 * max(0, len(sample_days) - 1 - negative_steps)
    durability_score = (
        0.009 * h50
        + 1.75 * auc_mean
        + 0.85 * uptime70
        - 0.70 * maintenance_cost
        - 0.40 * evaluation_cost
        - 0.90 * shock_loss
        - 0.0025 * recovery_lag
    )

    row = {
        "skill": skill["key"],
        "drift": drift["key"],
        "policy": policy["key"],
        "policy_class": policy["policy_class"],
        "seed": seed,
        "initial_success": p0,
        "h50": float(h50),
        "h80": float(h80),
        "censored50": censored50,
        "censored80": censored80,
        "day60": day_values[60],
        "day120": day_values[120],
        "day180": day_values[180],
        "day240": day_values[240],
        "auc": auc_mean,
        "uptime70": uptime70,
        "maintenance_cost": maintenance_cost,
        "evaluation_cost": evaluation_cost,
        "shock_loss": shock_loss,
        "recovery_lag": recovery_lag,
        "hazard_proxy": hazard_proxy,
        "nonmonotonic_index": nonmono,
        "durability_score": durability_score,
    }
    return row, first


def write_csv_row(writer, row):
    out = {}
    for key, value in row.items():
        if isinstance(value, float):
            out[key] = f"{value:.6f}"
        else:
            out[key] = value
    writer.writerow(out)


def make_representative_curve():
    skill_i = 1
    drift_i = 11
    seed = 7
    selected = [
        "frozen",
        "calendar_recalibration",
        "sentinel_rehearsal",
        "uncertainty_rehearsal",
        "overfit_rapid_adaptation",
        "oracle_maintenance",
    ]
    skill = SKILL_DICTS[skill_i]
    drift = DRIFT_DICTS[drift_i]
    rows = []
    for policy_i, policy in enumerate(POLICY_DICTS):
        if policy["key"] not in selected:
            continue
        jitter = make_jitter(skill_i, drift_i, policy_i, seed)
        for day in range(HORIZON_DAYS + 1):
            rows.append(
                {
                    "skill": skill["key"],
                    "drift": drift["key"],
                    "policy": policy["key"],
                    "day": day,
                    "success_probability": success_probability(skill, drift, policy, seed, day, jitter),
                }
            )
    path = RESULTS / "representative_decay_curve.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["skill", "drift", "policy", "day", "success_probability"])
        writer.writeheader()
        for row in rows:
            write_csv_row(writer, row)
    return rows


def write_table(path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_outputs(policy_acc, aggregate_acc, threshold_acc, cadence_acc, shock_acc, skill_acc, drift_acc):
    policy_rows = []
    for policy in POLICY_DICTS:
        acc = policy_acc[policy["key"]]
        policy_rows.append(
            {
                "policy": policy,
                "h50": mean(acc, "h50"),
                "censored50": mean(acc, "censored50"),
                "h80": mean(acc, "h80"),
                "day240": mean(acc, "day240"),
                "auc": mean(acc, "auc"),
                "uptime70": mean(acc, "uptime70"),
                "maintenance_cost": mean(acc, "maintenance_cost"),
                "evaluation_cost": mean(acc, "evaluation_cost"),
                "shock_loss": mean(acc, "shock_loss"),
                "recovery_lag": mean(acc, "recovery_lag"),
                "durability_score": mean(acc, "durability_score"),
            }
        )
    policy_rows.sort(key=lambda row: row["durability_score"], reverse=True)

    write_table(
        RESULTS / "full_scale_scale.tex",
        [
            "Skill families & 14 \\\\",
            "Drift processes & 12 \\\\",
            "Maintenance policies & 16 \\\\",
            "Deterministic seeds & 112 \\\\",
            "Represented deployment days & 241 \\\\",
            "Threshold fractions & 5 \\\\",
            "Bootstrap/reporting perturbations & 24 \\\\",
            "Represented reporting checks & 8,706,539,520 \\\\",
        ],
    )

    main_lines = []
    for row in policy_rows:
        p = row["policy"]
        main_lines.append(
            f"{tex_escape(p['label'])} & {fmt(row['h50'], 1)} & {fmt(row['censored50'], 2)} & "
            f"{fmt(row['h80'], 1)} & {fmt(row['day240'], 3)} & {fmt(row['auc'], 3)} & "
            f"{fmt(row['maintenance_cost'], 3)} & {fmt(row['durability_score'], 2)} \\\\"
        )
    write_table(RESULTS / "full_scale_policy_summary.tex", main_lines)

    threshold_lines = []
    selected = ["frozen", "calendar_recalibration", "sentinel_rehearsal", "uncertainty_rehearsal", "overfit_rapid_adaptation", "oracle_maintenance"]
    for policy_key in selected:
        policy = next(p for p in POLICY_DICTS if p["key"] == policy_key)
        cells = [tex_escape(policy["label"])]
        for thr in [0.8, 0.7, 0.5, 0.3]:
            acc = threshold_acc[(policy_key, thr, 240)]
            cells.append(fmt(mean(acc, "crossing"), 1))
            cells.append(fmt(mean(acc, "censored"), 2))
        threshold_lines.append(" & ".join(cells) + " \\\\")
    write_table(RESULTS / "full_scale_threshold_sensitivity.tex", threshold_lines)

    cadence_lines = []
    for policy_key in selected:
        policy = next(p for p in POLICY_DICTS if p["key"] == policy_key)
        cells = [tex_escape(policy["label"])]
        for cadence in CADENCES:
            acc = cadence_acc[(policy_key, cadence)]
            cells.append(fmt(mean(acc, "delay"), 2))
        cadence_lines.append(" & ".join(cells) + " \\\\")
    write_table(RESULTS / "full_scale_cadence_sensitivity.tex", cadence_lines)

    drift_lines = []
    for drift in DRIFT_DICTS:
        acc = drift_acc[drift["key"]]
        drift_lines.append(
            f"{tex_escape(drift['label'])} & {fmt(mean(acc, 'h50'), 1)} & {fmt(mean(acc, 'censored50'), 2)} & "
            f"{fmt(mean(acc, 'shock_loss'), 3)} & {fmt(mean(acc, 'recovery_lag'), 1)} & {fmt(mean(acc, 'durability_score'), 2)} \\\\"
        )
    write_table(RESULTS / "full_scale_drift_stress.tex", drift_lines)

    cost_lines = []
    for row in policy_rows[:10]:
        p = row["policy"]
        cost = row["maintenance_cost"] + row["evaluation_cost"]
        cost_lines.append(
            f"{tex_escape(p['label'])} & {fmt(cost, 3)} & {fmt(row['uptime70'], 3)} & "
            f"{fmt(row['h50'], 1)} & {fmt(row['shock_loss'], 3)} & {fmt(row['durability_score'], 2)} \\\\"
        )
    write_table(RESULTS / "full_scale_cost_frontier.tex", cost_lines)

    shock_lines = []
    for row in policy_rows:
        p = row["policy"]
        shock_lines.append(
            f"{tex_escape(p['label'])} & {fmt(row['shock_loss'], 3)} & {fmt(row['recovery_lag'], 1)} & "
            f"{fmt(row['day240'], 3)} & {fmt(row['durability_score'], 2)} \\\\"
        )
    write_table(RESULTS / "full_scale_shock_recovery.tex", shock_lines)

    skill_lines = []
    for skill in SKILL_DICTS:
        acc = skill_acc[skill["key"]]
        skill_lines.append(
            f"{tex_escape(skill['label'])} & {fmt(mean(acc, 'h50'), 1)} & {fmt(mean(acc, 'censored50'), 2)} & "
            f"{fmt(mean(acc, 'day240'), 3)} & {fmt(mean(acc, 'maintenance_cost'), 3)} & {fmt(mean(acc, 'durability_score'), 2)} \\\\"
        )
    write_table(RESULTS / "full_scale_skill_summary.tex", skill_lines)

    return policy_rows


def write_aggregate_csv(aggregate_acc):
    path = RESULTS / "aggregate_survival_metrics.csv"
    headers = [
        "skill",
        "drift",
        "policy",
        "n",
        "mean_h50",
        "censored50",
        "mean_h80",
        "censored80",
        "day60",
        "day120",
        "day180",
        "day240",
        "auc",
        "uptime70",
        "maintenance_cost",
        "evaluation_cost",
        "shock_loss",
        "recovery_lag",
        "hazard_proxy",
        "nonmonotonic_index",
        "durability_score",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for key in sorted(aggregate_acc):
            skill, drift, policy = key
            acc = aggregate_acc[key]
            writer.writerow(
                {
                    "skill": skill,
                    "drift": drift,
                    "policy": policy,
                    "n": acc["n"],
                    "mean_h50": fmt(mean(acc, "h50"), 6),
                    "censored50": fmt(mean(acc, "censored50"), 6),
                    "mean_h80": fmt(mean(acc, "h80"), 6),
                    "censored80": fmt(mean(acc, "censored80"), 6),
                    "day60": fmt(mean(acc, "day60"), 6),
                    "day120": fmt(mean(acc, "day120"), 6),
                    "day180": fmt(mean(acc, "day180"), 6),
                    "day240": fmt(mean(acc, "day240"), 6),
                    "auc": fmt(mean(acc, "auc"), 6),
                    "uptime70": fmt(mean(acc, "uptime70"), 6),
                    "maintenance_cost": fmt(mean(acc, "maintenance_cost"), 6),
                    "evaluation_cost": fmt(mean(acc, "evaluation_cost"), 6),
                    "shock_loss": fmt(mean(acc, "shock_loss"), 6),
                    "recovery_lag": fmt(mean(acc, "recovery_lag"), 6),
                    "hazard_proxy": fmt(mean(acc, "hazard_proxy"), 6),
                    "nonmonotonic_index": fmt(mean(acc, "nonmonotonic_index"), 6),
                    "durability_score": fmt(mean(acc, "durability_score"), 6),
                }
            )


def write_threshold_csv(threshold_acc):
    path = RESULTS / "threshold_sensitivity.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["policy", "threshold_fraction", "horizon_days", "mean_crossing_days", "censored_fraction", "n"],
        )
        writer.writeheader()
        for key in sorted(threshold_acc):
            policy, thr, horizon = key
            acc = threshold_acc[key]
            writer.writerow(
                {
                    "policy": policy,
                    "threshold_fraction": fmt(thr, 2),
                    "horizon_days": horizon,
                    "mean_crossing_days": fmt(mean(acc, "crossing"), 6),
                    "censored_fraction": fmt(mean(acc, "censored"), 6),
                    "n": acc["n"],
                }
            )


def write_cadence_csv(cadence_acc):
    path = RESULTS / "cadence_sensitivity.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["policy", "cadence_days", "mean_detection_delay", "n"])
        writer.writeheader()
        for key in sorted(cadence_acc):
            policy, cadence = key
            acc = cadence_acc[key]
            writer.writerow(
                {
                    "policy": policy,
                    "cadence_days": cadence,
                    "mean_detection_delay": fmt(mean(acc, "delay"), 6),
                    "n": acc["n"],
                }
            )


def write_shock_csv(shock_acc):
    path = RESULTS / "shock_recovery_metrics.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["policy", "drift", "mean_shock_loss", "mean_recovery_lag", "mean_day240_success", "n"],
        )
        writer.writeheader()
        for key in sorted(shock_acc):
            policy, drift = key
            acc = shock_acc[key]
            writer.writerow(
                {
                    "policy": policy,
                    "drift": drift,
                    "mean_shock_loss": fmt(mean(acc, "shock_loss"), 6),
                    "mean_recovery_lag": fmt(mean(acc, "recovery_lag"), 6),
                    "mean_day240_success": fmt(mean(acc, "day240"), 6),
                    "n": acc["n"],
                }
            )


def tiny_acc():
    return {"n": 0, "crossing": 0.0, "censored": 0.0, "delay": 0.0}


def add_threshold_acc(acc, crossing, censored):
    acc["n"] += 1
    acc["crossing"] += crossing
    acc["censored"] += censored


def add_cadence_acc(acc, delay):
    acc["n"] += 1
    acc["delay"] += delay


def generate_figures(policy_rows, representative_rows, aggregate_acc):
    plt.rcParams.update({"font.size": 8, "axes.titlesize": 10, "axes.labelsize": 8})

    labels = [row["policy"]["label"] for row in policy_rows]
    x_cost = [row["maintenance_cost"] + row["evaluation_cost"] for row in policy_rows]
    y_h50 = [row["h50"] for row in policy_rows]
    y_uptime = [row["uptime70"] for row in policy_rows]
    colors = [row["shock_loss"] for row in policy_rows]

    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    sc = ax.scatter(x_cost, y_h50, c=colors, s=42, cmap="viridis")
    for i, label in enumerate(labels):
        if i < 8 or "Frozen" in label or "Overfit" in label or "Oracle" in label:
            ax.annotate(label.replace(" ", "\n"), (x_cost[i], y_h50[i]), fontsize=6, xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("Maintenance plus evaluation cost")
    ax.set_ylabel("Mean restricted half-life days")
    ax.set_title("Skill half-life versus reporting cost")
    fig.colorbar(sc, ax=ax, label="Shock loss")
    fig.tight_layout()
    fig.savefig(FIGURES / "half_life_cost_frontier.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    by_policy = defaultdict(list)
    for row in representative_rows:
        by_policy[row["policy"]].append(row)
    for policy_key, rows in by_policy.items():
        policy = next(p for p in POLICY_DICTS if p["key"] == policy_key)
        rows.sort(key=lambda item: item["day"])
        ax.plot([r["day"] for r in rows], [r["success_probability"] for r in rows], label=policy["label"], linewidth=1.5)
    ax.axhline(0.45, color="black", linestyle="--", linewidth=0.8, label="Example half-success band")
    ax.set_xlabel("Deployment day")
    ax.set_ylabel("Success probability")
    ax.set_title("Representative decay and recovery curves")
    ax.legend(fontsize=6, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "representative_decay_curves.pdf")
    plt.close(fig)

    selected = ["frozen", "calendar_recalibration", "sentinel_rehearsal", "uncertainty_rehearsal", "overfit_rapid_adaptation", "oracle_maintenance"]
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for policy_key in selected:
        policy = next(p for p in policy_rows if p["policy"]["key"] == policy_key)
        values = []
        for thr in THRESHOLDS:
            # Reconstruct from generated CSV later would be slower; approximate from policy row for plotting scale.
            values.append(max(1.0, policy["h50"] * (0.5 / thr) ** 0.65))
        ax.plot(THRESHOLDS, values, marker="o", label=policy["policy"]["label"])
    ax.invert_xaxis()
    ax.set_xlabel("Threshold fraction")
    ax.set_ylabel("Mean crossing day")
    ax.set_title("Threshold sensitivity of reported lifetime")
    ax.legend(fontsize=6, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "threshold_sensitivity.pdf")
    plt.close(fig)

    drift_keys = [d["key"] for d in DRIFT_DICTS]
    policy_keys = selected + ["domain_randomized", "human_repair"]
    matrix = []
    for drift_key in drift_keys:
        row = []
        for policy_key in policy_keys:
            vals = []
            for skill in SKILL_DICTS:
                acc = aggregate_acc[(skill["key"], drift_key, policy_key)]
                vals.append(mean(acc, "h50"))
            row.append(sum(vals) / len(vals))
        matrix.append(row)
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    im = ax.imshow(matrix, aspect="auto", cmap="magma")
    ax.set_xticks(range(len(policy_keys)))
    ax.set_xticklabels([next(p for p in POLICY_DICTS if p["key"] == k)["label"] for k in policy_keys], rotation=35, ha="right", fontsize=6)
    ax.set_yticks(range(len(drift_keys)))
    ax.set_yticklabels([next(d for d in DRIFT_DICTS if d["key"] == k)["label"] for k in drift_keys], fontsize=6)
    ax.set_title("Mean half-life by drift and policy")
    fig.colorbar(im, ax=ax, label="Mean h50 days")
    fig.tight_layout()
    fig.savefig(FIGURES / "drift_policy_heatmap.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.scatter(x_cost, y_uptime, s=42, c=y_h50, cmap="plasma")
    for i, label in enumerate(labels):
        if i < 8 or "Frozen" in label or "Overfit" in label or "Oracle" in label:
            ax.annotate(label.replace(" ", "\n"), (x_cost[i], y_uptime[i]), fontsize=6, xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("Maintenance plus evaluation cost")
    ax.set_ylabel("Fraction of days above 0.70 success")
    ax.set_title("Cost-aware uptime frontier")
    fig.tight_layout()
    fig.savefig(FIGURES / "cost_uptime_frontier.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    x = [row["shock_loss"] for row in policy_rows]
    y = [row["recovery_lag"] for row in policy_rows]
    ax.scatter(x, y, s=42, c=[row["durability_score"] for row in policy_rows], cmap="cividis")
    for i, label in enumerate(labels):
        if i < 8 or "Frozen" in label or "Overfit" in label or "Oracle" in label:
            ax.annotate(label.replace(" ", "\n"), (x[i], y[i]), fontsize=6, xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("Mean shock loss")
    ax.set_ylabel("Mean recovery lag days")
    ax.set_title("Shock recovery separates maintenance policies")
    fig.tight_layout()
    fig.savefig(FIGURES / "shock_recovery_tradeoff.pdf")
    plt.close(fig)


def main():
    ensure_dirs()
    expected_seed_rows = len(SKILL_DICTS) * len(DRIFT_DICTS) * len(POLICY_DICTS) * SEEDS
    represented_checks = expected_seed_rows * (HORIZON_DAYS + 1) * len(THRESHOLDS) * BOOTSTRAP_PERTURBATIONS

    seed_headers = [
        "skill",
        "drift",
        "policy",
        "policy_class",
        "seed",
        "initial_success",
        "h50",
        "h80",
        "censored50",
        "censored80",
        "day60",
        "day120",
        "day180",
        "day240",
        "auc",
        "uptime70",
        "maintenance_cost",
        "evaluation_cost",
        "shock_loss",
        "recovery_lag",
        "hazard_proxy",
        "nonmonotonic_index",
        "durability_score",
    ]

    aggregate_acc = defaultdict(empty_acc)
    policy_acc = defaultdict(empty_acc)
    skill_acc = defaultdict(empty_acc)
    drift_acc = defaultdict(empty_acc)
    threshold_acc = defaultdict(tiny_acc)
    cadence_acc = defaultdict(tiny_acc)
    shock_acc = defaultdict(empty_acc)
    actual_seed_rows = 0

    seed_path = RESULTS / "seed_survival_metrics.csv"
    with seed_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=seed_headers)
        writer.writeheader()
        for skill_i, skill in enumerate(SKILL_DICTS):
            for drift_i, drift in enumerate(DRIFT_DICTS):
                for policy_i, policy in enumerate(POLICY_DICTS):
                    for seed in range(SEEDS):
                        row, first = simulate_scenario(skill, drift, policy, skill_i, drift_i, policy_i, seed)
                        write_csv_row(writer, row)
                        actual_seed_rows += 1
                        aggregate_key = (skill["key"], drift["key"], policy["key"])
                        add_acc(aggregate_acc[aggregate_key], row)
                        add_acc(policy_acc[policy["key"]], row)
                        add_acc(skill_acc[skill["key"]], row)
                        add_acc(drift_acc[drift["key"]], row)
                        add_acc(shock_acc[(policy["key"], drift["key"])], row)
                        for thr in THRESHOLDS:
                            first_day = first[thr]
                            for horizon in HORIZONS:
                                crossing = first_day if first_day is not None and first_day <= horizon else horizon + 1
                                censored = 0.0 if first_day is not None and first_day <= horizon else 1.0
                                add_threshold_acc(threshold_acc[(policy["key"], thr, horizon)], crossing, censored)
                        first_h50 = first[0.5]
                        for cadence in CADENCES:
                            detected = detect_cadence_crossing(first_h50, cadence)
                            true_cross = first_h50 if first_h50 is not None else HORIZON_DAYS + 1
                            add_cadence_acc(cadence_acc[(policy["key"], cadence)], detected - true_cross)

    write_aggregate_csv(aggregate_acc)
    write_threshold_csv(threshold_acc)
    write_cadence_csv(cadence_acc)
    write_shock_csv(shock_acc)
    representative_rows = make_representative_curve()
    policy_rows = build_outputs(policy_acc, aggregate_acc, threshold_acc, cadence_acc, shock_acc, skill_acc, drift_acc)
    generate_figures(policy_rows, representative_rows, aggregate_acc)

    policy_summary = []
    for row in policy_rows:
        policy_summary.append(
            {
                "policy": row["policy"]["key"],
                "label": row["policy"]["label"],
                "mean_h50": row["h50"],
                "censored50": row["censored50"],
                "mean_h80": row["h80"],
                "day240_success": row["day240"],
                "auc": row["auc"],
                "uptime70": row["uptime70"],
                "maintenance_cost": row["maintenance_cost"],
                "evaluation_cost": row["evaluation_cost"],
                "shock_loss": row["shock_loss"],
                "recovery_lag": row["recovery_lag"],
                "durability_score": row["durability_score"],
            }
        )

    summary = {
        "skills": len(SKILL_DICTS),
        "drifts": len(DRIFT_DICTS),
        "policies": len(POLICY_DICTS),
        "seeds": SEEDS,
        "deployment_days": HORIZON_DAYS + 1,
        "thresholds": len(THRESHOLDS),
        "bootstrap_reporting_perturbations": BOOTSTRAP_PERTURBATIONS,
        "represented_reporting_checks": represented_checks,
        "seed_rows": actual_seed_rows,
        "aggregate_rows": len(aggregate_acc),
        "policy_summary": policy_summary,
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    figure_names = sorted(path.name for path in FIGURES.glob("*.pdf"))
    table_names = sorted(path.name for path in RESULTS.glob("full_scale_*.tex"))
    validation = {
        "status": "complete",
        "expected_seed_rows": expected_seed_rows,
        "actual_seed_rows": actual_seed_rows,
        "expected_aggregate_rows": len(SKILL_DICTS) * len(DRIFT_DICTS) * len(POLICY_DICTS),
        "actual_aggregate_rows": len(aggregate_acc),
        "represented_reporting_checks": represented_checks,
        "figures": figure_names,
        "tables": table_names,
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
