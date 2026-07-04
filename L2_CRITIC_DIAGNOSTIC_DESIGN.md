# L2 (MAPPO) Reduced Critic Diagnostic — Implementation Design

**Status:** Design finalized (2026-07-02) — Shannon entropy (Option A) selected. Ready for implementation.
**Context:** full background/derivation in `MANUSCRIPT_RESULTS_LOG.md` §5b. This document is the implementation spec — read that section first if the *why* isn't clear; this file only covers the *what* and *how*.
**Parent docs:** `ANALYSIS_PLAN.md` (Tier 1 #2, D^Q leg), `RUN_LOG_2026-07-02.md`.

---

## 1. Purpose

The paper's method section defines a dedicated dependency instrument per coordination level: D^MI for L1, D^Q for L2, D^G for L3. D^Q as originally defined (`Section 3.3`, Eq. djac) requires a per-target-agent critic output `V_i(s)` — confirmed via code read (`agents/policy/actor_critic.py:78`, `agents/common/marl.py:132,147`) that the current global MAPPO critic does not provide this: `critic_scope == "global"` feeds every row of `critic_obs` the identical concatenation, so the critic's "per-agent" output vector is `N` copies of one scalar. **There is no target index `i`.** A full pairwise D^Q[i←j] cannot be extracted from existing checkpoints without retraining a decomposed-head critic — a separate, larger decision, not part of this design.

This document specifies a **reduced, honestly-scoped L2 diagnostic** that can be computed now, from existing checkpoints, with no retraining.

---

## 2. Naming discipline — read this before writing any code or file names

**Do not call anything in this diagnostic "Ψ" or "D_Q" without the word "reduced."** Ψ(P,D) is defined over pairs (Eq. psi) — it needs both `i` and `j` to classify a pair as within- or cross-module. The quantities below have no target index at all; they cannot answer "is dependency preserved within modules," only "does the partition group sensitive agents together." These are related but different claims. Conflating them is exactly the kind of error a Devil's Advocate review pass would flag.

| Quantity | Symbol | What it is | What it is NOT |
|---|---|---|---|
| Critic source-sensitivity | `g_j` | Per-agent scalar, gradient-based | Not a pairwise matrix; no target dimension |
| Module concentration | `Γ(P, g)` | Shannon entropy of module-mass shares | Not Ψ; does not test pairwise dependency retention |

Recommended output path: `analysis/outputs/model_dependency/l2_critic_diagnostic/` — kept **structurally separate** from `analysis/outputs/model_dependency/psi/` so the two are never confused in file listings or downstream scripts. Extend the existing `analysis/outputs/model_dependency/README.md` (already distinguishes headline-valid vs. diagnostic-only D_G) to state explicitly that files under `l2_critic_diagnostic/` are never inputs to a "Ψ" computation.

---

## 3. Formal definitions

### 3.1 Source-sensitivity vector (per checkpoint, computed once, partition-independent)

```
g_j = Σ_k |∂V/∂X_{j,k}|      for each agent j = 1..N
```

where `V` is the global critic's scalar output (any of the `N` identical output rows — they are provably identical given the shared input, so row choice doesn't matter; consider asserting this equality in code as a sanity check, see §7), and `X_{j,k}` is feature `k` of agent `j`'s observation block within the global concatenation. This is the same aggregated-absolute-Jacobian construction as `lrd2025`'s influence framework and the existing D^G instrument (Eq. djac) — grounded more generally in gradient-based saliency (Simonyan et al. 2013; Sundararajan et al. 2017), just applied with the target dimension collapsed since the critic provides none.

### 3.2 Module concentration (per partition, reuses the same fixed `g`)

```
p_k(P) = Σ_{j∈M_k} g_j  /  Σ_j g_j          (module k's share of total sensitivity mass, partition P)
Γ(P, g) = − Σ_k p_k(P) · log p_k(P)          (Shannon entropy over modules, base-e or base-2, be consistent)
```

Lower `Γ` = sensitivity mass concentrated in fewer modules. Higher `Γ` = spread evenly across modules (max value `log K` for `K` equal-mass modules). Compute `Γ(P_flow, g)` and `Γ(P_metis, g)` on the **same fixed `g`** — g does not depend on partition choice, only which module each agent falls into does.

### 3.3 Optional bonus (cheap, partition-independent, parallels existing ρ(W,D_MI)/ρ(W,D_G) checks)

```
ρ(w, g) = Spearman correlation between per-agent total OD flow volume w_j and g_j
```

No partition needed — a third scale-comparable correlation check alongside the two already computed.

---

## 4. Data requirements — checkpoints (checked via WandB, 2026-07-02)

