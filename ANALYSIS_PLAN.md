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
- **Status (2026-07-02, updated):** full-state Ingolstadt21 D_MI is now complete (`state_diagnostics_full_state/state_diagnostics_summary.csv`), superseding the earlier `queue_total` proxy. **This fixed the direction problem** — all four I21 conditions now show within > cross MI (the proxy had metis_k4 reversed); `h1_pass_count` improved from 0/3 everywhere to 1/3 (flow_k4, metis_k4) and 2/3 (flow_k5, metis_k5). But **effect size remains far smaller than Cologne8's** (I21 within/cross gaps ~0.007–0.018 vs. C8's ~0.09–0.19) — H1 is directionally correct on I21 but still statistically marginal even at full state. On C8, `h1_pass_count` is still 3/3 only for flow_k3; C8 metis_k3/flow_k5/metis_k5 remain 0/3, and flow_k5's failure despite a comparable effect size to flow_k3's (0.178 vs. 0.190 gap) is still unexplained — needs per-seed inspection, not yet done. **H2's result remains the load-bearing fallback** per the paper's own Algorithm 1 logic, and it's not resolving: H2 "ran, but is underpowered because spill-back events are sparse" (user-confirmed) — literally zero events on every Cologne8 condition. Don't draft Introduction/Conclusion claiming H1/H2 verified until this resolves; may need to reframe H1/H2 as diagnostic rather than a hard pass/fail gate in the manuscript text regardless of which network.

