# Consolidated Results Tables: Flow-Based Partitioning

This document groups the report-ready numerical results in one place. It
keeps replicated R2 results, single-checkpoint diagnostics, and historical
context separate so that their uncertainty is not conflated.

## Reading conventions

- **Retention metrics** \(\Phi\) and \(\Psi\) are bounded fractions. Flow gain
  is reported in **percentage points (pp)**:

  \[
  G_{\mathrm{pp}}=100\left(S_{\mathrm{Flow}}-S_{\mathrm{METIS}}\right).
  \]

- **Lower-is-better control metrics** use:

  \[
  G_{\mathrm{cost}}=
  100\frac{C_{\mathrm{METIS}}-C_{\mathrm{Flow}}}
  {|C_{\mathrm{METIS}}|}.
  \]

- **Higher-is-better reward** uses:

  \[
  G_{\mathrm{reward}}=
  100\frac{R_{\mathrm{Flow}}-R_{\mathrm{METIS}}}
  {|R_{\mathrm{METIS}}|}.
  \]

- Positive gain favors Flow. Negative gain favors METIS.
- Unless stated otherwise, uncertainty is the **sample standard deviation**.
- R2 training values select the minimum evaluation time loss independently
  within each seed, then report the mean and sample SD across seeds. Other
  metrics are taken from that same selected checkpoint.
- “Random” is one reproducible size-balanced partition at partition seed 0;
  it is not an average over partition seeds.

## Headline gain summary

| Evidence level | Replication | Flow over METIS | Short meaning |
|---|---:|---:|---|
| Physical-flow retention \(\Phi\) | 4 matched map/\(k\) blocks | **+15.4 to +32.5 pp** | Flow directly preserves more vehicle movement inside modules. |
| State-MI retention \(\Psi(D^{MI})\) | 3 traffic seeds per block | **+2.7 to +34.4 pp** | The same modules preserve more observed inter-agent state dependency. |
| Learned CoLight retention \(\Psi(D^G)\), coarse \(k\) | 1 global checkpoint per map | **+12.9 to +16.4 pp** | Flow preserves more learned one-hop dependency when modules remain coarse. |
| Centralized MAPPO critic retention \(\Psi(D^Q)\), Cologne8 | 3 global critic seeds | **+14.40 to +35.04 pp** | Flow strongly preserves value-relevant dependency used by centralized critics. |
| R2 best-checkpoint time loss, Cologne8 IPPO | 3 training seeds | **+62.9%** | Large control gain under regional reward sharing. |
| R2 best-checkpoint time loss, Cologne8 MAPPO | 3 training seeds | **+23.7%** | Large control gain under a regional critic. |
| Remaining completed R2 Flow–METIS comparisons | 3 training seeds | **−5.3% to +1.4%** | No reliable practical separation at current replication. |
| Legacy 1,500-episode sweep | 1 training seed | Flow favored in **9/12** comparisons | Broad exploratory evidence, not a multiseed estimate. |

**Highlight.** Flow has its most consistent advantage before training:
physical flow, state dependency, and centralized-critic dependency all favor
Flow. The downstream benefit is mechanism-dependent: it is large for
Cologne8 IPPO and MAPPO and neutral in the other completed R2 comparisons.

---

## 1. Physical-flow retention \(\Phi\)

| Map | \(k\) | Flow \(\Phi\) | METIS \(\Phi\) | Random \(\Phi\) | Flow gain over METIS |
|---|---:|---:|---:|---:|---:|
| Cologne8 | 3 | **0.9394** | 0.6143 | 0.1359 | **+32.51 pp** |
| Cologne8 | 5 | **0.5693** | 0.4155 | 0.2605 | **+15.38 pp** |
| Ingolstadt21 | 4 | **0.8170** | 0.6431 | 0.3417 | **+17.40 pp** |
| Ingolstadt21 | 5 | **0.7923** | 0.6357 | 0.1845 | **+15.67 pp** |

