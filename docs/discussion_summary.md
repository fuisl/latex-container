# Discussion Chapter — Current State Summary

Source: `src/TeXFiles/070_Results.tex`  
Purpose: audit of what has already been argued, compared, and ablated — use this before revising.

---

## Chapter Structure at a Glance

| Section | Title | Status |
|---------|-------|--------|
| §4.1 | Main Results | Tables written; narrative complete |
| §4.2 | Baseline Comparison | Three subsections written |
| §4.3 | Training Convergence Analysis | Seven paragraphs + 1 figure |
| §4.4 | Ablation Study | Table + 3 figures + 3 paragraphs |
| §4.5 | Design Evolution | Table + TikZ figure + 3 prose blocks |
| §4.6 | Interpretation and Discussion | Three subsections written |
| §4.7 | Answering the Research Questions | SQ1–SQ4 + MRQ answered |
| §4.8 | Limitations | Four paragraphs |

---

## §4.1 Main Results

### What is reported
- **Table 1** (`tab:main_results`): best-validation performance across all six German RESCO scenarios for all baselines and FGS Gen-1 variants.
- Four metrics per scenario: Wait (s), Delay (s), Trip (s), Queue (veh./lane).
- Methods: FixedTime (FT), MaxPressure (MP), DQN, PPO, CoLight, FRAP, FGS_S (MLP+GATv2+SAC), FGS_P (MLP+GATv2+PPO).
- **Table 2** (`tab:fgs_evolution`): FGS architecture progression (FGSv2-SAC, FGSv3-PPO, FGSv3-SAC) on Regional-tier only (cologne8, ingolstadt21).

### Three patterns highlighted in narrative
1. On cologne8 (N=8): PPO best (4.3 s), FGS_S and FGSv3-PPO close behind (4.9 s, 4.8 s). CoLight (11.0 s) and FRAP (13.9 s) substantially worse.
2. On ingolstadt21 (N=21): DQN best non-FGS (33.8 s); FGS_P worse than DQN (88.6 s); FGSv3-PPO best overall (22.9 s) = 74% improvement over FGS_P.
3. FRAP encoder causes catastrophic failure: cologne3 FRAP+GAT+SAC = 460.8 s vs. MLP counterpart = 7.4 s.

### Reporting conventions established
- Best-validation checkpoint (optimistic upper bound).
- `‡` = early-training transient (excluded from Bold), `†` = partial run (17/200 ep.), `*` = training in progress.
- Full ablation in Appendix Tables A1–A4.

---

## §4.2 Baseline Comparison

### §4.2.1 FGS versus CoLight
**Comparisons made:**
- cologne8: FGS_S = 4.9 s vs. CoLight = 11.0 s → **55% reduction**. Three attributed causes: (1) GATv2 additive attention vs. CoLight dot-product; (2) CoLight validated on regular Chinese grids, not German irregular topologies; (3) CoLight lacks phase-aware local encoder.
- ingolstadt21: FGS_P = 88.6 s vs. CoLight = 120.8 s → **27% improvement**. FGSv3-PPO further reduces to 22.9 s → **81% improvement** over CoLight.
- ingolstadt7: CoLight = 17.5 s, worse than DQN, PPO, FRAP, FGS_P. FGS_S not run.

**Conclusion stated:** GATv2 + capable RL consistently outperforms best published graph-based baseline at all tested scales.

### §4.2.2 FGS versus independent DQN and PPO
**Comparisons made:**
- cologne8: DQN = 6.7 s vs. FGS_S = 4.9 s → graph + SAC gives measurable advantage.
- ingolstadt7: FGS_P = 6.8 s; PPO = 5.4 s (best on network); DQN = 9.4 s; FRAP = 9.3 s. FGS_P beats DQN/FRAP but trails standalone PPO.
- ingolstadt21: DQN = 33.8 s, PPO = 40.0 s, FGS_P = 88.6 s → FGS_P **worse** than both. Two explanations: (1) DQN converges faster with fewer params; (2) PPO avoids centralized critic overhead.
- FGSv3-PPO = 22.9 s → outperforms both standalone DQN and PPO.
- cologne3: PPO = 6.0 s, DQN = 8.1 s, FGS_S = 7.4 s. Graph communication no net advantage at N=3.
- IndSAC baseline noted: 5.5 s (cologne3), 4.7 s (cologne8) — entropy bonus itself is strong at small/moderate scale.