### 2. $\Psi$ comparison — headline unifying figure
- [ ] **Calculation:** $\Psi(\mathcal{P}, D)$ for $\mathcal{P} \in \{\text{InfoMap}, \text{METIS}\}$, $D \in \{D^{\mathrm{MI}}, D^Q, D^G\}$, same $K$.
- **Prerequisite — resolved (2026-07-02), superseded by per-instrument status below.** Checkpoints for both global CoLight GAT and global MAPPO critic are confirmed to exist (see D^G/D^Q status lines). $D^Q$ additionally turned out to have an architectural obstacle beyond checkpoint availability — see below.
- **Expected result:** $\Psi_{\text{InfoMap}} > \Psi_{\text{METIS}}$ across all three instruments.
- **Visualization:** one grouped bar chart — x-axis $\{D^{\mathrm{MI}}, D^Q, D^G\}$, paired bars {InfoMap, METIS}, y-axis $\Psi \in [0,1]$.
- **Status (2026-07-02):** in progress, per-instrument.
  - $D^{\mathrm{MI}}$ leg: `state_diagnostics_summary.csv` produced — confirm it contains $\Psi(\mathcal P, D^{\mathrm{MI}})$ itself, not just the raw MI matrices.
  - $D^{G}$ leg: **done, headline-valid (2026-07-02), with a k=5 anomaly.** $\Psi(\mathcal P, D^G)$ on the shared global/original CoLight D_G matrix: flow_k4 = 0.798 > metis_k4 = 0.669 (✓ consistent with H); **flow_k5 = 0.700 < metis_k5 = 0.731 (✗ reverses H)**, even though $\Phi(\mathcal P, W)$ (pure flow retention) still favors flow at k=5 (0.792 vs 0.636) — the break happens specifically between flow-retention and model-dependency-retention at k=5. Worth checking once CoLight I21 k5 performance data exists, to see whether performance also reverses at k=5 (a clean test of whether $\Psi$ predicts performance, Item 4). Source: `analysis/outputs/model_dependency/psi/ingolstadt21_D_G_colight_original_seed7_gpu2/model_dependency_psi.csv`.
  - **Resolved via direct WandB check (2026-07-02):** confirmed via `mcp__wandb` query against project `hmarl_traffic_control` — none of the six logged Ingolstadt21 CoLight runs have `colight_partitioned_message_passing` set in config. The finished `flow_k4`/`metis_k4` runs (created 2026-05-26 23:33/23:34, seed 67) use a `signal_yaml` override pointing to a partition-specific topology file — i.e. the actual mechanism is restricting road-graph edges fed into the standard global-attention CoLight class, not the Appendix's documented "Variant A: PartitionedAttentionStack" flag. This is a plausible experimental design but the Appendix text (§Regional MARL Architecture) needs correcting to describe it accurately. It also confirms, independent of the earlier checkpoint-key mismatch, that `flow_k4`/`metis_k4` Jacobians would have structurally-zero cross-module entries even if the loader had succeeded (edges are deleted from the graph, not masked) — reinforcing that the shared-global-matrix approach above is the only valid one. Earlier runs (`flow_partition`/`metis_partition`/`default_fixed_topology`, created 2026-05-26 03:12–08:16, 5-module management, no `signal_yaml` override, seed unset) are a distinct, earlier generation — clarify which generation the Appendix's Table `i21_colight` numbers actually came from.
  - **Cologne8 D^G leg: done (2026-07-02).** flow_k3 = 0.754 > metis_k3 = 0.591 (✓); flow_k5 = 0.370 < metis_k5 = 0.476 (✗ reverses) — **the same k-dependent reversal as I21, now confirmed on a second, independent network.** This is a replicated finding, not an anomaly — treat as a real secondary result requiring explicit discussion in the manuscript, not omission. ρ(W,D_G) = 0.796 (p=2.23e-13) on C8, close to I21's 0.750 — D_G is scale-robust across networks, unlike D_MI (§ above, 0.514 C8 vs. 0.141 I21). Open caveat: the one available check of whether this diagnostic (computed on the *global* model) predicts actual trained-model performance (I21 Variant B at k=5) shows performance *not* reversing (flow still wins by ~4%) — undetermined whether that's proxy-vs-real-model mismatch or single-seed noise. Full detail and recommended next check (C8 CoLight k=5 performance) in `MANUSCRIPT_RESULTS_LOG.md` §5.
  - $D^{Q}$ leg: **resolved to a design decision (2026-07-02).** Confirmed via code read (`agents/policy/actor_critic.py:78,312`, `agents/common/marl.py:132,147`): MAPPO's global critic (`critic_scope: global`, the default) feeds every one of its `N` output rows the identical global input, so the "per-agent" value vector is `N` copies of one scalar — there is no target index $i$, and a full pairwise D^Q[i←j] genuinely cannot be extracted from existing checkpoints (not a rerun issue, an architecture fact). **Decision:** implement a reduced, explicitly-scoped L2 diagnostic instead — $g_j$ (critic source-sensitivity, gradient-based) and $\Gamma(P,g)$ (Shannon entropy of module-mass concentration, chosen over an HHI alternative). Full spec: `L2_CRITIC_DIAGNOSTIC_DESIGN.md`. True target-conditioned D^Q (requiring a decomposed-head critic and retraining) remains a separate, deferred decision. **Priority note stands:** MAPPO produces the paper's strongest result (2.85–3.99×) and was backed only by the borrowed L1 $D^{\mathrm{MI}}$ instrument until now — this closes that gap with an honestly-labeled diagnostic rather than an overclaimed one.

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
- **Status (2026-07-02):** in progress — CoLight attention-entropy hooks added; running against flow_k4/metis_k4 checkpoints (`analysis_dg_flow_k4`, `analysis_dg_metis_k4`).

### 6. Hop-distance dependency profile $\bar{D}_h$
- [ ] **Calculation:** aggregate $D^Q_{i \leftarrow j}$, $D^G_{i \leftarrow j}$ by road-graph hop distance $h$.
- **Expected result:** steep decay by $h=2$–3, giving a concrete minimum-module-radius figure to cite when explaining small-module saturation.
- **Visualization:** line plot, x = hop distance, y = mean $\bar{D}_h$, separate lines for $D^Q$ vs. $D^G$, both networks overlaid.
- **Status (2026-07-02):** $D^G$ leg done for both networks (see item 2 — computed from the shared global Jacobian matrix; the `flow_k4`/`metis_k4`-checkpoint attempts referenced in earlier drafts of this status line failed and were correctly discarded, not used). $D^Q$ leg: **not just blocked, architecturally inapplicable as a hop-distance profile** — this item needs a genuine pairwise $D_{i\leftarrow j}$ to bucket by graph distance $\rho(i,j)$, and the reduced L2 diagnostic (`g_j`, `L2_CRITIC_DIAGNOSTIC_DESIGN.md`) has no target index `i` at all, so there is no pair to bucket. This item's $D^Q$ leg is out of scope unless/until true target-conditioned $D^Q$ is built (separate, deferred decision, see item 2).