These values are deterministic for a fixed traffic-flow graph and partition,
so mean and SD are not applicable.

### Raw retained and cut flow

| Map | Method | \(k\) | Observed edges | Total flow | Retained flow | Cut flow | \(\Phi\) |
|---|---|---:|---:|---:|---:|---:|---:|
| Cologne8 | Flow | 3 | 22 | 1,781 | 1,673 | 108 | **0.9394** |
| Cologne8 | METIS | 3 | 22 | 1,781 | 1,094 | 687 | 0.6143 |
| Cologne8 | Random | 3 | 22 | 1,781 | 242 | 1,539 | 0.1359 |
| Cologne8 | Flow | 5 | 22 | 1,781 | 1,014 | 767 | **0.5693** |
| Cologne8 | METIS | 5 | 22 | 1,781 | 740 | 1,041 | 0.4155 |
| Cologne8 | Random | 5 | 22 | 1,781 | 464 | 1,317 | 0.2605 |
| Ingolstadt21 | Flow | 4 | 71 | 13,271 | 10,843 | 2,428 | **0.8170** |
| Ingolstadt21 | METIS | 4 | 71 | 13,271 | 8,534 | 4,737 | 0.6431 |
| Ingolstadt21 | Random | 4 | 71 | 13,271 | 4,535 | 8,736 | 0.3417 |
| Ingolstadt21 | Flow | 5 | 71 | 13,271 | 10,515 | 2,756 | **0.7923** |
| Ingolstadt21 | METIS | 5 | 71 | 13,271 | 8,436 | 4,835 | 0.6357 |
| Ingolstadt21 | Random | 5 | 71 | 13,271 | 2,448 | 10,823 | 0.1845 |

**Meaning.** At the same module count, replacing road geometry with observed
movement retains an additional 15.4–32.5% of all flow mass inside
coordination modules.

---

## 2. Full-state MI dependency retention \(\Psi(D^{MI})\)

| Map | \(k\) | Flow \(\Psi(D^{MI})\) | METIS \(\Psi(D^{MI})\) | Random \(\Psi(D^{MI})\) | Paired Flow gain over METIS |
|---|---:|---:|---:|---:|---:|
| Cologne8 | 3 | **0.6405 ± 0.0092** | 0.2961 ± 0.0074 | 0.2443 ± 0.0052 | **+34.44 ± 1.66 pp** |
| Cologne8 | 5 | **0.2804 ± 0.0094** | 0.1262 ± 0.0045 | 0.1115 ± 0.0032 | **+15.42 ± 1.36 pp** |
| Ingolstadt21 | 4 | **0.2455 ± 0.0025** | 0.2181 ± 0.0032 | 0.2166 ± 0.0015 | **+2.74 ± 0.46 pp** |
| Ingolstadt21 | 5 | **0.2199 ± 0.0027** | 0.1665 ± 0.0045 | 0.1602 ± 0.0008 | **+5.34 ± 0.68 pp** |

Values are means ± sample SD over three stochastic traffic seeds. The gain SD
is calculated from the paired seed-wise Flow–METIS differences.

### Within- and cross-module MI diagnostic

| Map | Method | \(k\) | Within-module MI | Cross-module MI | Seeds with within > cross |
|---|---|---:|---:|---:|---:|
| Cologne8 | Flow | 3 | 0.5415 ± 0.0101 | 0.3510 ± 0.0206 | **3/3** |
| Cologne8 | METIS | 3 | 0.5369 ± 0.0312 | 0.4251 ± 0.0095 | 0/3 |
| Cologne8 | Flow | 5 | 0.5929 ± 0.0303 | 0.4149 ± 0.0137 | 0/3 |
| Cologne8 | METIS | 5 | 0.5339 ± 0.0287 | 0.4434 ± 0.0142 | 0/3 |
| Ingolstadt21 | Flow | 4 | 0.5058 ± 0.0171 | 0.4986 ± 0.0160 | 1/3 |
| Ingolstadt21 | METIS | 4 | 0.5095 ± 0.0237 | 0.4979 ± 0.0140 | 1/3 |
| Ingolstadt21 | Flow | 5 | 0.5134 ± 0.0168 | 0.4968 ± 0.0162 | 2/3 |
| Ingolstadt21 | METIS | 5 | 0.5147 ± 0.0290 | 0.4976 ± 0.0139 | 2/3 |

