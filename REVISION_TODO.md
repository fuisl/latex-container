# Revision TODO — cair/manuscript (from panel review + coaching, 2026-07-16)

Strategy locked in coaching: **criterion-and-rationale paper**. Retention theory is the headline;
InfoMap is the instrument. One mechanism story everywhere: *retention proven → causal middle
tested-and-null in this regime → training gains attributed to conditioning (ε_cond)*.

## P1 — Required (this pass)

- [x] **R1a. Related Work** — written first to calibrate the gap claim. Positions against
  `odflow2019partition` (OD-flow partitioning exists → our gap is the *rationale*, never
  "nobody used flow"), feudal/METIS lineage (`ma2020fma2c`, `ma2022feudal`), learned-topology
  MARL, dependency-measurement work, theory imports, and CD baselines.
- [x] **R1b. Introduction** — meta-gap framing (no principled account of what a partition
  should preserve); contributions C1–C5 reworded criterion-first.
- [x] **R1c. Conclusion** — evidentiary split stated plainly; near-saturation arm named as
  the decisive next experiment; limitations enumerated.
- [x] **R1d. Abstract** — rewritten ≤210 words, confirmatory result leads; "up to 2.85×"
  and all vs-global ratios removed (old draft kept in comment).
- [x] **R2. ε_opt contradiction (DA-CRITICAL)** — Theorem 1 error term split into
  ε_approx + ε_opt⁰ + ε_cond(P); C stated uniform over partitions; §5.7/§5.9/App. A.3
  aligned to the same decomposition. "Optimisation conditioning" now has a named term.
- [x] **R4 (partial). Baseline-dependent claims quarantined** — vs-global waiting-time ratios
  moved to LaTeX comments marked `PENDING-RERUN` (baselines are re-running); flow-vs-METIS
  kept as the primary in-text comparison. Restore the commented text once reruns land.

## P2 — Strongly recommended (this pass where possible)

- [x] **S2 wording. D^G "replicated" softened** — single-checkpoint status now explicit at
  the claim site; multi-checkpoint evaluation left as commented TODO.
- [x] **S5. Practitioner procedure** — "recommended procedure" paragraph added to Conclusion.
- [x] **S6. Positioning vs odflow2019partition** — done inside Related Work ¶1.
- [x] **Epistemic-status table** (from proof.tex §6) added at the top of Appendix A.
- [x] **FMA2C evidence** — honest paragraph drafted as a COMMENT in Conclusion (non-converged;
  do not uncomment until numbers are verified against logs).
- [ ] **S1. Random-partition training runs** (1 per network, IPPO+MAPPO) — COMPUTE. Kills the
  "any partition would help" alternative. Commented hook left in §5.8.
- [ ] **S3. Regress ΔΨ on ΔΦ across the 4,935 benchmark partitions** — quantifies
  (non-)circularity of the confirmatory core. Data exist in the analysis repo.
- [ ] **S4. Train one named validation-front partition** — connects benchmark to training study.
- [ ] **R3. KSG validity** — block-bootstrap estimator variance + k_KSG/dimension sensitivity
  for the 12/12 ordering. Commented TODO at the claim site in §5.2.
- [ ] **R4 (rest). Baseline reruns finish** → restore `PENDING-RERUN` comment blocks, update
  Tables 6/9/10 and appendix notes.

## P3 — Minor sweep

- [x] "percentage points" unit fix (§5.1).
- [x] Theorem 1: C stated uniform over partitions (quantifier order).
- [x] Title kept; three alternatives left in comment above `\title` for author's choice.
- [x] Corollary numbering (`Corollary 1.1` style) — kept deliberately: it preserves the
  "Prop. 1 / Prop. 2 / Thm. 1" narrative numbering. Noted here so it reads as a choice.
- [x] Duplicate labels `sec:infomap`/`sec:theory` — kept (both are referenced; harmless).
- [ ] Multi-seed expansion of the training case study (≥5 seeds, rliable IQM/CI) — next
  collection cycle, per §App. "Open runs".

## Next paper (explicitly out of scope for this revision)

- Higher-demand (near-saturation) arm — tests the causal middle link where it has content.
- ONE preregistered partition-level Ψ_adj hypothesis (a named front partition vs. connected
  null) instead of edge families.
- Dynamic / regime-indexed repartitioning; real-world OD data.

## Verification

- [ ] `lualatex` compile check after edits (artifacts deleted from `src/` afterwards;
  user's build engine outputs to `out/`).
- [ ] When revision complete → run reviewer **re-review mode** against this file.
