# Paper 39 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Harden Paper 39's visible PDF link-box styling so it matches the VLA-v4 role-model PDF's professional red and green boxed link treatment while preserving the final 25-page robot-skill-half-life manuscript, deterministic survival suite, and all scientific claims.

## Plan-Start Evidence

- Canonical PDF at plan start: `C:/Users/wangz/Downloads/39.pdf`.
- Plan-start size: 434913 bytes.
- Plan-start page count: 25.
- Plan-start affected link pages: 2, 5, 6, 7, 8, 16, 21, and 22.
- Plan-start link annotations: 28 green citation/link annotations and 14 red internal-reference annotations.
- Plan-start border state: all 42 link annotations used hidden zero-width borders, so the colored boxes were not visible.
- Plan-start LaTeX source used `\usepackage[hidelinks]{hyperref}` in root `main.tex`.
- Build wrapper is `scripts/build_pdf.ps1`; it builds from the repository root, exports `C:/Users/wangz/Downloads/39.pdf`, writes ignored `data/build_status.json`, and removes local `main.pdf`.
- Plan-start local `main.pdf` was absent.
- The full-scale survival suite remains 301,056 deterministic rows and 8,706,539,520 represented deployment-success reporting checks.

## Role-Model Style Target

Match the VLA-v4 role model's link annotation style:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

Expected Paper 39 result after rebuild:

- Page count remains 25.
- All 28 citation/link annotations remain green.
- All 14 internal-reference annotations remain red.
- All 42 link annotations use visible border `(0, 0, 1)`.
- No experiment data, figures, tables, claims, captions, or manuscript body text changes.

## Execution Plan

1. Render the current Downloads PDF pages 2, 5, 6, 7, 8, 16, 21, and 22 to a Paper39 baseline folder under `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/`.
2. Replace `\usepackage[hidelinks]{hyperref}` in root `main.tex` with plain `\usepackage{hyperref}` plus the VLA-v4 `\hypersetup` block above.
3. Rebuild using `scripts/build_pdf.ps1`, which exports only `C:/Users/wangz/Downloads/39.pdf`, records ignored build metadata, and removes local `main.pdf`.
4. Verify with `pypdf` that the rebuilt PDF has 25 pages, 28 green link annotations, 14 red link annotations, and 42 visible `(0, 0, 1)` borders.
5. Render affected post-change pages 2, 5, 6, 7, 8, 16, 21, and 22 and visually inspect the boxes for role-model-like color, line weight, alignment, spacing, and legibility, paying special attention to the dense citation runs on page 2 and appendix citation clusters on pages 21 and 22.
6. Update README, child status, final audit, reproducibility checklist, submission decision, version log, and full-scale execution metadata with the final hash and VLA-style visual QA evidence.
7. Remove Paper39 temporary render folders after QA while preserving the shared `role_model` render.
8. Commit and push the clean repo before moving to Paper38.

## Non-Goals

- Do not rerun the full-scale survival suite.
- Do not pad content or alter the 25-page manuscript.
- Do not revise scientific claims, tables, captions, figures, or body text unless visual QA exposes a layout defect that requires a tiny local fix.

## Final QA Result

- Rebuilt canonical PDF: `C:/Users/wangz/Downloads/39.pdf`.
- Final SHA256: `A8A9CCC28B8996DF055CE60037828F3513107585CE1BADB5C867D332ADB08B2E`.
- Final size: 434913 bytes.
- Page count remains 25.
- Annotation inventory: 28 green citation/link boxes, 14 red internal-reference boxes, and 42 visible `(0, 0, 1)` borders.
- Visual QA rendered pages 2, 5, 6, 7, 8, 16, 21, and 22 at 160 dpi. The boxes are thin, aligned, legible, and collision-free, matching the VLA-v4 role-model treatment.
- Local `main.pdf` was removed by the build wrapper after export.