### §4.2.3 FGS versus standalone FRAP
**Comparisons made:**
- cologne3: FRAP = 18.6 s vs. FGS_S = 7.4 s.
- cologne8: FRAP = 13.9 s vs. FGS_S = 4.9 s.
- ingolstadt7: FRAP = 9.3 s vs. FGS_P = 6.8 s (27% improvement).
- ingolstadt21: FRAP live best = 120.4 s; FGS_P = 88.6 s, FGSv3-PPO = 22.9 s.
- **Conclusion:** standalone FRAP is not competitive on larger German networks; FRAP encoder within FGS + demand pathway substantially reduces mismatch.

---

## §4.3 Training Convergence Analysis

**Figure:** `training_curves_regional.pdf` (Regional tier only — cologne8 + ingolstadt21)

### Seven training dynamics analyzed (all narrated in text)

| Variant | Scenario | Behavior described |
|---------|----------|--------------------|
| FGS_S (MLP+GATv2+SAC) | cologne8 | High-variance early (ep 1–13: 438–660 s), monotonic improvement from ep 14, stable ~6–7 s from ep 22. Best checkpoint 6.0 s at ep 39. Confirmed converged. |
| FGSv3-PPO | cologne8 | Fastest-converging. Reaches 5.4 s by ep 5, stays 4.8–6.1 s for remainder. Best 4.8 s at ep 39. |
| FGS_S (MLP+GATv2+SAC) | ingolstadt21 | Only 17 episodes completed (OOM). Waiting time 75–185 s, no trend. Final checkpoint = 757.5 s (highly suboptimal). |
| FGS_P (MLP+GATv2+PPO) | ingolstadt21 | All 200 eps. Drops from ~58 s at ep 11, stabilizes 29–34 s (ep 140–200). Periodic spikes (200–340 s) with 2–3 ep recovery. Best 88.6 s. Large train-to-val gap (29 s train vs 88.6 s val). |
| FGSv3-PPO | ingolstadt21 | Best FGS variant. Stable 22–35 s from ep 7. Best 22.9 s at ep 90. Factored critic (204 dims vs 3,091) enables efficient updates. |
| FGSv3-SAC / FGSv2-SAC | ingolstadt21 | Complete training (factored critic). High-variance: FGSv3-SAC best = 11.1 s at ep 3 (transient); stable median ~25.8 s after ep 6. FGSv2-SAC best = 13.9 s at ep 1; stable median ~27.8 s. Marked `‡`. |
| DQN | ingolstadt21 | Starts ~48 s, large spikes, stabilizes 33–50 s by ep 140. Best 33.8 s. Simple per-agent Q-net → all 200 eps used efficiently. |
| FGS (MLP+GAT+PPO) | ingolstadt21 | Markedly worse with original GAT. Frequent severe spikes, oscillates 37–330 s throughout 200 eps. Best 261.2 s vs GATv2 variant 88.6 s. |

**Explanations offered:** SAC deadly triad (off-policy + function approx + bootstrap), replay non-stationarity at N=21, entropy bonus incentivizing cycling.

---

## §4.4 Ablation Study

**Table 3** (`tab:ablation`): 3 components × 2 levels each, tested on cologne8 (N=8) and ingolstadt21 (N=21).

### What was ablated

| Component | Levels compared | Fixed |
|-----------|----------------|-------|
| Encoder (Module I) | MLP vs. FRAP | GATv2 + PPO |
| Graph layer (Module II) | GATv2 vs. GAT | MLP + PPO |
| RL algorithm (Module III) | SAC vs. PPO | MLP + GATv2 |

### Ablation results at a glance

**Cologne Regional (N=8):**

| Encoder | Graph | RL | Wait (s) |
|---------|-------|----|---------:|
| MLP | GATv2 | SAC | **4.93** |
| MLP | GATv2 | PPO | 6.25 |
| MLP | GAT | PPO | 6.72 |
| FRAP | GATv2 | PPO | 6.69 |

**Ingolstadt Regional (N=21):**

| Encoder | Graph | RL | Wait (s) |
|---------|-------|----|---------:|
| MLP | GATv2 | PPO | **88.6** |
| MLP | GAT | PPO | 261.2 |
| FRAP | GATv2 | PPO | 460.7 |
| MLP | GATv2 | SAC | 757.5 `†` |

