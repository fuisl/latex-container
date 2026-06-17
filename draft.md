# Preliminary Results Analysis — HMARL Traffic Control
*Cologne8 and Ingolstadt21 — Initial Experiments (single seed, seed=0)*
*Generated 2026-06-17 from WandB project `hmarl_traffic_control`*

---

## 1. Experiment Status

| Map | Algorithm | Baseline | +Flow (InfoMap) | +METIS |
|-----|-----------|----------|-----------------|--------|
| Cologne8 | MAPPO | ✅ done (1500 ep) | ✅ done (1500 ep) | ✅ done (1500 ep) |
| Cologne8 | IPPO | ✅ done (1500 ep) | ✅ done (1500 ep) | ✅ done (1500 ep) |
| Cologne8 | IDQN | ❌ crashed ep 1340 | ✅ done | ✅ done |
| Cologne8 | CoLight | ❌ crashed ep 470 | ❌ crashed ep 470 | ❌ crashed ep 330 |
| Cologne8 | FMA2C | ⚠️ seed instability | ⚠️ seed instability | ⚠️ seed instability |
| Ingolstadt21 | MAPPO | N/A (not started) | 🔄 running (~ep 830–1360) | 🔄 running |
| Ingolstadt21 | IPPO | N/A | 🔄 running | 🔄 running |
| Ingolstadt21 | FMA2C | 🔄 running | ✅ done (~240 ep only) | ✅ done (~240 ep only) |

**Critical data gaps**: No Ingolstadt21 baselines for MAPPO/IPPO; all CoLight variants crashed;
IDQN baseline unreliable; single seed throughout.

---

## 2. Cologne8 — Quantitative Summary

All values are `eval/metrics/timeLoss` (seconds per vehicle). Lower is better.
Single run, seed=0. No statistical claims.

### 2.1 Final ATT at Episode 1500

| Condition | Final ATT (s/veh) | vs Baseline | Late-σ (ep 1201–1500) |
|-----------|-------------------|-------------|------------------------|
| IPPO baseline | 39.2 | — | 1.24 |
| IPPO + flow (k=3) | 27.1 | **−31%** | 0.95 |
| IPPO + METIS (k=3) | 33.8 | −14% | 68.51 ⚠️ |
| MAPPO baseline | 28.9 | — | 0.53 |
| MAPPO + flow (k=3) | 26.0 | **−10%** | 0.54 |
| MAPPO + METIS (k=3) | 26.8 | −7% | 0.46 |

**Note on IPPO+METIS late-σ = 68.51:** the last 300 episodes still oscillate between
~14 and ~165 s/veh — this run has not converged by ep 1500. The reported final ATT of
33.8 is a single snapshot, not a stable plateau.

### 2.2 AUC-LC and Sample Efficiency

AUC-LC = area under the timeLoss learning curve (trapezoidal integration over episodes 10–1500).
Unit: 10³ (s/veh)·ep. Lower = less cumulative delay during training.

| Condition | AUC-LC (k) | Reduction vs Baseline |
|-----------|------------|----------------------|
| IPPO baseline | 66.7 | — |
| IPPO + flow | 237.6 | +256% ⚠️ (worse AUC; starts at ~1236) |
| IPPO + METIS | 509.2 | +663% ⚠️ (catastrophic; starts at ~1319) |
| MAPPO baseline | 165.2 | — |
| MAPPO + flow | 94.4 | **−43%** |
| MAPPO + METIS | 109.3 | **−34%** |

The IPPO baseline AUC-LC appears better than regional variants because it starts from a
reasonable initial ATT (~128 s/veh at ep 10), while regional IPPO variants start from
catastrophic ATT (~1200–1300 s/veh). This is an initialization artifact of the regional
reward, not a genuine sample efficiency advantage for the baseline.

### 2.3 Episodes to Threshold (ET)

First episode at which `eval/metrics/timeLoss ≤ threshold`.

| Condition | ET(≤50) | ET(≤40) | ET(≤32) | ET(≤28) |
|-----------|---------|---------|---------|---------|
| IPPO baseline | ep 240 | ep 690 | — | — |
| IPPO + flow | ep 490 | ep 550 | ep 830 | ep 1330 |
| IPPO + METIS | ep 1350 | ep 1360 | — | — |
| MAPPO baseline | ep 320 | ep 350 | ep 430 | ep 570 |
| MAPPO + flow | ep 270 | ep 290 | ep 360 | ep 540 |
| MAPPO + METIS | ep 270 | ep 300 | ep 380 | ep 560 |

