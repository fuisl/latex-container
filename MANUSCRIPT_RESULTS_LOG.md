# Manuscript Results Log

**Purpose:** durable record of actual numeric findings, organized by the claim/section of `neurips_2026.tex` they'll eventually feed, so drafting Introduction/Experiments/Appendix later doesn't require re-deriving anything from `RUN_LOG_*.md` files or chat history. Update this file whenever a result changes; don't delete superseded numbers, mark them superseded (proxies/old generations are useful context for why a claim reads the way it does).

**Related:** `L2_CRITIC_DIAGNOSTIC_DESIGN.md` is the implementation spec for the new L2 diagnostic introduced in §5b below — read that file when writing code, this file when writing the manuscript.

---

## 1. H1 — Spatial MI Advantage (feeds §3.2, Eq. h1, Algorithm 1)

**Test:** Wilcoxon signed-rank, within-module vs. cross-module KSG MI, 3 seeds per condition, p<0.05.

| Network | Condition | k | mean within-MI | mean cross-MI | gap | pass count (of 3 seeds) |
|---|---|---|---|---|---|---|
| Cologne8 | flow | 3 | 0.5415 | 0.3510 | 0.190 | **3/3** |
| Cologne8 | metis | 3 | 0.5369 | 0.4251 | 0.112 | 0/3 |
| Cologne8 | flow | 5 | 0.5929 | 0.4149 | 0.178 | 0/3 |
| Cologne8 | metis | 5 | 0.5340 | 0.4434 | 0.091 | 0/3 |
| Ingolstadt21 (`queue_total` proxy, **superseded**) | flow | 4 | 0.124 | 0.104 | 0.020 | 0/3 |
| Ingolstadt21 (`queue_total` proxy, **superseded**) | metis | 4 | 0.104 | 0.110 | **−0.006 (reversed)** | 0/3 |
| Ingolstadt21 (`queue_total` proxy, **superseded**) | flow | 5 | 0.140 | 0.0998 | 0.041 | 0/3 |
| Ingolstadt21 (`queue_total` proxy, **superseded**) | metis | 5 | 0.0921 | 0.112 | **−0.019 (reversed)** | 0/3 |
| Ingolstadt21 (full-state, current) | flow | 4 | 0.5058 | 0.4986 | 0.0072 | 1/3 |
| Ingolstadt21 (full-state, current) | metis | 4 | 0.5095 | 0.4979 | 0.0117 | 1/3 |
| Ingolstadt21 (full-state, current) | flow | 5 | 0.5134 | 0.4968 | 0.0166 | 2/3 |
| Ingolstadt21 (full-state, current) | metis | 5 | 0.5147 | 0.4976 | 0.0171 | 2/3 |

**Honest read for the manuscript:** full-state I21 fixed the *direction* problem (proxy had metis_k4/k5 reversed) but effect size is an order of magnitude smaller than Cologne8's, and pass rate is still 1–2 of 3 seeds, not robust. Cologne8 itself only cleanly passes for flow_k3 — flow_k5 fails despite a comparable gap to flow_k3 (0.178 vs. 0.190), which is unexplained (needs per-seed KSG values, not yet pulled). **Do not write "H1 verified" without qualification.** If this doesn't improve with more seeds, the manuscript needs to either (a) report H1 as network/k-dependent with an honest boundary discussion, or (b) lean more on H2/Ψ as the supporting evidence and describe H1 as directionally-consistent-but-not-always-significant.

Sources: `analysis/outputs/state_diagnostics/state_diagnostics_summary.csv` (C8 + old I21 proxy), `analysis/outputs/state_diagnostics_full_state/state_diagnostics_summary.csv` (I21 full-state).

---

## 2. H2 — Spill-back Containment (feeds §3.2, Eq. h2)

**Status: not usable yet.** Mean spill-back events per seed: **Cologne8 = 0.0 for every condition** (flow_k3/metis_k3/flow_k5/metis_k5) — literally no extracted events, so the proportion test has nothing to test. Ingolstadt21 showed a nonzero mean (1.0/seed) under the old proxy run, but user confirms (2026-07-02) H2 "ran, but is underpowered because spill-back events are sparse" generally. **This is currently the weakest link in the H2⇒H1⇒H causal chain the manuscript's method section (§3.2) narrates** — worse than H1's marginal significance, since there's no data at all on C8. Needs longer/stress warm-up traces (already flagged as pending in `RUN_LOG_2026-07-02.md`) before this can support any manuscript claim. Until then, the manuscript's Algorithm 1 language ("if H1 fails, halt and revise") needs softening — a hard gate can't be enforced on a mechanism test that returns no data.