**Meaning.** Flow retains more total dependency mass in all 12 seed-level
comparisons. Strong pairwise spatial separation occurs only for Cologne8
Flow-\(k=3\); on Ingolstadt21, common demand makes within- and cross-module
means similar even though retained mass still favors Flow.

---

## 3. Physical flow versus observed dependency

| Map and dependency source | Mean Spearman \(\rho\) ± SD | Seed-level \(\rho\) | Seed-level \(p\) | Interpretation |
|---|---:|---|---|---|
| Cologne8, full state | **0.5143 ± 0.0937** | 0.5427, 0.5906, 0.4097 | 1.55e−5, 1.65e−6, 0.00171 | Moderate-to-strong alignment in every seed |
| Ingolstadt21, full state | **0.1409 ± 0.0339** | 0.1797, 0.1264, 0.1167 | 0.000214, 0.00952, 0.01673 | Weak but positive alignment in every seed |
| Ingolstadt21, queue total only | 0.0314 ± 0.0234 | 0.0166, 0.0584, 0.0191 | 0.735, 0.233, 0.696 | No detectable alignment |

**Meaning.** Full multidimensional traffic state, rather than queue total
alone, carries the dependency relationship associated with physical flow.

### Ingolstadt21 queue-total sensitivity

| \(k\) | Flow \(\Psi(D^{MI}_{queue})\) | METIS \(\Psi(D^{MI}_{queue})\) | Random \(\Psi(D^{MI}_{queue})\) | Paired Flow gain over METIS |
|---:|---:|---:|---:|---:|
| 4 | **0.2783 ± 0.0103** | 0.2053 ± 0.0075 | 0.2206 ± 0.0016 | **+7.30 ± 1.48 pp** |
| 5 | **0.2783 ± 0.0103** | 0.1382 ± 0.0089 | 0.1309 ± 0.0069 | **+14.01 ± 0.69 pp** |

---

## 4. Learned CoLight dependency retention \(\Psi(D^G)\)

| Map | \(k\) | Flow \(\Psi(D^G)\) | METIS \(\Psi(D^G)\) | Random \(\Psi(D^G)\) | Flow gain over METIS | Flow–\(D^G\) \(\rho\) |
|---|---:|---:|---:|---:|---:|---:|
| Cologne8 | 3 | **0.7542** | 0.5906 | 0.2473 | **+16.37 pp** | 0.7961 |
| Cologne8 | 5 | 0.3703 | **0.4763** | 0.3110 | **−10.60 pp** | 0.7961 |
| Ingolstadt21 | 4 | **0.7979** | 0.6693 | 0.2458 | **+12.86 pp** | 0.7503 |
| Ingolstadt21 | 5 | 0.6998 | **0.7314** | 0.2554 | **−3.17 pp** | 0.7503 |

Each map uses one seed-7 global, no-partition CoLight checkpoint and one
evaluated observation. There is no across-checkpoint SD.

**Meaning.** Learned one-hop dependency strongly aligns with flow at the
matrix level, but METIS retains more of it at \(k=5\). Fine partitions can
cut live adjacency/message-passing edges even when they retain corridor flow.

### Learned dependency range

| Map | Agents | Graph diameter | Influence-weighted range | Hop-1 / hop-0 influence | Normalized attention entropy |
|---|---:|---:|---:|---:|---:|
| Cologne8 | 8 | 3 | 0.5729 | 1.3289 | ≈1.0000 |
| Ingolstadt21 | 21 | 4 | 0.5675 | 1.4129 | ≈1.0000 |

---