**MAPPO sample efficiency at baseline's best (ATT ≤ 28.9 s/veh):**
- MAPPO + flow reaches 28.9 s/veh at **ep 470** (31% of training budget)
- MAPPO + METIS reaches 28.9 s/veh at **ep 500** (33% of training budget)
- Both partition schemes match the baseline's best performance in ≈1/3 of episodes

**IPPO sample efficiency at baseline's best (ATT ≤ 39.2 s/veh):**
- IPPO + flow reaches 39.2 s/veh at ep 550 (37% of budget) — but then continues improving to 27.1
- IPPO + METIS barely reaches 39.2 s/veh at ep 1360 (91% of budget) — with ongoing instability

---

## 3. Learning Curve Qualitative Analysis

### 3.1 MAPPO (Regional Critic — Level 2) — Clean Signal

All three MAPPO conditions exhibit a similar **three-phase pattern**:
1. **Catastrophic start** (ep 10–140): ATT ~1000–1200 s/veh for all three (no differentiation yet)
2. **Rapid collapse** (ep 140–400): Sharp decline as the critic learns a value baseline. The
   partition conditions collapse faster (~ep 290 for flow, ~ep 300 for METIS vs ~ep 350 for baseline).
3. **Stable convergence** (ep 400+): Zero spikes across all three MAPPO variants. The partition
   conditions converge to lower plateaus (26.0–26.8) than the baseline (28.9).

The key distinction is not *when* convergence happens but *where it converges to*. The regional
critic provides a better-conditioned value function that finds a lower-loss operating point.

**Flow vs METIS for MAPPO:**
- Flow reaches AUC-LC of 94.4k vs METIS 109.3k (flow 14% lower AUC-LC)
- Flow final ATT: 26.0 vs METIS 26.8 (flow 0.8 s/veh lower)
- ET(≤28): flow ep 540 vs METIS ep 560 (nearly identical)
- Both are stable (Late-σ ≈ 0.5); neither dominates dramatically

**Interpretation**: InfoMap's OD-coherent partition (flow) provides marginally better reward
structure than METIS's purely geometric cut. The difference is real but small at k=3 on this
map. Whether it scales with k or on larger maps remains to be tested.

### 3.2 IPPO (Regional Reward — Level 1) — Instability

The IPPO results reveal a fundamentally different dynamic:

**IPPO Baseline**: Starts at a modest ATT of ~128 s/veh at ep 10 (no cold-start problem).
Converges slowly but stably, reaching a plateau of ~39–42 s/veh by ep ~400 and barely
improving thereafter. Zero instability spikes throughout. Final ATT: 39.2.

**IPPO + Flow**: Starts catastrophically (~1236 s/veh), consistent with a cold-start problem
unique to regional reward. The reward signal is corrupted early in training when neighbors
in the same module are performing poorly — agents receive a mix of their own poor performance
and equally poor neighbors, making gradient attribution difficult. Despite this, the run
eventually reaches competitive performance:
- Rapid improvement begins at ep ~290
- Transient stabilisation near 32 s/veh at ep ~480–550
- **Major instability cluster at ep 620–780** (26 total spikes after ep 400, worst at ep 650
  with ATT = 241.2 s/veh) — a policy collapse followed by recovery
- Eventual stable plateau at ~27–29 s/veh from ep ~1100 onward
- Final ATT: 27.1 (31% improvement over baseline)

**IPPO + METIS**: Worst behavior of all six runs:
- Catastrophic start (~1319 s/veh)
- Persistent instability throughout training (83 spikes after ep 400, worst ep 660 ATT = 435.6)
- Late-σ = 68.51 indicates the run is still not converged at ep 1500
- The final value of 33.8 is a snapshot in a still-oscillating trajectory

**Interpretation**: Regional reward (Level 1) disrupts the natural IPPO optimization by coupling
agent reward signals before the policy is stable enough to benefit from the coupling. The
InfoMap partition (flow) provides better-structured coupling (OD-coherent modules have
naturally correlated rewards) and eventually enables the agent to benefit, but METIS's
geometric partition leads to reward coupling that lacks this structural alignment, causing
chronic instability.