| Network | Run | Status |
|---|---|---|
| Ingolstadt21 | `ing21_mappo_original_global_gpu0_wandb` | Confirmed: `critic_scope: global`, `reward_scope: global_mean`, `save_model: True`, finished (created 2026-06-23). **Ready to use.** |
| Cologne8 | `cologne8+mappo+20260611_130731` | `save_model: True`, finished (2026-06-11), `management` populated. **`critic_scope` not explicit in logged config — confirm this is the global-critic baseline before using it** (check the actual run config/checkpoint, not just WandB's logged subset — some keys may not be logged if left at default). |

No new training required for either network if the Cologne8 confirmation checks out.

---

## 5. Computation procedure

1. Load the global MAPPO checkpoint (see §4). Confirm `critic_scope == "global"` from the actual saved config, not just inference from the run name.
2. Run a forward pass through the critic with the standard global `critic_obs` construction (`CentralizedInputBuilder`, same as training).
3. Sanity check (see §7): assert all `N` output rows of `V` are numerically identical (within floating-point tolerance). If they are not, the "identical global input per row" premise is wrong for this checkpoint and this whole design needs revisiting before proceeding.
4. Take gradients of the (single, deduplicated) scalar `V` w.r.t. each agent `j`'s observation block; aggregate absolute values per §3.1 to get `g_j` for `j = 1..N`. This is a one-time computation per checkpoint, independent of partition.
5. For each partition `P ∈ {P_flow, P_metis}` at each `k` already used elsewhere in the analysis (same `k` values as the D^MI/Φ tables, for direct comparability): compute `Γ(P, g)` per §3.2.
6. Optionally compute `ρ(w, g)` per §3.3 once per network (partition-independent).
7. Write outputs to `analysis/outputs/model_dependency/l2_critic_diagnostic/<network>_mappo_<checkpoint_tag>/`, holding: raw `g` vector, per-partition `Γ` values, and `ρ(w,g)` if computed. Do **not** write to or alongside the `psi/` folder.

---

## 6. Reporting — headline table and Item 4 (Ψ-predicts-performance) rule

Use this table structure (from the design-review discussion, 2026-07-02):

```
Network  Level  k  Partition  Performance  Φ(P,W)  Ψ(P,D_MI)  Γ(P,g)         Ψ(P,D_G)
I21      L1     4  Flow       ...          ...     ...        n/a            n/a
I21      L1     4  METIS      ...          ...     ...        n/a            n/a
I21      L2     4  Flow       ...          ...     ...        Γ_flow         n/a
I21      L2     4  METIS      ...          ...     ...        Γ_metis        n/a
I21      L3     4  Flow       ...          ...     ...        n/a            Ψ_flow
I21      L3     4  METIS      ...          ...     ...        n/a            Ψ_metis
```

Φ(P,W) and Ψ(P,D_MI) are **not** n/a outside L1 — both are model-free and level-agnostic, already computed at matching k for both networks; include them in every row as common baseline columns. Only the level-*specific* instrument (Γ for L2, Ψ(D_G) for L3) is restricted.

**Hard rule for Tier 1 #4 (Ψ-predicts-performance scatter):** do not pool ΔΓ into the same scatter/regression as ΔΨ(D_MI)/ΔΨ(D_G). Γ is not Ψ (§2) — plotting it on the same axis implies a comparability that doesn't exist. Report L1+L3's ΔΨ-vs-Δperformance as the primary scatter (both are true Ψ, same definition and range), and L2's ΔΓ-vs-Δperformance as its own clearly-labeled secondary panel.

---

## 7. Test plan additions

- Unit test: assert the `N` critic output rows are identical under `critic_scope == "global"` (the premise this whole design rests on). If a future code change breaks this assumption, this test should fail loudly before any downstream Γ number is trusted.
- Unit test: `Γ` formula correctness — all mass in one module → `Γ = 0`; mass split evenly across `K` modules → `Γ = log K`.
- Smoke test: run the full pipeline (§5) on Cologne8 first (cheap) before Ingolstadt21, consistent with the project's established "validate on the cheap network first" practice this session.

---

## 8. Known limitations to carry into the manuscript text later

- **Gradient saturation / sensitivity axiom.** Vanilla input-gradient attribution (what `g_j` and the existing D^G both are) can understate a feature's true influence if the function has saturated at the evaluation point — this is the core motivation behind Integrated Gradients (Sundararajan et al. 2017). Applies to the whole Jacobian-based instrument family already in the paper, not just this new addition; worth one shared Limitations sentence rather than a Γ-specific caveat.
- **Concentration ≠ functional importance.** Entropy/attention-concentration diagnostics do not reliably predict which agents are *causally* important (Jain & Wallace 2019, "Attention is not Explanation" — **citation not yet re-verified this session, confirm author/venue before adding to `refs.bib`**). Frame Γ as "does the partition concentrate sensitivity mass," not "does the partition concentrate what matters."

---

## 9. Citations for the eventual manuscript write-up

Added to `refs.bib` (2026-07-02), verified via search this session:
- `simonyan2013saliency` — Simonyan, Vedaldi & Zisserman (2013), foundational gradient-saliency grounding for `g_j`.
- `sundararajan2017axiomatic` — Sundararajan, Taly & Yan (2017), ICML — axiomatic grounding + the saturation caveat (§8).
- `yu2023lowentropymarl` — Yu, Qiu, Wang, Zhang & Wang (2023), arXiv:2302.05055 — direct MARL-communication-entropy precedent for using entropy as a concentration diagnostic in this exact subfield.

**Not yet added, needs verification pass:**
- Jain & Wallace (2019), "Attention is not Explanation," NAACL — the concentration-≠-importance caveat (§8). High-confidence recall, not independently re-verified via search this session.

**Considered and not adopted (Option B, HHI/participation-ratio):** kept here for the record in case the entropy formulation runs into problems downstream. `Γ_HHI(P,g) = Σ_k p_k(P)²` — mathematically the same statistic as the physics "participation ratio," with a direct network-community-detection precedent (HHI computed on a per-node distribution across Louvain-detected communities, arXiv:2309.14232). Not currently cited in `refs.bib` since Option A was selected; add if the design changes.