---

## 3. Φ(P,W) — Flow Retention (feeds Tier 3 #8a, causal-chain Stage 1)

| Network | k | Φ_flow | Φ_metis |
|---|---|---|---|
| Cologne8 | 3 | 0.939 | 0.614 |
| Cologne8 | 5 | 0.569 | 0.415 |
| Ingolstadt21 | 4 | 0.817 | 0.643 |
| Ingolstadt21 | 5 | 0.792 | 0.636 |

Robust and consistent — flow beats METIS at every (network, k). This is close to definitional (InfoMap directly optimizes within-module flow), but it's the empirical confirmation the paper needs regardless, and it's clean. Source: `analysis/outputs/flow_retention/flow_retention.csv`.

---

## 4. Ψ(P, D_MI) — Dependency Retention, MI instrument (feeds §3.3, Eq. psi, headline Fig. Ψ comparison)

| Network | k | Ψ_flow | Ψ_metis | ρ(W, D_MI) |
|---|---|---|---|---|
| Cologne8 | 3 | 0.640 | 0.296 | 0.514 |
| Cologne8 | 5 | 0.280 | 0.126 | 0.514 |
| Ingolstadt21 (full-state) | 4 | 0.2455 | 0.2181 | 0.1409 |
| Ingolstadt21 (full-state) | 5 | 0.2199 | 0.1665 | 0.1409 |

Consistent with H at every (network, k) — this is the cleanest headline result available right now. Note ρ(W,D_MI) is markedly stronger on Cologne8 (0.514) than Ingolstadt21 (0.1409, even after the full-state fix) — flow and MI-dependency are more tightly coupled on the small network; worth a sentence in Discussion/Limitations rather than treating the two networks as interchangeable evidence for the same effect size.

---

## 5. Ψ(P, D_G) — Dependency Retention, CoLight Jacobian instrument (feeds §3.3, L3 row of headline comparison)

| Network | k | Ψ_flow | Ψ_metis | Consistent with H? |
|---|---|---|---|---|
| Ingolstadt21 | 4 | 0.798 | 0.669 | ✓ |
| Ingolstadt21 | 5 | 0.700 | 0.731 | **✗ reverses** |
| Cologne8 | 3 | 0.754 | 0.591 | ✓ |
| Cologne8 | 5 | 0.370 | 0.476 | **✗ reverses** |

ρ(W, D_G): I21 = 0.750 (p=3.98e-77, n=420); **C8 = 0.796 (p=2.23e-13)** — both strong and stable across network scale, unlike ρ(W,D_MI) (§4), which dropped sharply from C8 (0.514) to I21 (0.141). D_G looks like a more scale-robust instrument than D_MI here — worth a sentence in Discussion.

**The k-reversal is now a replicated, cross-network finding, not a one-off anomaly — treat it as a real secondary result, not noise.** Smaller k favors flow on both networks (C8 k=3, I21 k=4); larger k favors METIS on both (C8 k=5, I21 k=5). Φ(P,W) favors flow at every k on both networks (§3), so the break is specifically between flow-retention and *the trained global model's* dependency structure as modules shrink/multiply — this is a quantitative companion to the already-existing L3 module-size-saturation hypothesis (attention entropy conjecture in `RESEARCH_PLAN.md`), not a contradiction of it.

**Important open caveat — diagnostic vs. actual trained performance may not agree.** Ψ(D_G) here comes from the *global* (no-partition) model's Jacobian — a diagnostic about what a partition *should* do, not a direct measurement of an actually-trained regional model (which, per §6 below, is often a structurally different model — e.g. `CoLightRegional`/Variant B — that has no single unified Jacobian at all). The one place this can currently be checked is Ingolstadt21 Variant B at k=5: actual trained performance is flow=629.34 vs. metis=656.28 wait-time (**flow still wins, ~4% margin**) — the opposite direction from what Ψ(D_G) predicts at that k. This could mean the global-model proxy doesn't fully capture what a regionally-trained model learns, or it could be single-seed noise on a small margin — undetermined with current data. **Recommended next step:** get Cologne8 CoLight performance at k=5 (only k=3 currently exists) as a second, cheap check of whether the Ψ(D_G) reversal predicts an actual performance reversal anywhere, before treating the diagnostic as validated.

