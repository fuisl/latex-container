# Submission Readiness Tracker

**Created:** 2026-07-01 (via academic-paper-reviewer trajectory assessment)
**Question answered:** *If `ANALYSIS_PLAN.md` is fully executed as scoped, does this reach A*/A Q1 standard?*
**Verdict source:** inline multi-lens review (EIC / methodology / domain / devil's-advocate lenses), not a fresh 5-agent panel — the draft is ~40% written (Background + Method complete; Intro/Related Work/Experiments/Conclusion are placeholders), so a literal panel would just re-report "sections missing," which isn't the useful signal right now. Re-run a full panel once §Intro/§Related Work/§Experiments are drafted and results are final.

---

## Bottom line

**Completing `ANALYSIS_PLAN.md` as written is necessary but not sufficient for A\*.** It is very plausibly sufficient for a strong **A/A− venue** (AAMAS, ITSC/T-ITS-adjacent ML venues) or a **Q1 transportation/ITS journal** (Transportation Research Part C, IEEE T-ITS) — arguably a *better* fit than a generalist A\* ML venue, because the contribution is domain-grounded empirical methodology, not a new algorithm or theorem.

For NeurIPS/ICML/AAAI-tier A*, two things in the current scope are load-bearing and neither is fixed by finishing the analysis plan alone:
1. The title/abstract claim ("across all coordination levels") is contradicted by the paper's own L3 (CoLight) data.
2. Empirical breadth is thin — 2 real networks, 1 non-flow baseline (METIS), no comparison against the closest prior work (Ma & Wu, GPLight) that the Related Work section will need to discuss qualitatively instead of empirically.

Neither is a plan-execution problem — they're scoping decisions that need an explicit call before the paper is written further.

---

## The five discriminating risks

| # | Risk | Status | Resolves via plan completion? |
|---|------|--------|-------------------------------|
| 1 | **Ψ (the headline metric) is not yet computed** — blocked on whether global-model checkpoints from existing no-partition runs were saved (Open Q #1 in `ANALYSIS_PLAN.md`) | Blocking, unresolved | Yes, if checkpoints exist. **Verify this first** — it gates whether Tier 1 Item 2 is even executable without expensive reruns. |
| 2 | **Title says "across all coordination levels"; L3 is negative** — CoLight+flow diverges on Cologne8 (+73% ATT), Ingolstadt21 CoLight run incomplete | Open, unresolved | Only if I21 CoLight (k=4, ~5 agents/module) turns around. If it doesn't, the title/abstract framing must retreat to "levels 1–2, with a documented L3 boundary condition" — **this is the single most reviewer-visible issue in the current draft**. |
| 3 | **Single-seed results throughout; rliable/IQM machinery invoked but not run** | Open, in Tier 1 #3/#4 | Yes — directly addressed by `ANALYSIS_PLAN.md` Tier 1, Open Q #4. Non-negotiable: the draft cites Henderson et al. and rliable explicitly, so a methodology reviewer *will* check whether the paper follows its own cited standard. |
| 4 | **Only 2 real networks** (Cologne8, Ingolstadt21) — main.tex's original proposal had 5–6 (6×6/10×10 grids, Jinan, Manhattan) | Scoped down deliberately per `docs/comments.md` ("don't combine too many objectives") | No — this is a ceiling on generality claims regardless of how well the 2 networks are executed. Acceptable for a focused A/Q1 paper; likely capped at A* without a 3rd network. |
| 5 | **No sparsification/random-partition control** — main.tex's L1.5 condition (random sparse graph, same degree as InfoMap) was dropped in the neurips scope-down | Not in `ANALYSIS_PLAN.md` | No — this is the internal-validity answer to "is the gain from flow-coherence specifically, or just from having *any* principled non-uniform partition instead of METIS's structural-balance objective?" METIS partially controls for this (it's not random), but a rigorous reviewer can still ask for the random-degree-matched control that the authors themselves previously judged necessary. Consider reinstating as a cheap ablation (no retraining needed beyond one extra condition per level) or explicitly justifying its removal in Limitations. |

---

## Devil's-advocate flag (would block "Accept" per skill's iron rule if this were a real panel)

**CRITICAL — overclaim in framing.** The strongest counter-argument a reviewer will make: *"InfoMap only reliably helps when paired with a centralized regional critic (L2, 2.85–3.99× on Ingolstadt21). L1 (reward-only) is directionally positive but noisy/unstable (cold-start, 26–83 instability spikes). L3 (attention) actively fails on the smaller network. The paper's title and Hypothesis H frame this as a uniform, level-agnostic advantage — the data instead show a level-*dependent* advantage that peaks at L2."* This must be resolved by either (a) I21 CoLight results turning around and being reported at full 1500 ep with multi-seed CIs, or (b) rewriting the central claim to be honest about level-dependence before the Introduction/Conclusion are drafted — doing it after would mean rewriting the framing invisibly baked into every section.

**Secondary, non-blocking:** the Background section still frames the setup as an "ND-POMDP" (§2.1, `neurips_2026.tex`). `docs/comments.md` already flagged (correctly) that ND-POMDP formally requires transition independence, observation independence, and reward locality (Nair et al. 2005) — the current draft doesn't establish these three conditions hold, it just uses the reward-decomposition equation informally. Less totalizing than `main.tex`'s heavier ND-POMDP theorizing (already toned down — good), but still worth either (a) explicitly stating which of the 3 conditions hold/are assumed, or (b) softening to "coordination-graph framing inspired by ND-POMDP" rather than claiming the formalism outright.

---

## Citation-accuracy carryover from `docs/comments.md` (advisor feedback, already given once)

These were flagged against `main.tex`'s Related Work and must not reappear when `neurips_2026.tex`'s Related Work (currently "[To be written — Step 5]") is drafted:
- HiLight — is a hierarchical policy with sub-policies optimizing trip time; **does not** do partitioning/subregions as `main.tex` implied.
- IMAC — bandwidth-constrained communication; no "80% message reduction" claim exists in that work.
- Reference [18] (main.tex numbering) — about clustering travel patterns, not TSC; no "adjacency-based delay/speed" result.
- GPLight — MI-based grouping should be framed as a flow/topology-adjacent method, not a separate category.
- Ma & Wu — uses GNN/MCTS, which is an *implicit* flow-based method — frame the InfoMap vs. Ma&Wu distinction as explicit-vs-implicit flow methods, per the advisor's suggested narrative axis.
- Prefer peer-reviewed venues over arXiv preprints when a citation choice exists.
- Advisor also suggested the narrative could be organized around the **explicit vs. implicit flow-based** axis (InfoMap vs. GNN/attention-learned) rather than treating "flow-based" as a monolithic category — worth deciding before drafting Related Work, since it changes the section's structure, not just its content.

---

## Target-venue calibration

| Tier | Plausible? | Condition |
|------|-----------|-----------|
| NeurIPS/ICML/AAAI (generalist A*) | Unlikely as scoped | Needs: L3 resolved or claim retreat, 3rd network, empirical (not just qualitative) comparison to ≥1 closest prior work (Ma & Wu or GPLight), full rliable multi-seed |
| AAMAS / ITSC-adjacent ML venue (A) | **Plausible** | Requires items 1–3 above (checkpoints, honest L3 framing, multi-seed) done; 2 networks is acceptable at this tier |
| IEEE T-ITS / Transportation Research Part C (Q1 journal) | **Plausible, arguably best fit** | Same as above; journal format tolerates the domain-grounded empirical contribution better than a generalist ML A* venue would |
| Strong workshop | Already cleared | Current state (pilot results + method) would already pass a workshop bar |

---

## Immediate next actions (priority order)

1. **Resolve Open Q #1** — confirm whether global (unpartitioned) MAPPO critic / CoLight GAT checkpoints exist from prior no-partition runs. This gates Tier 1 Item 2 (Ψ) and Tier 2 Item 6.
2. **Decide the L3 framing now, not after drafting** — either commit to finishing the I21 CoLight rerun to a real verdict, or pre-write the Introduction/Conclusion around a level-dependent (not uniform) claim.
3. Execute Tier 1 (H1/H2 gate, Ψ, main results, Ψ-predicts-performance) — this is the paper's evidentiary core regardless of venue.
4. Multi-seed expansion (≥5 seeds) for the primary MAPPO+flow condition on Ingolstadt21 — non-negotiable given the paper cites Henderson/rliable itself.
5. Decide on reinstating an L1.5-style random-degree-matched control, or write an explicit Limitations sentence justifying its absence.
6. When drafting Related Work (Step 5) and Introduction (Step 6): apply the citation-accuracy corrections above verbatim; consider the explicit-vs-implicit-flow narrative axis.
7. Re-run a full 5-reviewer panel (`academic-paper-reviewer` full mode) once Introduction/Related Work/Experiments are drafted and Tier 1 results are in — that's when a literal per-section review becomes informative rather than redundant with this tracker.

---

## File cross-references

| Artifact | Path |
|----------|------|
| This tracker | `/workspace/SUBMISSION_TRACKER.md` |
| Results/analysis plan | `/workspace/ANALYSIS_PLAN.md` |
| Research plan (hypotheses, pilot status) | `/workspace/RESEARCH_PLAN.md` |
| Target paper (NeurIPS format, in progress) | `/workspace/src/neurips_2026.tex` |
| Original full proposal (LLNCS format, superset) | `/workspace/src/main.tex` |
| Prior human advisor feedback (scope + citation issues) | `/workspace/docs/comments.md` |
| Metric brainstorm (superset of ANALYSIS_PLAN) | `/workspace/metrics.md` |