## 5. Centralized MAPPO critic dependency retention \(\Psi(D^Q)\)

### Definition and audit protocol

\(D^Q_{t,s}\) is the absolute gradient mass of target \(t\)'s centralized
critic value with respect to source \(s\)'s observation features, averaged
over 100 queue-load-stratified held-out observations. Diagonal mass is
excluded when calculating \(\Psi\).

- Critics: three independently trained Cologne8 R2 global MAPPO critics,
  seeds 1–3.
- Checkpoint: each run's saved best MAPPO checkpoint.
- Trace: 10 stochastic-policy episodes at trace seed 7001; observations are
  selected from held-out episodes.
- Integrity check: critic parameters were hashed before and after every
  Jacobian audit and were unchanged.
- The candidate partition is applied **after** estimating each global
  dependency matrix. Regional critic matrices are not used because their
  structural cross-module zeros would circularly favor their own partition.
- Cologne8 \(k=5\) candidates were regenerated with the current partitioner
  from the same stored realized route file because the historical \(k=5\)
  directories were unavailable.

### Raw seed-level values

| Map | \(k\) | Global critic seed | Flow \(\Psi(D^Q)\) | METIS \(\Psi(D^Q)\) | Random \(\Psi(D^Q)\) | Flow gain over METIS |
|---|---:|---:|---:|---:|---:|---:|
| Cologne8 | 3 | 1 | **0.6073** | 0.2531 | 0.2522 | **+35.42 pp** |
| Cologne8 | 3 | 2 | **0.6149** | 0.2578 | 0.2517 | **+35.70 pp** |
| Cologne8 | 3 | 3 | **0.5957** | 0.2556 | 0.2532 | **+34.01 pp** |
| Cologne8 | 5 | 1 | **0.2525** | 0.1137 | 0.1080 | **+13.88 pp** |
| Cologne8 | 5 | 2 | **0.2659** | 0.1150 | 0.1081 | **+15.08 pp** |
| Cologne8 | 5 | 3 | **0.2578** | 0.1154 | 0.1043 | **+14.24 pp** |

### Mean ± SD across global critic seeds

| Map | \(k\) | Flow \(\Psi(D^Q)\) | METIS \(\Psi(D^Q)\) | Random \(\Psi(D^Q)\) | Paired Flow gain over METIS |
|---|---:|---:|---:|---:|---:|
| Cologne8 | 3 | **0.6060 ± 0.0097** | 0.2555 ± 0.0023 | 0.2524 ± 0.0008 | **+35.04 ± 0.91 pp** |
| Cologne8 | 5 | **0.2587 ± 0.0067** | 0.1147 ± 0.0009 | 0.1068 ± 0.0022 | **+14.40 ± 0.62 pp** |

**Meaning.** Flow preserves substantially more centralized-critic dependency
than both METIS and Random at both module counts. The low seed dispersion and
the positive gain in every critic seed make this the strongest model-derived
support for the Flow → dependency link.

### Coverage limitation

| Map | \(k\) | Status | Reason |
|---|---:|---|---|
| Ingolstadt21 | 4 | Not estimable | No global MAPPO checkpoint weights are available locally or as downloadable W&B model files. |
| Ingolstadt21 | 5 | Not estimable | No global MAPPO checkpoint weights are available locally or as downloadable W&B model files. |

The available Ingolstadt21 R2 MAPPO checkpoints use regional critics. They are
intentionally excluded rather than reported as artificially high
partition-retention estimates.

---

## 6. Constrained selection benchmark

| Quantity | Value | Scope |
|---|---:|---|
| Total candidate records | 337,575 | Both maps combined |
| Feasible records | 62,257 | Both maps combined |
| Unique connected, size-bounded partitions | 4,935 | Both maps combined |
| Validation-front unique partitions | 5 | Cologne8 |
| Validation-front unique partitions | 16 | Ingolstadt21 |

### Connected-null adjusted held-out CMI retention