### Three paragraphs of interpretation written

**Encoder effect:**
- cologne8: FRAP penalty = +7% (6.69 vs 6.25).
- ingolstadt21: FRAP penalty = **+5.2× on Wait, +2.6× on Delay** (460.7 vs 88.6).
- Scaling confirmed: penalty amplifies with N. Attribution: FRAP structural mismatch with German heterogeneous phase counts.

**Graph layer effect:**
- Most striking result: GATv2 → GAT swap on ingolstadt21 inflates Wait from 88.6 → 261.2 s (**+195%, 66% reduction from GATv2**).
- cologne8: only 8% difference (6.25 vs 6.72 s) — small, homogeneous network.
- Attribution: GATv2 dynamic per-edge attention distinguishes structurally similar nodes; GAT cannot.

**RL algorithm effect:**
- cologne8: SAC wins (4.93 s vs PPO 6.25 s, 21% improvement). Attribution: PER replay buffer sample efficiency on moderate networks.
- ingolstadt21: PPO wins (88.6 s) vs SAC terminates after 17 eps (757.5 s). Attribution: centralized critic input ~3,133 dims exceeds GPU memory.
- FGSv3 factored critic fixes this: both SAC and PPO complete at N=21.

**Figures produced:** `ablation_encoder.pdf`, `ablation_graph.pdf`, `ablation_rl.pdf` (training curves for each ablation pair, both scenarios).

---

## §4.5 Design Evolution

**Table 4** (`tab:fgs_generation_summary`): 3-generation comparison (Gen-1, FGSv2, FGS final).
**Table 5** (`tab:fgsv3_vs_fgsv2`): FGS final vs FGSv2 on Regional tier (best-validation checkpoint).
**Figure:** `fig:fgs_framework` — TikZ diagram of Gen-1 / FGSv2 / FGS final architecture.

### What each generation changed and why

**Gen-1 → FGSv2:**
- **Failure identified:** Module-I scalar output discards per-phase competition information before graph aggregation.
- **Fix:** Tap FRAP after movement-embedding step (before scalar projection) → per-phase action tokens `z_{i,a}`. Tokens bypass Module II via skip connection; concatenated with graph context at actor input. GATv2 message = pooled competition score `s_i`.
- **Residual failure:** Centralized critic still OOM at N=21 (failure (2) persisting). Also, `s_i` encodes phase rankings, not demand state.

**FGSv2 → FGS final:**
- **Failure identified:** GATv2 message `s_i` is a competition score (phase rankings), not demand state — suboptimal for anticipating upstream pressure.
- **Fix 1:** Module-II signal replaced with demand embeddings `d_i` from FRAP phase-demand branch (Eq. fgsv3_demand).
- **Fix 2:** Centralized critic replaced with factored neighborhood critic (O(d_c + A_max) independent of N). Input reduced from 3,091 → 204 dims (15× reduction).

### Generation comparison on ingolstadt21 (Table 5)

| Method | Wait (s) | Queue |
|--------|----------:|------:|
| FGSv2-SAC `‡` | 13.9 | 12.90 |
| FGS-PPO | **22.9** | 0.71 |
| FGS-SAC `‡` | 11.1 | 12.41 |
| FGS_P Gen-1 | 88.6 | 2.58 |

Note: FGSv2-SAC and FGS-SAC queue anomalies flagged (`‡`) — see §4.8.

---

## §4.6 Interpretation and Discussion

### §4.6.1 FRAP encoding and German intersection geometry
**Argument:** FRAP constructs phase-pair competition features assuming each phase controls a fixed pair of opposing movements. German RESCO intersections have 2–6 phases with variable movement counts per phase. When a phase controls fewer than two movements, competition weight normalization produces undersaturated features — actor misinterprets as low-demand signal.

**Evidence cited:**
- Catastrophic outcomes: cologne3 FRAP+GATv2+SAC = 460.8 s vs. MLP = 7.4 s.
- But: FRAP+GATv2+PPO on cologne8 = 6.69 s (only 7% above MLP) — GATv2 partially corrects by down-weighting near-zero-output neighbors.
- At ingolstadt21: correction fails (5.2× penalty) — mismatch amplified at N=21.
- FGS final design bypasses this via demand-branch pathway.