---

## Tier 3 — Lower priority (only if time permits after Tier 1–2)

- [ ] **7. Module-size ($k$) ablation** — performance vs. mean module size, locating the empirical saturation threshold explicitly.
- [x] **8a. Flow-retention $\Phi(\mathcal{P}, W)$** — anchors Stage 1 of the causal pipeline (see above). Cheap, computable directly on the OD matrix, no trained model required. **Candidate for promotion to Tier 1** — flag for decision. **Done (2026-07-02):** `analysis/outputs/flow_retention/flow_retention.csv`.
- [ ] **8b. Flow–dependency alignment $\rho(W,D)$** — anchors Stage 2 of the causal pipeline (see above), pairwise/partition-agnostic test of "does flow predict dependency." Also cheap. **Candidate for promotion to Tier 1** — flag for decision. **Status (2026-07-02):** D_MI variant likely computed as part of `state_diagnostics_summary.csv` — confirm the Spearman $\rho$ value is actually in that file before checking this off.

---

## Open Questions / Blockers

| # | Question | Blocks |
|---|----------|--------|
| 1 | Are global (unpartitioned) MAPPO/CoLight checkpoints saved from existing "no-partition" baseline runs? | Item 2 ($\Psi$ for $D^Q$/$D^G$), Item 6. **Update (2026-07-02):** CoLight side resolved — global/original checkpoint exists, D^G computed from it. MAPPO side (D^Q) is a separate, harder blocker: not just checkpoint existence but a target-conditioned global-critic probe that hasn't been built yet (see #5). |
| 2 | IDQN failure mode under regional reward averaging — root cause not yet investigated | L1 empirical scope (currently IPPO-only) |
| 3 | Ingolstadt21 Regional CoLight rerun — convergence status | Item 3 (L3 main result), Item 5 (saturation diagnostic needs the run to progress far enough to observe divergence/non-divergence). **Update (2026-07-02):** IPPO local seed0 baseline + CoLight flow_k4/metis_k4 seed7 refires running (`analysis_gpu2_queue`) — verdict expected once these complete. |
| 4 | Multi-seed expansion for L1/L2 (MAPPO+flow primary condition per `RESEARCH_PLAN.md` §7.1) | rliable IQM/CI in Item 3. **Note (2026-07-02):** today's H1/H2 warm-up traces use seeds 0–2 (3 seeds) — progress, but still short of the ≥5-seed target for the performance-metric rliable protocol specifically. |
| 5 | **(new, 2026-07-02)** Paper-grade $D^Q$ needs a target-conditioned global-critic probe — implementation task, not a rerun | Item 2 ($D^Q$ leg), Item 6 ($D^Q$ leg) |

---

## File Locations

| Artifact | Path |
|----------|------|
| This plan | `/workspace/ANALYSIS_PLAN.md` |
| Research plan (hypotheses, pilot status) | `/workspace/RESEARCH_PLAN.md` |
| Full metric brainstorm (superset of this plan) | `/workspace/metrics.md` |
| Numeric results ledger, organized by manuscript claim | `/workspace/MANUSCRIPT_RESULTS_LOG.md` |
| L2 critic diagnostic implementation spec | `/workspace/L2_CRITIC_DIAGNOSTIC_DESIGN.md` |
| Today's operational run log | `/workspace/RUN_LOG_2026-07-02.md` |
| Target paper draft | `/workspace/src/neurips_2026.tex` |
| Bibliography | `/workspace/src/refs.bib` |