| Frontier point | Margin over connected null |
|---|---:|
| Cologne8 validation-selected best | **+10.9 pp** |
| Ingolstadt21 validation-selected best | **+1.5 pp** |
| Ingolstadt21 post-hoc held-out best | **+5.4 pp** |

**Meaning.** Retention remains above connected operational alternatives, but
the best held-out partition can differ from the validation choice. Candidate
selection must therefore remain validation-only.

---

## 7. Causal and spillback diagnostics

| Diagnostic | Cologne8 | Ingolstadt21 | Interpretation |
|---|---|---|---|
| Spillback events | 0 | 1, 2, and 0 across three seeds | Too sparse for a spillback-retention claim |
| Observed action-to-future-queue CMI | No edge separated from its matched null | No edge separated from its matched null | No resolved action-level coupling |
| Randomized action perturbation | No held-out edge separated from null | No held-out edge separated from null | Intervention changed behavior but did not resolve cross-agent causal effects |
| Hop-\(\geq3\) negative controls | 0.00–0.05 | 0.00–0.05 | Negative controls behaved as expected |

**Meaning.** The supported mechanism is optimization conditioning through
correlated within-module signals, not demonstrated action-level causality in
this undersaturated demand regime.

---

## 8. Completed R2 training: best-checkpoint time loss

Every row uses three training seeds. Values are mean ± sample SD in seconds
per vehicle.

| Map | Learner | \(k\) | Flow | METIS | None | Random | Flow vs METIS | Flow vs None | Flow vs Random |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cologne8 | IPPO | 3 | **183.86 ± 81.64** | 495.94 ± 120.26 | 316.72 ± 239.75 | 351.45 ± 70.90 | **+62.9%** | **+42.0%** | **+47.7%** |
| Cologne8 | MAPPO | 3 | **50.68 ± 6.98** | 66.40 ± 12.14 | 79.59 ± 27.78 | 60.26 ± 11.13 | **+23.7%** | **+36.3%** | **+15.9%** |
| Cologne8 | CoLight | 3 | 22.14 ± 0.33 | 21.60 ± 0.46 | 22.38 ± 0.33 | **21.14 ± 0.25** | −2.5% | +1.0% | −4.8% |
| Ingolstadt21 | IPPO | 4 | **1290.54 ± 49.95** | 1309.49 ± 46.01 | — | — | +1.4% | — | — |
| Ingolstadt21 | MAPPO | 4 | 936.61 ± 101.81 | **889.77 ± 236.05** | — | — | −5.3% | — | — |

**Meaning.** Flow provides large replicated gains for Cologne8 IPPO and
MAPPO. The other completed comparisons are small relative to their seed
dispersion and should be described as neutral.

### Full R2 metrics at the time-loss-selected checkpoint

For phase length, the last column is a signed relative change, not a
performance gain; shorter or longer phases are not universally preferable.