### §4.6.2 Graph-based coordination and network scale
**Arguments made:**
- H1 (graph-based comm. provides measurable benefit): **conditionally confirmed** — benefit depends on N and FGS generation.
- GATv2 vs. GAT: 66% improvement on ingolstadt21; only 7% on cologne8.
- FGS_P vs. CoLight on ingolstadt21: 27% improvement; FGSv3-PPO: 81% improvement.
- Key nuance: first-generation FGS_P is **outperformed by DQN and PPO** on ingolstadt21. Train-to-val gap for FGS_P (29 s train, 88.6 s val) >> DQN (38 s train, 33.8 s val). Interpretation: FGS_P develops more demand-specific but less generalizable policy.
- FGSv3-PPO closes this gap: architectural changes improve both sample efficiency and generalization.

### §4.6.3 SAC convergence and network complexity
**Arguments made:**
- SAC sample-efficiency advantage is scenario-dependent: wins on cologne8 (N=8), fails on ingolstadt21 (N=21) with centralized critic.
- Effective threshold lies between N=8 and N=21.
- Centralized critic input: O(Nd + NA_max); PPO value function: O(d) independent of N.
- FGSv3 factored neighborhood critic: O(d_c + A_max) = 204 dims at N=21 (15× reduction from 3,091).
- FGSv3: both SAC and PPO complete at N=21. FGSv3-SAC best-checkpoints (11.1 s, 13.9 s) = early-transient lower bounds. Stable converged region ~25–28 s for SAC variants.

**CTDE paragraph:** Connects to Zhou et al. CADP (2023) — identifies two failure boundaries:
- CADP: standard CTDE not "centralized enough" (mutual independence during training).
- This work: fully centralized critic not "scalable enough" at large N.
- FGSv3 factored critic as navigation between these two boundaries. Two-stage information flow (graph propagation → local critic aggregation) achieves similar effect to CADP's training-time comm. channel, but with constant-dimension input.

---

## §4.7 Research Questions — What Has Been Answered

### SQ1 (Baseline comparison)
**Question:** How do FGS pipeline instantiations compare with classical and deep RL baselines across scale tiers?

**Answer given:**
- cologne8: FGS_S = 4.9 s, trails PPO (4.3 s) by 14%, beats DQN (6.7 s) by 27%, beats CoLight (11.0 s) by 55%, beats FRAP (13.9 s) by 64%. FGSv3-PPO = 4.8 s ≈ PPO.
- cologne3: FGS_S = 7.4 s; CoLight = 6.5 s; PPO = 6.0 s.
- ingolstadt7: FGS_P = 6.8 s, outperforms FRAP (9.3 s) and DQN (9.4 s); PPO = 5.4 s (best); FGS_S not run.
- ingolstadt21: FGS_P = 88.6 s (beats CoLight 120.8 s); FGSv3-PPO = 22.9 s (best on network, outperforms all 7 baselines).
- **Verdict:** FGS competitive/superior at Regional tier; FGSv3-PPO is best-performing method on largest network.

### SQ2 (Design-space analysis)
**Question:** How do encoder choice and graph-attention mechanism affect performance and training stability?

**Answer given:**
- Encoder = dominant determinant: FRAP 5.2–62× worse than MLP across scenarios.
- Graph layer determines generalization gap: GATv2 substantially reduces train-to-val gap vs. GAT on ingolstadt21.
- Interaction asymmetric: GATv2 partially compensates FRAP on cologne8, not at N=21.
- **Verdict:** MLP > FRAP; GATv2 > GAT at Regional scale.

### SQ3 (Scale and topology dependency)
**Question:** How does benefit of each design component vary with network scale and topology?

**Answer given:**
- N=1: graph module = structural no-op (no neighbors); FGSv2-SAC and FGSv3-SAC produce identical metrics to Gen-1 at N=1. Modest improvements over FRAP but trails DQN/PPO on some scenarios.
- N=7 (ingolstadt7): FGS_P beats DQN/FRAP/CoLight but trails standalone PPO — benefit not yet consistent at N=7 across all algorithms.
- N=8 (cologne8): graph lifts FGS_S to best graph-based result; SAC vs. PPO gap = 21%.
- N=21 (ingolstadt21): GATv2 becomes essential (GAT swap = +195% wait); centralized SAC fails; PPO and FGSv3 succeed.
- **Verdict:** Benefit scales with N and topology heterogeneity; negligible at N=1; consistent advantage from N=7 onward; GATv2 essential at N=21.