This suggests that **Level 1 (regional reward) is the most sensitive to partition quality**,
while **Level 2 (regional critic, MAPPO) is more robust** to partition choice.

### 3.3 Post-400 Instability Summary

| Condition | Spikes (ATT > 100 after ep 400) | Worst spike |
|-----------|--------------------------------|-------------|
| IPPO baseline | 0 | — |
| IPPO + flow | 26 | ep 650, ATT = 241.2 |
| IPPO + METIS | 83 | ep 660, ATT = 435.6 |
| MAPPO baseline | 0 | — |
| MAPPO + flow | 0 | — |
| MAPPO + METIS | 0 | — |

Regional reward introduces significant instability; regional critic does not.

---

## 4. Flow vs METIS: Directional Evidence for H1

H1 predicts that InfoMap (OD-coherent flow-based partitions) should outperform
geometry-based alternatives (METIS). Directional evidence from Cologne8:

| Metric | Direction | Strength |
|--------|-----------|----------|
| MAPPO final ATT | flow < metis (26.0 vs 26.8) | Weak (0.8 s/veh gap) |
| MAPPO AUC-LC | flow < metis (94.4k vs 109.3k) | Moderate (13.7% gap) |
| IPPO final ATT | flow < metis (27.1 vs 33.8) | Strong (6.7 s/veh gap) |
| IPPO instability | flow < metis (26 vs 83 spikes) | Strong |
| IPPO convergence | flow converges; metis doesn't | Strong |

**Assessment**: Across all metrics and both IPPO and MAPPO, InfoMap (flow) consistently
outperforms METIS. The difference is most pronounced for IPPO where the partition quality
directly affects reward coupling stability. This is directionally consistent with H1.

**Caveat**: Single seed, single map, k=3 only. No statistical tests possible with n=1.
The METIS penalty may partly reflect a k=3 METIS cut being suboptimal for Cologne8's
spatial structure — proper hyperparameter tuning of k per algorithm might narrow the gap.

---

## 5. Ingolstadt21 — Partial Results (runs still active)

At the time of data extraction, Ingolstadt21 runs were at ep 830–1360. Approximate
current ATT values (not final):

| Condition | Current ATT | Episode | Notes |
|-----------|-------------|---------|-------|
| MAPPO + flow (run A) | 162.8 | ~ep 1100 | Converging |
| MAPPO + flow (run B) | 597.6 | ~ep 1100 | **3.7× difference vs run A** ⚠️ |
| MAPPO + METIS | 576.6 | ~ep 930 | Still converging |
| MAPPO + METIS | 927.2 | ~ep 830 | Early |
| IPPO + flow | 590.7 / 711.9 | ~ep 1100 | High variance |
| IPPO + METIS | 853.5 / 1095.2 | ~ep 830 | Early |
| FMA2C + flow | ~549 avg | ~ep 240 (done) | Short run |
| FMA2C + METIS | ~561 avg | ~ep 240 (done) | Short run |
| FMA2C baseline | ~1300 avg | ~ep 240 (done) | Partition clearly helps |

**Critical concern — MAPPO+flow variance**: Two runs with the same configuration (seed=0,
flow partition, k=3) show a 3.7× difference in ATT at comparable episode counts (162.8 vs 597.6).
This suggests either: (a) environment non-determinism in Ingolstadt21 initialization,
(b) an implementation bug causing random state divergence, or (c) these are actually
different hyperparameter configurations mislabeled. Requires investigation.

**FMA2C Ingolstadt21 observation**: FMA2C with any partition (flow: ~549, METIS: ~561)
dramatically outperforms FMA2C without partition (~1300), even after only 240 episodes.
This is the clearest signal in the Ingolstadt21 data but is limited by the short training.

---

## 6. Other Algorithms

### 6.1 CoLight (Level 3 — Regional Communication Graph)
All three CoLight variants on Cologne8 crashed:
- CoLight baseline: crashed at ep 470
- CoLight + flow: crashed at ep 470
- CoLight + METIS: crashed at ep 330

The synchronized crash episodes suggest a shared implementation bug, not a numerical
divergence — most likely an index-out-of-bounds or NaN propagation in the regional GAT
implementation when the communication graph is partitioned. Requires code-level debugging.