| Map | Learner | \(k\) | Metric | Flow mean ± SD | METIS mean ± SD | Flow gain/effect |
|---|---|---:|---|---:|---:|---:|
| Cologne8 | CoLight | 3 | Time loss | 22.14 ± 0.33 | 21.60 ± 0.46 | −2.5% |
| Cologne8 | CoLight | 3 | Duration | 87.35 ± 0.34 | 86.78 ± 0.57 | −0.7% |
| Cologne8 | CoLight | 3 | Waiting time | 9.41 ± 0.26 | 8.87 ± 0.50 | −6.0% |
| Cologne8 | CoLight | 3 | Reward | −2.53 ± 0.08 | −2.43 ± 0.09 | −4.1% |
| Cologne8 | CoLight | 3 | Maximum queue | 0.75 ± 0.02 | 0.70 ± 0.03 | −6.8% |
| Cologne8 | CoLight | 3 | Queue length | 1.08 ± 0.03 | 1.04 ± 0.04 | −3.8% |
| Cologne8 | CoLight | 3 | Vehicles completed | 2046.00 ± 0.00 | 2046.00 ± 0.00 | 0.0% |
| Cologne8 | CoLight | 3 | Phase length | 401.05 ± 128.48 | 65.76 ± 18.83 | +509.9% change |
| Cologne8 | IPPO | 3 | Time loss | **183.86 ± 81.64** | 495.94 ± 120.26 | **+62.9%** |
| Cologne8 | IPPO | 3 | Duration | **237.27 ± 72.08** | 391.36 ± 75.34 | **+39.4%** |
| Cologne8 | IPPO | 3 | Waiting time | **160.65 ± 74.32** | 322.90 ± 79.88 | **+50.2%** |
| Cologne8 | IPPO | 3 | Reward | **−18.26 ± 8.90** | −27.20 ± 5.32 | **+32.9%** |
| Cologne8 | IPPO | 3 | Maximum queue | **4.22 ± 1.01** | 7.35 ± 1.80 | **+42.6%** |
| Cologne8 | IPPO | 3 | Queue length | **7.64 ± 1.07** | 18.26 ± 5.79 | **+58.1%** |
| Cologne8 | IPPO | 3 | Vehicles completed | 2046.00 ± 0.00 | 2046.00 ± 0.00 | 0.0% |
| Cologne8 | IPPO | 3 | Phase length | 918.51 ± 164.55 | 820.89 ± 245.89 | +11.9% change |
| Cologne8 | MAPPO | 3 | Time loss | **50.68 ± 6.98** | 66.40 ± 12.14 | **+23.7%** |
| Cologne8 | MAPPO | 3 | Duration | **115.81 ± 6.59** | 129.75 ± 10.51 | **+10.7%** |
| Cologne8 | MAPPO | 3 | Waiting time | **35.69 ± 7.37** | 51.31 ± 11.16 | **+30.4%** |
| Cologne8 | MAPPO | 3 | Reward | **−2.36 ± 1.57** | −7.50 ± 0.97 | **+68.6%** |
| Cologne8 | MAPPO | 3 | Maximum queue | **2.09 ± 0.22** | 2.32 ± 0.40 | **+9.9%** |
| Cologne8 | MAPPO | 3 | Queue length | **2.89 ± 0.31** | 3.68 ± 0.61 | **+21.5%** |
| Cologne8 | MAPPO | 3 | Vehicles completed | 2046.00 ± 0.00 | 2046.00 ± 0.00 | 0.0% |
| Cologne8 | MAPPO | 3 | Phase length | 151.32 ± 28.34 | 217.22 ± 27.65 | −30.3% change |
| Ingolstadt21 | IPPO | 4 | Time loss | **1290.54 ± 49.95** | 1309.49 ± 46.01 | +1.4% |
| Ingolstadt21 | IPPO | 4 | Duration | 1086.00 ± 51.54 | **949.31 ± 165.56** | −14.4% |
| Ingolstadt21 | IPPO | 4 | Waiting time | 997.01 ± 45.96 | **860.12 ± 153.44** | −15.9% |
| Ingolstadt21 | IPPO | 4 | Reward | −42.92 ± 1.42 | **−42.24 ± 2.95** | −1.6% |
| Ingolstadt21 | IPPO | 4 | Maximum queue | **7.08 ± 0.35** | 7.09 ± 0.31 | +0.2% |
| Ingolstadt21 | IPPO | 4 | Queue length | 15.60 ± 1.50 | **15.54 ± 0.25** | −0.4% |
| Ingolstadt21 | IPPO | 4 | Vehicles completed | 4283.00 ± 0.00 | 4283.00 ± 0.00 | 0.0% |
| Ingolstadt21 | IPPO | 4 | Phase length | 862.10 ± 29.99 | 894.97 ± 145.01 | −3.7% change |
| Ingolstadt21 | MAPPO | 4 | Time loss | 936.61 ± 101.81 | **889.77 ± 236.05** | −5.3% |
| Ingolstadt21 | MAPPO | 4 | Duration | 763.84 ± 15.81 | **737.81 ± 137.44** | −3.5% |
| Ingolstadt21 | MAPPO | 4 | Waiting time | 638.42 ± 37.58 | **601.01 ± 162.26** | −6.2% |
| Ingolstadt21 | MAPPO | 4 | Reward | −28.63 ± 4.20 | **−25.11 ± 6.92** | −14.0% |
| Ingolstadt21 | MAPPO | 4 | Maximum queue | **5.25 ± 0.81** | 5.32 ± 0.87 | +1.5% |
| Ingolstadt21 | MAPPO | 4 | Queue length | **10.75 ± 1.57** | 10.78 ± 1.99 | +0.3% |
| Ingolstadt21 | MAPPO | 4 | Vehicles completed | 4283.00 ± 0.00 | 4283.00 ± 0.00 | 0.0% |
| Ingolstadt21 | MAPPO | 4 | Phase length | 400.81 ± 49.27 | 350.29 ± 158.90 | +14.4% change |

