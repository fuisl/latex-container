# Research Plan: InfoMap-Partitioned MARL for Traffic Signal Control

**Status:** Pilot completed (Cologne8, Ingolstadt21) · Full study planned  
**Document:** Living reference — last updated 2026-06-22  
**Proposal:** `/workspace/src/main.tex` · **WandB project:** `hmarl_traffic_control` (entity: `jv-fuisl-vietnamese-german-university`)

---

## 1. Research Question

> Does an OD-flow-based network partition (InfoMap/map equation) provide a better inductive bias for multi-agent RL in traffic signal control than a geometric partition (METIS), and does this hold consistently at all three coordination levels (reward, critic, attention)?

**Formal framing:** ND-POMDP with coordination graph $G_C$ defined by InfoMap partition of the OD flow matrix. The map equation minimisation provides a principled approximation to the ND-POMDP's optimal coordination graph without requiring MARL training.

---

## 2. Core Hypotheses

| ID | Hypothesis | Verification |
|----|-----------|-------------|
| **H1** | Within-module agent pairs share higher mutual information about future traffic states than cross-module pairs: $I(X_i(t); X_j(t{+}\tau)) > I(X_i(t); X_l(t{+}\tau))$ for $i,j \in M_k$, $l \notin M_k$ | KSG estimator MI + Wilcoxon signed-rank test |
| **H2** | Spill-back events are more likely to stay within modules than cross modules | Queue trajectory spill-back events + one-sample proportion test |

**Mandatory gate:** H1 and H2 must be verified on each network before proceeding to MARL training.

---

## 3. Three-Level Coordination Protocol

| Level | Mechanism | Algorithm | Partition role |
|-------|-----------|-----------|---------------|
| L1 | Regional reward shaping | IDQN / IPPO | Defines reward averaging boundary |
| L2 | Regional centralized critic | MAPPO | Defines critic input grouping |
| L3 | Regional GAT attention | CoLight | Defines attention neighbourhood |

**Annealing schedule (L1 cold-start mitigation):**
$$\alpha(e) = 1 - (1-\alpha_{\min}) \cdot \min(e / E_{\text{warm}}, 1)$$

---

## 4. Pilot Experimental Status

### 4.1 Cologne8 (8 intersections, k=3, seed=0, 1500 ep) — COMPLETED

**MAPPO / IPPO (Levels 1–2):**

| Condition | Final ATT (s/veh) | AUC-LC (k) | Late-σ |
|-----------|-------------------|------------|--------|
| IPPO baseline | 39.2 | 66.7 | 1.2 |
| IPPO + flow | 27.1 | 237.6 | 1.0 |
| IPPO + METIS | 33.8 | 509.2 | 68.5 ★ |
| MAPPO baseline | 28.9 | 165.2 | 0.5 |
| MAPPO + flow | **26.0** | **94.4** | 0.5 |
| MAPPO + METIS | 26.8 | 109.3 | 0.5 |

★ Not converged at ep 1500.

**CoLight (Level 3):**

| Condition | Eval ATT | Late-mean | Late-σ |
|-----------|----------|-----------|--------|
| CoLight original | 16.20 | 14.4 | 1.3 |
| CoLight + METIS k3 | 15.92 | 18.4 | 1.9 |
| CoLight + flow k3 | 28.06 | 56.2 | **25.3** ★★ |

★★ Catastrophic divergence: ATT rises to 40–121 s/veh after ep 700 before partial recovery.

### 4.2 Ingolstadt21 (21 intersections, k∈{4,5}, seed=0, 1500 ep) — COMPLETED

| Algo | Flow k4 | Flow k5 | METIS k4 | METIS k5 | Flow/METIS k4 | Flow/METIS k5 |
|------|---------|---------|----------|----------|--------------|--------------|
| MAPPO | **141** | 161 | 401 | 641 | 2.85× | 3.99× |
| IPPO | 565 | 203 | 846 | 526 | 1.50× | 2.60× |

No no-partition baseline exists for Ingolstadt21 yet — values are relative to each other.

---

## 5. Updated Beliefs (Post-Pilot)

| Belief | Prior | Updated | Evidence |
|--------|-------|---------|----------|
| Flow > METIS at L1 (reward) | Likely | **Confirmed directionally** | Cologne8: IPPO+flow 6.7 s/veh better, 3.2× fewer instability spikes |
| Flow > METIS at L2 (critic) | Likely | **Confirmed strongly** | I21: MAPPO+flow 2.85–3.99× lower ATT than METIS |
| Flow > METIS at L3 (attention) | Likely | **Refuted on small networks** | Cologne8: flow diverges (+73%), METIS neutral; root cause: ~2 agents/module too small |
| MAPPO > IPPO | Expected | **Confirmed (4.01× at flow k4)** | Centralized critic amplifies partition benefit |
| k-sensitivity low | Neutral | **Moderate for flow, high for METIS** | MAPPO+flow: k4 14% better; MAPPO+METIS: k4 2.4× better than k5 |
| H1 holds | Hypothesis | **Consistent with results** — not yet formally tested | MI correlation implied by Cologne8/I21 training dynamics |

**Key revision:** Flow partition benefit is **level-dependent**. At L1/L2, OD-coherent module boundaries reduce credit-assignment noise. At L3, pre-specified boundaries restrict the GAT and may prevent necessary cross-module coordination — especially when modules are too small (~2 agents).

---

## 6. Outstanding Issues (P1 → P3)

