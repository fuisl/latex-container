# Analysis Plan — Results Chapter (NeurIPS 2026 Draft)

**Status:** Planning complete · Implementation not started
**Document:** Tracking reference — created 2026-07-01
**Parent docs:** `RESEARCH_PLAN.md` (hypotheses, pilot status), `metrics.md` (full metric brainstorm — this plan is the scoped-down subset actually being implemented), `src/neurips_2026.tex` (target paper)

Scope discipline note: this plan intentionally implements a subset of `metrics.md`'s full metric list, per the earlier reviewer feedback (`docs/comments.md`) against combining too many objectives. Tier 3 items are explicitly deprioritized.

---

## Locked scope going into this analysis

- **L1 = IPPO only** (IDQN deferred pending investigation into its failure mode under regional reward averaging — see Open Questions).
- **L2 = MAPPO**, **L3 = CoLight** (Ingolstadt21 Regional CoLight currently being rerun).
- Baselines: **None (no partition) → METIS → InfoMap**. Ma & Wu (adaptive GNN/MCTS partition) and FMA2C are **not** empirical baselines this round — argued qualitatively in Related Work only.
- Claim being tested is **comparative** (InfoMap beats METIS/None), **not optimality**.

---

## Causal Pipeline & Evidence Mapping

The paper's argument is a five-stage causal chain. Each stage below states the
claim, which analysis item(s) test it empirically in *this* paper, what the
literature already establishes (so we're not re-proving it from scratch), and
what remains genuinely novel here.

| Stage | Claim | Tested by | Literature already establishes | Novel to this paper |
|---|---|---|---|---|
| **1. InfoMap preserves flow** | InfoMap retains more within-module OD flow than METIS | Tier 3 #8a ($\Phi(\mathcal P, W)$) | Map equation is *defined* to minimize random-walk description length, which mathematically maximizes within-module flow retention (`rosvall2008maps`, `rosvall2009mapequation`); `lucchini2023intraod` confirms empirically on real urban OD data (82.9% stable community membership) | The margin over METIS specifically, on Cologne8/Ingolstadt21 road networks — not previously measured |
| **2. Flow preserved → dependency preserved** | High-OD-flow pairs are also high-MI/spillback-coupled pairs | Tier 1 #1 (H1/H2) + Tier 3 #8b ($\rho(W,D)$) | `dependencydyn2025` establishes the mechanism generally (coordination necessary iff spillback couples queues); `stmarl2020` establishes spatial MI dominance in TSC generally | That InfoMap partition boundaries *specifically* align with where this dependency concentrates — neither prior work tests InfoMap |
| **3. Dependency retention → coordination quality** | Higher $\Psi$ corresponds to better-structured coordination (correlated rewards for L1, dependency-aligned critic for L2, attention-concentrated-within-module for L3) | Tier 1 #2 ($\Psi$ comparison, used as the coordination-quality proxy) + Tier 2 #5/#6 (**L3 only** — attention entropy, hop-distance profile) | The Jacobian dependency instrument itself is borrowed from `lrd2025` (there, diagnosing GNN over-squashing) | Applying it to ask whether a *partition* aligns with what a model depends on is a distinct question `lrd2025` never asks (already noted in `main.tex`). **Gap: no direct coordination-quality metric for L1 (reward correlation) or L2 (critic approximation error) — $\Psi$ alone stands in for both, by scope decision, not measurement** |
| **4. Coordination quality → RL learning quality** | Better-structured coordination improves sample efficiency/stability | Tier 1 #3 (AUC-LC, ET, Late-$\sigma$) + Tier 1 #4 ($\Delta\Psi$ vs. $\Delta$AUC-LC scatter) | General RL/MARL theory supports variance reduction from better credit assignment; `expocomm2025` shows pre-designed topologies improve MARL sample efficiency in general | The specific magnitude/direction for InfoMap vs. METIS on TSC — genuinely new |
| **5. Better RL → better TSC outcome** | Lower ATT/waiting time/queue | Tier 1 #3 (final ATT, Delay, Trip, Wait, Queue) | Standard MARL-TSC evaluation convention; `henderson2018matters` and `agarwal2021rliable` establish *how* to measure this rigorously (already adopted) | N/A — this is the measured outcome, not a claim needing separate literature support |

**Two things this mapping surfaces:**

1. **Tier 3 items #8a/#8b are not "nice-to-have" — they anchor Stages 1 and 2, the opening links of the chain.** They're also the cheapest to compute (no trained-model dependency, direct on the OD matrix). Worth reconsidering whether they should move to Tier 1 despite the original prioritization, since without them, Stage 1's claim rests entirely on theoretical/literature grounding rather than this paper's own measurement.
2. **Stage 3 has a real scope gap at L1/L2**: unlike L3 (which gets a dedicated mechanism diagnostic via attention entropy/hop-distance), L1 and L2's "dependency retention → coordination quality" step is not independently verified — $\Psi$ itself is the only evidence. This is a defensible scope decision (avoids the metric sprawl `docs/comments.md` warned against — reward-correlation and critic-approximation-error metrics from `metrics.md` are deliberately excluded), but it should be stated as an explicit scope boundary in the paper, not left implicit.

---

## Tier 1 — Must-have (directly answers H1, H2, H/OP1–OP3)

### 1. H1/H2 pre-training gate
- [ ] **Calculation:** KSG-estimator MI $\hat{I}(X_i(t); X_j(t+\tau))$ for all agent pairs, $\tau \in \{1,5,15,30\}$, on warm-up trajectories. Classify pairs within/cross InfoMap module. Wilcoxon signed-rank test, $p<0.05$.
- [ ] **Calculation:** Spill-back event extraction from SUMO queue trajectories (queue exceeds capacity at consecutive intersections). $\Pr(\text{within-module})$ vs. $\Pr(\text{cross-module})$, one-sample proportion test.
- **Expected result:** within-module MI and spill-back proportion both significantly higher than cross-module.
- **Visualization:** $|\mathcal{V}| \times |\mathcal{V}|$ MI heatmap with InfoMap module boundaries overlaid. One per network (Cologne8, Ingolstadt21).
- **Status:** not started.

### 2. $\Psi$ comparison — headline unifying figure
- [ ] **Calculation:** $\Psi(\mathcal{P}, D)$ for $\mathcal{P} \in \{\text{InfoMap}, \text{METIS}\}$, $D \in \{D^{\mathrm{MI}}, D^Q, D^G\}$, same $K$.
- **Prerequisite (blocking):** $D^Q$/$D^G$ require Jacobians from the trained **global** (unpartitioned) MAPPO critic and CoLight GAT. **Need to confirm checkpoints from existing "no-partition" baseline runs are saved, or add checkpoint-saving to the current rerun.**
- **Expected result:** $\Psi_{\text{InfoMap}} > \Psi_{\text{METIS}}$ across all three instruments.
- **Visualization:** one grouped bar chart — x-axis $\{D^{\mathrm{MI}}, D^Q, D^G\}$, paired bars {InfoMap, METIS}, y-axis $\Psi \in [0,1]$.
- **Status:** not started; blocked on checkpoint confirmation.

### 3. Main performance results
- [ ] **Calculation:** for each (algorithm, partition) in {IPPO, MAPPO, CoLight} × {None, METIS, InfoMap}: IQM + stratified bootstrap CI where $\geq$5 seeds exist (L1/L2 target); single-seed point estimate, explicitly hedged as preliminary, for L3 pending the current rerun. AUC-LC, ET($\leq t$), Late-$\sigma$ throughout.
- **Expected result:** InfoMap $<$ METIS $<$ None (lower ATT), statistically supported at L1/L2, directional only at L3.
- **Visualization:**
  - (a) Learning curves — one panel per algorithm, lines = {None, METIS, InfoMap}, CI shading where multi-seed available.
  - (b) One summary table, both networks.
  - (c) rliable performance-profile / probability-of-improvement plot, InfoMap vs. METIS, wherever seed count supports it.
- **Status:** partial data exists (Cologne8, Ingolstadt21 pilot in `RESEARCH_PLAN.md` §4); needs multi-seed expansion for L1/L2 and CoLight-I21 completion for L3.

### 4. $\Psi$ predicts performance — evidence-chain-closing plot
- [ ] **Calculation:** scatter of $\Delta\Psi$ (InfoMap $-$ METIS) vs. $\Delta$AUC-LC per (algorithm, network, $k$) condition. Report correlation coefficient.
- **Expected result:** positive correlation — empirically closes "flow retention → dependency retention → better RL outcome."
- **Visualization:** single scatter plot with fitted trend line, one point per tested condition.
- **Status:** not started; depends on Tier 1 items 2 and 3 being complete first.

---

## Tier 2 — Targets the L3 saturation hypothesis (reuses runs already being generated, no new experiments required)

### 5. Attention saturation diagnostic
- [ ] **Calculation:** per-episode attention entropy $H(\alpha_{i \cdot})$ or influence-weighted range $\hat{\rho}_u$ for CoLight (flow-partitioned), tracked across training, on **both** Cologne8 (small modules, ~2–3 agents) and Ingolstadt21 (larger modules, ~4–5 agents).
- **Expected result:** Cologne8 shows entropy/attention collapsing as training progresses; Ingolstadt21 does not. Direct empirical test of the module-size saturation hypothesis using existing runs — no synthetic/new network required.
- **Visualization:** line plot, x = episode, y = attention entropy (or $\hat{\rho}_u$), two lines (Cologne8 vs. Ingolstadt21), marker at Cologne8's divergence point (~ep 700 per pilot notes).
- **Status:** not started.

### 6. Hop-distance dependency profile $\bar{D}_h$
- [ ] **Calculation:** aggregate $D^Q_{i \leftarrow j}$, $D^G_{i \leftarrow j}$ by road-graph hop distance $h$.
- **Expected result:** steep decay by $h=2$–3, giving a concrete minimum-module-radius figure to cite when explaining small-module saturation.
- **Visualization:** line plot, x = hop distance, y = mean $\bar{D}_h$, separate lines for $D^Q$ vs. $D^G$, both networks overlaid.
- **Status:** not started; shares the $D^Q$/$D^G$ checkpoint prerequisite with item 2.

---

## Tier 3 — Lower priority (only if time permits after Tier 1–2)

- [ ] **7. Module-size ($k$) ablation** — performance vs. mean module size, locating the empirical saturation threshold explicitly.
- [ ] **8a. Flow-retention $\Phi(\mathcal{P}, W)$** — anchors Stage 1 of the causal pipeline (see above). Cheap, computable directly on the OD matrix, no trained model required. **Candidate for promotion to Tier 1** — flag for decision.
- [ ] **8b. Flow–dependency alignment $\rho(W,D)$** — anchors Stage 2 of the causal pipeline (see above), pairwise/partition-agnostic test of "does flow predict dependency." Also cheap. **Candidate for promotion to Tier 1** — flag for decision.

---

## Open Questions / Blockers

| # | Question | Blocks |
|---|----------|--------|
| 1 | Are global (unpartitioned) MAPPO/CoLight checkpoints saved from existing "no-partition" baseline runs? | Item 2 ($\Psi$ for $D^Q$/$D^G$), Item 6 |
| 2 | IDQN failure mode under regional reward averaging — root cause not yet investigated | L1 empirical scope (currently IPPO-only) |
| 3 | Ingolstadt21 Regional CoLight rerun — convergence status | Item 3 (L3 main result), Item 5 (saturation diagnostic needs the run to progress far enough to observe divergence/non-divergence) |
| 4 | Multi-seed expansion for L1/L2 (MAPPO+flow primary condition per `RESEARCH_PLAN.md` §7.1) | rliable IQM/CI in Item 3 |

---

## File Locations

| Artifact | Path |
|----------|------|
| This plan | `/workspace/ANALYSIS_PLAN.md` |
| Research plan (hypotheses, pilot status) | `/workspace/RESEARCH_PLAN.md` |
| Full metric brainstorm (superset of this plan) | `/workspace/metrics.md` |
| Target paper draft | `/workspace/src/neurips_2026.tex` |
| Bibliography | `/workspace/src/refs.bib` |