---

## 9. Legacy 1,500-episode best-checkpoint results

These runs provide broader algorithm and module-count coverage but use one
training seed. They should be presented as exploratory sensitivity results,
not pooled with the R2 estimates.

| Map | Learner | \(k\) | Flow time loss | METIS time loss | Flow gain |
|---|---|---:|---:|---:|---:|
| Ingolstadt21 | MAPPO | 4 | **191.3** | 374.0 | **+48.9%** |
| Ingolstadt21 | MAPPO | 5 | **128.1** | 371.9 | **+65.5%** |
| Ingolstadt21 | IPPO | 4 | **379.4** | 879.9 | **+56.9%** |
| Ingolstadt21 | IPPO | 5 | **230.3** | 673.9 | **+65.8%** |
| Ingolstadt21 | CoLight | 4 | **376.4** | 447.0 | **+15.8%** |
| Ingolstadt21 | CoLight | 5 | **420.6** | 537.5 | **+21.7%** |
| Ingolstadt21 | FMA2C | 4 | **744.5** | 967.4 | **+23.0%** |
| Ingolstadt21 | FMA2C | 5 | **930.1** | 956.4 | +2.8% |
| Cologne8 | IPPO | 3 | **26.7** | 33.8 | **+21.0%** |
| Cologne8 | MAPPO | 3 | **25.0** | 25.2 | +0.9% |
| Cologne8 | CoLight | 3 | 32.6 | **29.3** | −11.3% |
| Cologne8 | FMA2C | 3 | **49.3** | 58.7 | **+15.9%** |

**Meaning.** Flow is favorable in 9 of 12 legacy comparisons, including all
four coordination mechanisms. Because these are single-seed best-checkpoint
values, they demonstrate attainable gains rather than expected multiseed
performance.

---

## 10. Recovered historical W&B endpoints

This table records all deduplicated finished, known-seed CoLight,
CoLightRegional, and FMA2C groups recovered from W&B. It is provenance
context, not a matched experiment: several rows mix cohorts, step lengths,
reward settings, and unpaired seeds.