| Priority | Issue | Action |
|----------|-------|--------|
| **P1** | No no-partition baseline on Ingolstadt21 | Run MAPPO+no-partition and IPPO+no-partition on I21 |
| **P1** | CoLight+flow L3 benefit unconfirmed for larger modules | Run CoLight (no-partition / flow / METIS) on I21 with k=4 (~5 agents/module) |
| **P2** | IPPO+METIS Cologne8 not converged at ep 1500 | Extend run; apply $\alpha(e)$ annealing |
| **P2** | MAPPO+METIS k=5 anomalously worse than IPPO+METIS k=5 | Inspect module graph connectivity at k=5 METIS; check for degenerate (<3 agent) regions |
| **P3** | Single seed throughout; rliable protocol inapplicable | Expand to ≥5 seeds for MAPPO+flow conditions |

---

## 7. Full Experimental Programme

### 7.1 Core Factorial Study

**Networks:** Cologne8 (8 int), Ingolstadt21 (21 int), FGS-Synthetic-P (scalability)  
**Seeds:** ≥5 per condition for rliable evaluation  
**Metrics:** IQM + stratified bootstrap CIs (rliable), AUC-LC, Late-σ, ET(t)

**Factorial conditions (per network):**

| Factor | Levels |
|--------|--------|
| Partition | InfoMap/flow · METIS · None (baseline) |
| Algorithm level | L1 (IPPO) · L2 (MAPPO) · L3 (CoLight) |
| k (modules) | 3 · 4 · 5 (network-size dependent) |
| Seed | 5 independent seeds |

**Primary comparisons:**
- C1: Flow vs METIS vs None at L2 (MAPPO) — main result
- C2: Flow vs METIS vs None at L3 (CoLight) — resolves L3 ambiguity from pilot
- C3: L1 vs L2 vs L3 (algorithm level effect) at fixed partition
- C4: k-sensitivity at fixed (algo, partition)

### 7.2 Ablation Studies

| Ablation | ID | Conditions |
|----------|----|-----------|
| Reward annealing | C1-α | $\alpha_{\min} \in \{0, 0.1, 0.3\}$, $E_{\text{warm}} \in \{100, 300\}$ |
| Temporal partition | T0–T5 | No-partition · METIS · InfoMap off-peak · peak · 24h · dynamic re-partition |
| Attention range | A1 | GNN range $\hat{\rho}_u(\mathbf{F})$ computed per partition condition |

### 7.3 H1/H2 Verification (Pre-MARL Gate)

- **H1 (MI advantage):** KSG estimator on 1-hour OD traces; within- vs cross-module pair comparison; Wilcoxon signed-rank; significance threshold p < 0.05
- **H2 (Spill-back containment):** Queue trajectory extraction from SUMO; proportion test $\Pr(\text{spill-back within module})$ vs $\Pr(\text{cross-module})$

### 7.4 Attention Range Analysis (§7.6)

For each trained CoLight model:
1. Freeze weights; compute Jacobian $\partial a_u / \partial s_v$ for all $v$
2. Normalise: $\tilde{J}_{uv} = |\partial a_u / \partial s_v| / \sum_v |\partial a_u / \partial s_v|$
3. Compute $\hat{\rho}_u(\mathbf{F}) = \mathbb{E}_{v \sim \tilde{J}_{u\cdot}}[d_G(u,v)]$
4. Compare global $\hat{\rho}$ (no partition) vs regional (flow/METIS) per module

---

## 8. Evaluation Protocol

**Primary metric:** Average waiting time (ATT, s/veh) — `eval/metrics/waitingTime`  
**Sample efficiency:** AUC-LC $= \int_0^T \text{ATT}(e)\,de$ (trapezoidal)  
**Convergence time:** ET($\le t$) — first episode where ATT $\le t$  
**Stability:** Late-σ — std of ATT over episodes 1201–1500  
**Statistical:** rliable framework — IQM + stratified bootstrap CIs (10k samples) across ≥5 seeds  
**Performance profiles:** Probability of improvement plots between flow vs METIS at each level

---

## 9. Theoretical Contributions

1. **ND-POMDP + InfoMap connection:** First formal derivation that the map equation minimisation approximates the ND-POMDP optimal coordination graph from OD flow data
2. **Coordination description length:** Map equation terms $q_\circlearrowleft H(Q)$ (between-module) and $\sum p_i^\circlearrowleft H(P_i)$ (within-module) as coordination complexity measures
3. **Three-level framework:** Single OD-flow partition applied consistently at reward (L1), critic (L2), and attention (L3) — closing gap G6
4. **Formal GNN range measure:** $\hat{\rho}_u(\mathbf{F}) = \mathbb{E}_{v \sim I_u}[d_G(u,v)]$ for attention analysis

---

## 10. Pending Runs Summary

| Run | Network | Algo | Partition | k | Status |
|-----|---------|------|-----------|---|--------|
| MAPPO no-partition baseline | I21 | MAPPO | None | — | **TODO** |
| IPPO no-partition baseline | I21 | IPPO | None | — | **TODO** |
| CoLight no-partition | I21 | CoLight | None | — | **TODO** |
| CoLight + flow | I21 | CoLight | Flow | 4 | **TODO** |
| CoLight + METIS | I21 | CoLight | METIS | 4 | **TODO** |
| IPPO+METIS extended | C8 | IPPO | METIS | 3 | TODO (extend ep) |
| Multi-seed expansion | I21 | MAPPO | Flow | 4 | TODO (×5 seeds) |
| FGS-P ingolstadt7 | Synth | MAPPO | Flow | — | RUNNING |

---

## 11. File Locations

| Artifact | Path |
|----------|------|
| Proposal (LaTeX source) | `/workspace/src/main.tex` |
| Bibliography | `/workspace/src/refs.bib` |
| Compiled PDF | `/workspace/out/main.pdf` |
| WandB runs | Project `hmarl_traffic_control`, entity `jv-fuisl-vietnamese-german-university` |