### SQ4 (Exploratory — emergent coordination)
**Question:** To what extent can learned coordination behavior be interpreted as decentralized self-organization?

**Answer given (tentative):**
- Indirect evidence: isolated spikes followed by rapid 2-episode recovery on ingolstadt21 — consistent with upstream agents adjusting phase plans in response to GATv2-relayed demand signal.
- FGS_P shows recovery from 300 s spike within 2 episodes — too fast for individual agent response.
- **Caveat:** Attention weights not logged → full visualization left to future work. Answer is tentative, causal confirmation requires future attention-weight analysis.

### Main Research Question
**Question:** Can FGS provide competitive and scalable traffic signal control on German road networks, and which design dimensions are primary determinants?

**Answer:**
- Competitive: FGSv3-PPO outperforms all 7 baselines on largest network (22.9 s vs. CoLight 120.8 s, −81%).
- Scalable: 3-generation diagnosis-and-repair trajectory, culminating in factored critic removing O(N) scaling barrier.
- Primary design determinants (in order): (1) encoder type (structural compatibility with German phase geometry), (2) graph-attention mechanism (policy generalization at Regional scale), (3) RL algorithm + critic architecture (convergence within resource budget at large N).

---

## §4.8 Limitations — What Has Been Disclosed

| Limitation | Details stated |
|-----------|----------------|
| Incomplete scenario coverage | DQN/PPO baselines not crossed with all 6 scenarios. Ingolstadt Corridor FGS_S not run. |
| Single seed per run | Results = point estimates without variance bounds. RESCO protocol = 5 seeds. Confidence intervals not reported. |
| SAC instability at N=21 | FGSv3-SAC / FGSv2-SAC best-checkpoints are early-transients (ep 3, ep 1 respectively). Structural causes: deadly triad + replay non-stationarity at N=21. Stable ≈ 25–28 s after ep 6. Extended training (300–500 ep) + entropy-temperature tuning recommended. |
| Queue-wait discrepancy / reward gaming | FGS_P on cologne1/cologne3 and SAC variants on ingolstadt21: near-zero wait with enormous queues (120 veh./lane at ≤5 s wait). Mechanism: differential wait reward drops when vehicles briefly start moving; rapid phase cycling exploits this. SAC more susceptible (entropy bonus + off-policy replay). Marked `‡`; queue omitted; excluded from Bold. Recommendation: replace differential wait with pressure reward (PressLight) in future work. |
| Train-to-validation demand shift | FGS_P train-to-val gap (29 s → 88.6 s) >> DQN (38 s → 33.8 s). FGSv3-PPO reduces this. Multi-seed + domain randomization recommended. |

---

## What Is NOT Yet Discussed (gaps to address in revision)

1. **No quantitative confidence bounds** anywhere. Every number is a point estimate from a single seed. The text acknowledges this but does not attempt even informal uncertainty bracketing (e.g., "stable median ± interquartile range").

2. **No comparison to prior MARL baselines beyond CoLight** — e.g., PressLight, MPLight, AttendLight are not compared. The thesis scope is set (German RESCO only), but the omission is not explicitly justified in terms of why these were excluded.

3. **ingolstadt7 FGS_S result** is explicitly stated as "not run." No rationale is given for why (training budget? same OOM issue as ingolstadt21?). This is a gap in the crossing.

4. **No multi-metric visualization** — all quantitative comparison is single-metric (Wait). Delay, Trip, Queue trends are not narratively tied to the Wait trends (e.g., does CoLight's high wait also map to high queue?).

5. **Emergent coordination (SQ4)** is answered tentatively with "indirect evidence." No attention visualization, no phase-plan analysis, no case study episode. This subsection is currently the weakest in the chapter.

6. **FGSv2 results on Corridor and Single-intersection scenarios** are not reported anywhere — only cologne8 and ingolstadt21 are in Table 2. Whether FGSv2 was run on cologne3 or ingolstadt7 is unclear.

7. **IndSAC baseline** is mentioned in §4.2.2 but not included in Table 1 (only in Appendix). Its result (4.7 s on cologne8) is the best non-FGS result on that scenario and arguably belongs in the main table or at least a dedicated comparison paragraph.