| Map | Algorithm | Partition | \(n\) | Seeds | Time loss mean ± SD | Waiting time mean ± SD | Cohorts |
|---|---|---|---:|---|---:|---:|---|
| Cologne8 | CoLight | baseline | 4 | 1,2,3,7 | 25.84 ± 5.23 | 11.69 ± 3.09 | legacy_2026-06, R2 |
| Cologne8 | CoLight | flow_k3 | 3 | 1,2,3 | 27.98 ± 4.85 | 14.56 ± 5.13 | R2 |
| Cologne8 | CoLight | metis_k3 | 3 | 1,2,3 | 70.43 ± 82.58 | 55.19 ± 79.02 | R2 |
| Cologne8 | CoLight | random_k3 | 3 | 1,2,3 | 22.31 ± 0.70 | 9.26 ± 0.63 | R2 |
| Cologne8 | CoLightRegional | flow_k3 | 1 | 7 | 46.81 ± — | 28.06 ± — | legacy_2026-06 |
| Cologne8 | CoLightRegional | metis_k3 | 1 | 7 | 34.14 ± — | 15.92 ± — | legacy_2026-06 |
| Cologne8 | FMA2C | baseline | 2 | 0,67 | 888.86 ± 40.43 | 534.78 ± 33.21 | legacy_2026-06, legacy_20260526 |
| Cologne8 | FMA2C | flow_k3 | 3 | 7,27,67 | 809.68 ± 661.78 | 413.75 ± 295.81 | legacy_2026-06, legacy_20260526, rescoalign |
| Cologne8 | FMA2C | metis_k3 | 3 | 7,27,67 | 909.64 ± 690.34 | 517.06 ± 394.47 | legacy_2026-06, legacy_20260526, rescoalign |
| Ingolstadt21 | CoLight | baseline | 1 | 7 | 1086.50 ± — | 817.14 ± — | refire |
| Ingolstadt21 | CoLight | flow_k4 | 4 | 1,2,3,67 | 843.82 ± 213.25 | 649.29 ± 155.54 | legacy_20260526, R2 |
| Ingolstadt21 | CoLight | metis_k4 | 4 | 1,2,3,67 | 713.26 ± 142.34 | 541.97 ± 98.47 | legacy_20260526, R2 |
| Ingolstadt21 | CoLightRegional | flow_k4 | 1 | 7 | 872.64 ± — | 641.80 ± — | refire |
| Ingolstadt21 | CoLightRegional | flow_k5 | 1 | 7 | 906.83 ± — | 597.68 ± — | refire |
| Ingolstadt21 | CoLightRegional | metis_k4 | 1 | 7 | 698.42 ± — | 478.20 ± — | refire |
| Ingolstadt21 | CoLightRegional | metis_k5 | 1 | 7 | 792.42 ± — | 546.95 ± — | refire |
| Ingolstadt21 | FMA2C | baseline | 1 | 21 | 1273.06 ± — | 942.05 ± — | legacy_2026-05 |
| Ingolstadt21 | FMA2C | flow_k4 | 2 | 7,67 | 973.28 ± 654.99 | 655.45 ± 336.28 | legacy_20260526, legacy_20260603 |
| Ingolstadt21 | FMA2C | flow_k5 | 1 | 7 | 587.48 ± — | 464.10 ± — | legacy_20260603 |
| Ingolstadt21 | FMA2C | metis_k4 | 2 | 7,67 | 929.59 ± 596.30 | 707.69 ± 408.64 | legacy_20260526, legacy_20260603 |
| Ingolstadt21 | FMA2C | metis_k5 | 1 | 7 | 613.64 ± — | 394.56 ± — | legacy_20260603 |

**Meaning.** The recovered endpoints are useful for completeness and
sensitivity checks, but the large FMA2C dispersion and mixed cohorts prevent
their means from being interpreted as clean partition effects.

---

## Report-ready interpretation

1. **Direct structural gain:** Flow retains 15.4–32.5 pp more physical flow
   than METIS in every matched block.
2. **Training-free dependency gain:** Flow retains 2.7–34.4 pp more
   full-state MI dependency, with Flow > METIS in every traffic seed.
3. **Value-relevant dependency gain:** on three global MAPPO critics, Flow
   retains 35.04 ± 0.91 pp more \(D^Q\) at \(k=3\) and 14.40 ± 0.62 pp more
   at \(k=5\).
4. **Control gain where the coordination mechanism benefits:** Flow reduces
   Cologne8 IPPO and MAPPO best-checkpoint time loss by 62.9% and 23.7%
   relative to METIS, without partition-specific learner tuning.
5. **Boundary of the claim:** CoLight and the completed Ingolstadt21 R2
   comparisons are neutral or slightly METIS-favored. Flow is therefore a
   strong, inexpensive candidate generator with potentially large gains, not
   a universally optimal configuration.
