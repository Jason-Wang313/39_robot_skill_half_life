# Plan

## Original Construction

1. Reconstruct the paper's research direction through literature on skill persistence, robot drift, continual adaptation, and policy aging.
2. Build evidence artifacts: landscape sweep, hostile prior-work set, novelty boundary map, claims, reviewer attacks, and final audit notes.
3. Select the thesis that robot skill reports should include temporal decay, not only initial benchmark success.
4. Draft the initial anonymous ICLR paper, deterministic drift simulator, and canonical build script.

## V3 Full-Scale Execution

1. Write a detailed per-paper execution plan before touching Paper39.
2. Replace the short v2 diagnostic note with a RAM-light full-scale deterministic survival suite.
3. Evaluate 14 manipulation skill families, 12 drift processes, 16 policies, and 112 seeds.
4. Stream 301,056 seed-level rows and aggregate to 2,688 skill-drift-policy rows.
5. Generate threshold, cadence, shock-recovery, cost, policy, skill, and drift stress artifacts.
6. Generate manuscript figures and LaTeX table snippets under `figures/full_scale/` and `results/full_scale/`.
7. Rewrite `main.tex` into a 25-page final manuscript with protocol, results, discussion, limitations, appendices, and reproducibility details.
8. Build locally, scan logs and text, render the PDF, inspect visual layout, and rebuild/export.
9. Export only the final verified manuscript to `C:/Users/wangz/Downloads/39.pdf`.
10. Update docs, validation files, and status records to match the final artifact.
11. Commit and push before moving to Paper40.

## Final Acceptance State

- Final PDF: `C:/Users/wangz/Downloads/39.pdf`
- Page count: 25
- Represented checks: 8,706,539,520
- Seed rows: 301,056
- Aggregate rows: 2,688
- Local `main.pdf`: absent
- Visual render: passed