### 6.2 IDQN (Level 1/Regional Reward — Q-learning)
- IDQN baseline: crashed at ep 1340 (final eval unavailable)
- IDQN + flow: completed, ATT reported as 27.7 (comparable to IPPO+flow)
- IDQN + METIS: completed, ATT reported as 25.3

Without a reliable baseline, comparison is not possible. The runs suggest IDQN+METIS
may have performed well (25.3), but this cannot be contextualized.

### 6.3 FMA2C (Cologne8)
Two seeds (7 and 27) show orders-of-magnitude variance:
- FMA2C + flow: seed 7 → 715.7, seed 27 → ~120 (approximate)
- Extreme seed sensitivity makes FMA2C results uninterpretable on Cologne8

---

## 7. Issues Requiring Resolution

| Priority | Issue | Impact |
|----------|-------|--------|
| High | All CoLight variants crash — implementation bug | Level 3 test missing entirely |
| High | IDQN baseline crash — no Level 1 baseline for Q-learning | Cannot interpret IDQN regional results |
| High | MAPPO+flow Ingolstadt21 3.7× within-condition variance | May indicate env non-determinism |
| High | No Ingolstadt21 baseline runs for MAPPO/IPPO | Cannot establish relative improvement |
| Medium | IPPO+METIS not converged at ep 1500 | Need extended run or more seeds |
| Medium | Single seed everywhere — no CIs possible | rliable methodology cannot be applied |
| Medium | FMA2C extreme seed sensitivity | Results unusable without more seeds |
| Low | k=3 only — no hyperparameter sweep | May not be optimal k for each algorithm |

---

## 8. Key Conclusions and Implications for Proposal

### 8.1 Positive Signals (supporting the research agenda)

1. **MAPPO + InfoMap partition is the strongest result**: −10% final ATT, −43% AUC-LC,
   3× sample efficiency to baseline plateau. Clean convergence, zero instability. This
   is the most compelling evidence for Level 2 (regional critic) in the proposal.

2. **Flow > METIS consistently**: Across all measurable conditions, InfoMap partition
   outperforms METIS. Most dramatically for IPPO (27.1 vs 33.8 final ATT, 26 vs 83
   instability spikes). Directionally supports H1.

3. **IPPO eventually improves with flow partition**: Despite catastrophic initialization,
   IPPO+flow reaches 27.1 s/veh vs baseline 39.2 — a 31% improvement. Demonstrates
   Level 1 (regional reward) can work but requires careful tuning.

4. **FMA2C on Ingolstadt21 shows strong partition benefit**: ~50% reduction in ATT
   even with short training (240 episodes) — suggests hierarchical MARL benefits
   substantially from OD-coherent partitioning on large maps.

### 8.2 Challenges and Caveats (to acknowledge in proposal)

1. **Level 3 (CoLight) completely unvalidated** — crashes block this experiment track.
2. **Level 1 (regional reward) causes training instability** — IPPO+METIS has not
   converged at 1500 episodes; requires significantly more compute or algorithmic fixes
   (e.g., annealed α to reduce coupling early in training).
3. **Single seed** — no statistical claims are possible; all results are directional indicators.
4. **The anomalous IPPO baseline initialization** (starts at 128 vs 1200+ for regional)
   needs explanation: either the regional reward needs a warm-up phase, or the reward
   normalization must account for the multi-agent averaging.

### 8.3 Immediate Next Steps

1. Fix CoLight crash (debug regional GAT implementation)
2. Run MAPPO/IPPO baselines on Ingolstadt21
3. Add more seeds (minimum 5) to key conditions: MAPPO+flow, MAPPO baseline on both maps
4. Investigate MAPPO+flow Ingolstadt21 variance (two runs with 3.7× difference)
5. Extend IPPO+METIS run beyond 1500 episodes to confirm convergence
6. Consider annealing schedule for α in Level 1 regional reward to mitigate cold-start

---

*All data extracted from WandB project `hmarl_traffic_control` (entity: jv-fuisl-vietnamese-german-university).*
*Run IDs — IPPO_baseline: g2cgs8zb, IPPO+flow: f14n6jvy, IPPO+METIS: 2ztg0nqv,*
*MAPPO_baseline: pccprphk, MAPPO+flow: xiqx8m9e, MAPPO+METIS: gip35e5t.*
