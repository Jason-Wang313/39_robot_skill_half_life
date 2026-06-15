# Robot Skill Half-Life

Paper 39 in the robotics 60-paper batch, v3 final full-scale verified.

This repository contains a final 25-page ICLR-style manuscript proposing robot
skill half-life as a survival-style reporting diagnostic for deployed
manipulation policies. The paper argues that robot skills should be reported as
temporal deployment objects: initial success, decay curve, half-life, censoring,
threshold, horizon, cadence, shock recovery, maintenance policy, and cost must
be disclosed together.

Main artifacts:
- `main.tex`: final manuscript source.
- `C:/Users/wangz/Downloads/39.pdf`: canonical final PDF, 25 pages.
- `scripts/run_full_scale_skill_half_life_suite.py`: deterministic full-scale survival suite.
- `results/full_scale/`: seed rows, aggregate rows, stress CSVs, generated tables, validation, and summary metadata.
- `figures/full_scale/`: generated PDF figures used in the manuscript.
- `scripts/build_pdf.ps1`: canonical build/export script that copies only the final PDF to Downloads and removes local `main.pdf`.
- `docs/`: execution plan, claims, audit trail, reviewer attacks, readiness decision, and reproducibility notes.

Build:

```powershell
python scripts/run_full_scale_skill_half_life_suite.py
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

Final validation:
- Downloads PDF: `C:/Users/wangz/Downloads/39.pdf`
- Pages: 25
- File size: 434,913 bytes
- SHA256: `5987CFCC7345344C850BEDC488C9D357E881B851692F93F6FE34DFDCBA22643B`
- Local `main.pdf`: absent after canonical build
- Visual render check: passed on the final Downloads PDF
