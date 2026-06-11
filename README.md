# Robot Skill Half-Life

Paper 39 in the robotics 60-paper batch.

This repository contains an ICLR-style diagnostic paper proposing robot skill half-life: the time until a deployed manipulation policy's success probability falls below half of its initial value under a specified drift process.

Main artifacts:
- `main.tex` and `main.pdf`: paper source and compiled PDF.
- `tools_collect_literature.py`: metadata sweep script.
- `docs/related_work_matrix.csv`: 1,200-row supervised literature metadata matrix.
- `scripts/skill_half_life_sim.py`: deterministic toy drift simulation.
- `docs/skill_half_life_summary.csv`: summary table used by the paper.
- `docs/final_audit.md`: recovery and verification notes.

Build:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