Sources: I21 — `analysis/outputs/model_dependency/psi/ingolstadt21_D_G_colight_original_seed7_gpu2/model_dependency_psi.csv`, global Jacobian `.../ing21_colight_original_seed7_gpu2_refire_dg/model_dependency.npz`. C8 — `analysis/outputs/model_dependency/psi/cologne8_D_G_colight_original_seed7/model_dependency_psi.csv`, global Jacobian `.../cologne8_colight_original_seed7_global_dg/model_dependency.npz`.

---

## 5b. D^Q status — re-scoped (2026-07-02)

**L1 (IPPO) is not under-analyzed — D_MI is its correct, dedicated, complete instrument by design (Jacobians don't apply to independent actors).** The real asymmetry is L2 (MAPPO): its dedicated instrument, D^Q, has never been computed, even though MAPPO produces the paper's strongest result (2.85–3.99×, §1 causal-chain Stage 4/5). It's currently backed only by the borrowed L1 D_MI instrument — worth fixing before further L3/CoLight work, since MAPPO is the headline number.

**Checked directly via WandB — checkpoint is not the blocker:**
- `ing21_mappo_original_global_gpu0_wandb`: `critic_scope: global`, `reward_scope: global_mean`, `save_model: True`, finished (2026-06-23).
- `cologne8+mappo+20260611_130731`: `save_model: True`, finished (2026-06-11), `management` populated; `critic_scope` not explicit in config — confirm this is the intended global-critic baseline before using it.

**The actual blocker is architectural — confirmed via code read (2026-07-02).** `agents/policy/actor_critic.py:78`: critic is an MLP `state_dim -> 1` applied across the `N` rows of `critic_obs`. `agents/common/marl.py:132,147`: for `critic_scope == "global"` (MAPPO's default, `actor_critic.py:312`), `CentralizedInputBuilder` gives every row the **identical** global concatenation. So the "per-agent" value vector is `N` copies of one scalar — there is no target index `i`, and a full pairwise D^Q[i←j] cannot be extracted from the existing global checkpoints at all, confirmed rather than merely suspected.

**Decision (2026-07-02): implement a reduced, explicitly-scoped L2 diagnostic now; defer true target-conditioned D^Q as a separate, later decision (would require retraining a decomposed-head critic).** Full implementation spec, formal definitions, citations, and naming discipline: see `L2_CRITIC_DIAGNOSTIC_DESIGN.md`. Summary:
- `g_j = Σ_k |∂V/∂X_{j,k}|` — critic source-sensitivity vector, partition-independent, computed once per checkpoint. Grounded in gradient-saliency literature (`simonyan2013saliency`, `sundararajan2017axiomatic`), same instrument family as the existing `lrd2025`-based D^G.
- `Γ(P,g) = -Σ_k p_k log p_k` — **Shannon entropy** (Option A, chosen over an HHI/participation-ratio alternative) of the module-mass distribution under partition P. Grounded in `yu2023lowentropymarl` (direct MARL-communication-entropy precedent) and consistent with the paper's own information-theoretic idiom and the already-planned Tier 2 #5 attention-entropy diagnostic.
- **Naming discipline (critical):** Γ is not Ψ — no pairwise matrix, no target index, cannot test within/cross-module dependency retention, only "does the partition group sensitive agents together." Must not be labeled Ψ(P,D_Q) anywhere in code, file names, or manuscript text. See design doc §2 for the full rationale and required output-path separation.
- Checkpoints confirmed via WandB: I21 (`ing21_mappo_original_global_gpu0_wandb`, `critic_scope: global`, `save_model: True`) ready; C8 (`cologne8+mappo+20260611_130731`) needs a quick `critic_scope` confirmation before use.
- Known limitations to carry into the manuscript: gradient saturation (Sundararajan et al.'s own motivation for Integrated Gradients — applies to the whole Jacobian-instrument family, not just this one), and concentration ≠ functional importance (Jain & Wallace 2019 caveat — not yet re-verified this session, confirm before citing).
- **Do not pool ΔΓ into the same Tier 1 #4 scatter as ΔΨ(D_MI)/ΔΨ(D_G)** — report as a separate, clearly-labeled panel.

---

## 6. Architecture/mechanism findings — Appendix corrections needed (§Regional MARL Architecture)

Checked directly via WandB (`hmarl_traffic_control` project), not inferred:

- **Ingolstadt21** `flow_k4`/`metis_k4` CoLight runs: algorithm=`CoLight` (base/global class), no `colight_partitioned_message_passing` flag, but `signal_yaml` points to a partition-specific topology file. Mechanism = restrict road-graph edges fed into the standard global-attention class. **Not** the Appendix's documented Variant A (`PartitionedAttentionStack`).
- **Cologne8** `flow_k3`/`metis_k3` CoLight runs: algorithm=`CoLightRegional` — this **is** the Appendix's Variant B (separate independent learner/replay buffer per region).
- **Cologne8** `original_no_partition`: algorithm=`CoLight`, `colight_partitioned_message_passing: False` — confirmed valid, genuinely global.

**Consequence for the manuscript: the two networks' "regional CoLight" results were produced by two different mechanisms** (I21 = topology-restricted global CoLight; C8 = Variant B CoLightRegional). The current Appendix text describes Variant A and Variant B as if either could apply uniformly, but as logged, I21 used neither flag-based variant and C8 used only Variant B. Before the Appendix is finalized: (a) confirm whether this per-network mismatch is intentional (e.g., Variant B was tried on C8, found to interact badly with small modules, and I21 deliberately switched approach) or accidental; (b) if intentional, say so explicitly and justify it; (c) either way, correct the architecture description so it matches what actually produced each table's numbers, and note which run generation (I21 has two: an earlier 5-module `_partition` set and a later 4-module `_k4` set — see `RUN_LOG_2026-07-02.md`) the currently-reported table numbers came from.

---

## 7. Performance results (existing, pre-2026-07-02 pilot — not re-verified today)

Already in the manuscript: `neurips_2026.tex` Appendix Tables `tab:c8_full`, `tab:colight`, `tab:i21_mappo_ippo`, `tab:i21_colight`. Known gaps as of 2026-07-02, relevant when revising those tables:
- All single-seed except CoLight (seed 7); no rliable IQM/CI possible yet.
- Cologne8: k=3 only, no k=5 performance runs exist (but k=5 Ψ/Φ/H1 diagnostics do — see §1/§3/§4 above, so there's diagnostic data with no matching performance data at that k on C8).
- Ingolstadt21 CoLight: still incomplete/being refired as of 2026-07-02 (Open Question #3).
- No AUC-LC/ET computed for CoLight on either network — only final ATT/late-mean/late-σ.

---

## Open items before any of this goes into a manuscript draft

1. H1/H2 framing in §3.2 needs to soften from "mandatory gate, halt on failure" to something that matches the actual evidentiary picture (marginal H1, empty H2).
2. Appendix §Regional MARL Architecture needs rewriting to match actual per-network mechanisms (§6 above).
3. ~~Cologne8 Ψ(P,D_G) still pending~~ — **done (2026-07-02)**, see §5. Confirms the k-reversal is a replicated cross-network finding.
4. The k=5 reversal (§5, now on both networks) needs an explicit discussion in the manuscript — this is a real, replicated result, not something to omit or bury. Decide whether it becomes its own small result/figure (recommended, given it's now cross-network) or a Limitations paragraph.
5. Confirm which I21 CoLight run generation (see §6) the currently-drafted Appendix tables' numbers came from.
6. **New:** get Cologne8 CoLight performance at k=5 (only k=3 exists) to check whether the Ψ(D_G) reversal predicts an actual trained-model performance reversal — the one existing check (I21 Variant B, k=5) shows performance *not* reversing despite Ψ(D_G) reversing, which needs resolving before claiming Ψ(D_G) predicts performance (Tier 1 #4).
7. ~~check the MAPPO critic's output-layer architecture~~ — **done (2026-07-02)**, confirmed via code read: single joint scalar, no target index. See §5b and `L2_CRITIC_DIAGNOSTIC_DESIGN.md` for the resulting implementation spec (Shannon-entropy-based Γ diagnostic, decision finalized).
8. **New:** implement the Γ diagnostic per `L2_CRITIC_DIAGNOSTIC_DESIGN.md` — confirm Cologne8's `critic_scope` first (design doc §4), then compute `g_j`/`Γ(P,g)` for both networks at matching k, following the output-path and naming discipline in the design doc §2/§6.
