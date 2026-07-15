# Consolidated analysis results

## Report-ready summary

Flow-aware partitioning consistently preserves more observed traffic flow and more state-derived mutual-information (MI) dependency than same-size METIS partitioning. The advantage is large on Cologne8 and smaller but stable on Ingolstadt21. Dependencies extracted from a trained global CoLight model support the same conclusion at the lower tested module count, but not uniformly at `k=5`: METIS retains slightly more learned model dependency at `k=5` on both maps. The downstream seed-0 training results are strongest for MAPPO with flow partitions, but these runs are not sufficient for a general statistical performance claim.

The report should make the following claims:

1. **Physical-flow retention:** flow partitions outperform same-`k` METIS partitions by 15.4–32.5 percentage points (pp) on Cologne8 and 15.7–17.4 pp on Ingolstadt21.
2. **State-dependency retention:** flow partitions retain more full-state lagged MI for every map, `k`, and stochastic seed tested. Mean gains are 34.4 pp at Cologne8 `k=3`, 15.4 pp at Cologne8 `k=5`, 2.7 pp at Ingolstadt21 `k=4`, and 5.3 pp at Ingolstadt21 `k=5`.
3. **Flow–dependency alignment:** physical flow is strongly correlated with state MI on Cologne8 and weakly but significantly correlated with full-state MI on Ingolstadt21. Queue-total-only MI does not show significant alignment on Ingolstadt21.
4. **Learned CoLight dependency:** flow partitions retain more `D_G` at the lower module count, while METIS retains 3.2–10.6 pp more at `k=5`. This is an important exception to the otherwise consistent flow-partition result.
5. **Training outcome:** in the available completed Ingolstadt21 seed-0 runs, MAPPO-flow-`k4` gives the lowest final waiting time, while MAPPO-flow-`k5` gives the best waiting-time learning-curve AUC. These are descriptive single-seed results only.

## Metrics and evaluation scope

- Φ, **flow retention**, is the fraction of observed directed traffic flow whose source and destination remain in the same module.
- `Ψ(P,D)`, **dependency retention**, is the fraction of off-diagonal dependency mass in matrix `D` retained within modules under partition `P`.
- `D_MI` is the lagged KSG MI matrix, averaged over lags 1, 5, 15, and 30 with `k_KSG=3`.
- `D_G` is learned CoLight model dependency: the absolute input gradient of every valid target Q-value, summed over input features and valid target actions.
- ρ is Spearman correlation between off-diagonal directed flow weights and dependency values.
- H1 tests whether within-module MI exceeds cross-module MI using a paired one-sided Wilcoxon test over agents.
- H2 tests whether spillback events are overrepresented within modules using a one-sided binomial test.

State MI uses three stochastic seeds per map, one 361-step episode per seed. Cologne8 has 8 agents with a 30-dimensional state per agent; Ingolstadt21 has 21 agents with an 85-dimensional state per agent. Values below are means ± sample standard deviations over seeds unless stated otherwise.

## Physical-flow retention

| Map | Partition | `k` | Observed edges | Total flow | Retained flow | Cut flow | Φ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cologne8 | Flow | 3 | 22 | 1,781 | 1,673 | 108 | **0.9394** |
| Cologne8 | METIS | 3 | 22 | 1,781 | 1,094 | 687 | 0.6143 |
| Cologne8 | Flow | 5 | 22 | 1,781 | 1,014 | 767 | **0.5693** |
| Cologne8 | METIS | 5 | 22 | 1,781 | 740 | 1,041 | 0.4155 |
| Cologne8 | Flow-auto | auto | 22 | 1,781 | 1,781 | 0 | 1.0000 |
| Ingolstadt21 | Flow | 4 | 71 | 13,271 | 10,843 | 2,428 | **0.8170** |
| Ingolstadt21 | METIS | 4 | 71 | 13,271 | 8,534 | 4,737 | 0.6431 |
| Ingolstadt21 | Flow | 5 | 71 | 13,271 | 10,515 | 2,756 | **0.7923** |
| Ingolstadt21 | METIS | 5 | 71 | 13,271 | 8,436 | 4,835 | 0.6357 |
| Ingolstadt21 | Flow-auto | auto | 71 | 13,271 | 10,255 | 3,016 | 0.7727 |

For like-for-like comparisons, flow improves Φ over METIS by **0.3251** at Cologne8 `k=3`, **0.1538** at Cologne8 `k=5`, **0.1740** at Ingolstadt21 `k=4`, and **0.1567** at Ingolstadt21 `k=5`. Flow-auto is reported for completeness but should not be used as a same-`k` comparison.

## Full-state MI dependency retention

| Map | Partition | `k` | `Ψ(P,D_MI)` | Flow−METIS ΔΨ | H1 within MI | H1 cross MI | H1 passes |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cologne8 | Flow | 3 | **0.6405 ± 0.0092** | **+0.3444 ± 0.0166** | 0.5415 ± 0.0101 | 0.3510 ± 0.0206 | **3/3** |
| Cologne8 | METIS | 3 | 0.2961 ± 0.0074 | — | 0.5369 ± 0.0312 | 0.4251 ± 0.0095 | 0/3 |
| Cologne8 | Flow | 5 | **0.2804 ± 0.0094** | **+0.1542 ± 0.0136** | 0.5929 ± 0.0303 | 0.4149 ± 0.0137 | 0/3 |
| Cologne8 | METIS | 5 | 0.1262 ± 0.0045 | — | 0.5339 ± 0.0287 | 0.4434 ± 0.0142 | 0/3 |
| Ingolstadt21 | Flow | 4 | **0.2455 ± 0.0025** | **+0.0274 ± 0.0046** | 0.5058 ± 0.0171 | 0.4986 ± 0.0160 | 1/3 |
| Ingolstadt21 | METIS | 4 | 0.2181 ± 0.0032 | — | 0.5095 ± 0.0237 | 0.4979 ± 0.0140 | 1/3 |
| Ingolstadt21 | Flow | 5 | **0.2199 ± 0.0027** | **+0.0534 ± 0.0068** | 0.5134 ± 0.0168 | 0.4968 ± 0.0162 | 2/3 |
| Ingolstadt21 | METIS | 5 | 0.1665 ± 0.0045 | — | 0.5147 ± 0.0290 | 0.4976 ± 0.0139 | 2/3 |

The seed-level Ψ ordering is identical in all 12 same-`k` comparisons: flow > METIS. H1 gives strong, repeatable spatial separation only for Cologne8 flow-`k3`. On Ingolstadt21, within- and cross-module mean MI are close, so H1 support is seed-dependent even though total retained dependency mass Ψ consistently favors flow.

## Physical flow versus state dependency

| Map and dependency source | Mean ρ ± SD | Seed-level ρ | Seed-level `p` | Interpretation |
|---|---:|---:|---:|---|
| Cologne8, full state `X` | **0.5143 ± 0.0937** | 0.5427, 0.5906, 0.4097 | 1.55e−5, 1.65e−6, 0.00171 | Moderate-to-strong positive alignment in all seeds |
| Ingolstadt21, full state `X` | **0.1409 ± 0.0339** | 0.1797, 0.1264, 0.1167 | 0.000214, 0.00952, 0.01673 | Weak positive alignment, significant in all seeds |
| Ingolstadt21, queue total only | 0.0314 ± 0.0234 | 0.0166, 0.0584, 0.0191 | 0.735, 0.233, 0.696 | No significant alignment |

The full multidimensional state is therefore the appropriate headline `D_MI` source. Queue-total-only dependency omits relationships visible in the complete state and should remain a sensitivity result.

### Queue-total sensitivity result for Ingolstadt21

| Partition | `k` | `Ψ(P,D_MI_queue)` | Flow−METIS ΔΨ | H1 within | H1 cross | H1 passes |
|---|---:|---:|---:|---:|---:|---:|
| Flow | 4 | **0.2783 ± 0.0103** | **+0.0730 ± 0.0148** | 0.1239 ± 0.0133 | 0.1035 ± 0.0157 | 0/3 |
| METIS | 4 | 0.2053 ± 0.0075 | — | 0.1040 ± 0.0151 | 0.1097 ± 0.0153 | 0/3 |
| Flow | 5 | **0.2783 ± 0.0103** | **+0.1401 ± 0.0069** | 0.1404 ± 0.0151 | 0.0998 ± 0.0151 | 0/3 |
| METIS | 5 | 0.1382 ± 0.0089 | — | 0.0921 ± 0.0082 | 0.1117 ± 0.0165 | 0/3 |

## Spillback diagnostic

H2 is inconclusive. Ingolstadt21 produced only 1 event in seed 0, 2 events in seed 1, and no events in seed 2. No partition/seed combination passed `p<0.05`; observed `p`-values ranged from 0.466 to 1.000 when events existed. Cologne8 produced no spillback events. These counts are too small to support a claim about within-module spillback concentration.

## Learned CoLight model dependency

Only Jacobians from global, no-partition CoLight checkpoints are used for headline `D_G`. Partition-restricted checkpoint Jacobians would impose structural cross-partition zeros and artificially favor their own partition. Each map's result comes from one seed-7 checkpoint and one evaluated observation, so `D_G` has no across-seed uncertainty estimate.

| Map | Partition | `k` | `Ψ(P,D_G)` | Flow−METIS ΔΨ | Φ | Flow–`D_G` ρ | `p` |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cologne8 | Flow | 3 | **0.7542** | **+0.1637** | 0.9394 | 0.7961 | 2.23e−13 |
| Cologne8 | METIS | 3 | 0.5906 | — | 0.6143 | 0.7961 | 2.23e−13 |
| Cologne8 | Flow | 5 | 0.3703 | **−0.1060** | 0.5693 | 0.7961 | 2.23e−13 |
| Cologne8 | METIS | 5 | **0.4763** | — | 0.4155 | 0.7961 | 2.23e−13 |
| Ingolstadt21 | Flow | 4 | **0.7979** | **+0.1286** | 0.8170 | 0.7503 | 3.98e−77 |
| Ingolstadt21 | METIS | 4 | 0.6693 | — | 0.6431 | 0.7503 | 3.98e−77 |
| Ingolstadt21 | Flow | 5 | 0.6998 | **−0.0317** | 0.7923 | 0.7503 | 3.98e−77 |
| Ingolstadt21 | METIS | 5 | **0.7314** | — | 0.6357 | 0.7503 | 3.98e−77 |

The underlying learned dependency aligns strongly with physical flow on both maps. However, strong matrix-level correlation does not guarantee that every fixed-`k` partition maximizes retained `D_G`, which explains the `k=5` reversal.

### Learned dependency range and attention

| Map | Agents | Graph diameter | Influence-weighted range `R` | Mean hop-1 / hop-0 influence | Mean normalized attention entropy |
|---|---:|---:|---:|---:|---:|
| Cologne8 | 8 | 3 | 0.5729 | 1.3289 | ≈1.0000 |
| Ingolstadt21 | 21 | 4 | 0.5675 | 1.4129 | ≈1.0000 |

The analyzed CoLight models have nonzero Jacobian influence only at hops 0 and 1 for this observation/model structure. Normalized attention entropy is approximately 1.0 (5 heads; 22 Cologne8 and 63 Ingolstadt21 messages), indicating nearly uniform attention over each target's available neighbors in the evaluated forward pass.

## Random-partition control

The random baseline uses partition seed 0. Agents are shuffled with a local seeded RNG and assigned round-robin, producing size-balanced modules whose sizes differ by at most one. The same realized traffic-flow weights, stochastic state traces, lagged MI settings, and global CoLight `D_G` matrices used for flow and METIS are reused here, making the retention values directly comparable. This is one reproducible random partition per map/`k`, not an average over random partition seeds; the uncertainty below covers traffic-trace seeds only.

| Map | `k` | Module sizes | Random Φ | Retained / cut flow | Random `Ψ(P,D_MI)` | H1 within / cross MI | H1 passes | Random `Ψ(P,D_G)` |
|---|---:|---|---:|---|---:|---|---:|---:|
| Cologne8 | 3 | 3, 3, 2 | 0.1359 | 242 / 1,539 | 0.2443 ± 0.0052 | 0.4425 / 0.4566 | 0/3 | 0.2473 |
| Cologne8 | 5 | 2, 2, 2, 1, 1 | 0.2605 | 464 / 1,317 | 0.1115 ± 0.0032 | 0.4715 / 0.4509 | 0/3 | 0.3110 |
| Ingolstadt21 | 4 | 6, 5, 5, 5 | 0.3417 | 4,535 / 8,736 | 0.2166 ± 0.0015 | 0.5059 / 0.4989 | 0/3 | 0.2458 |
| Ingolstadt21 | 5 | 5, 4, 4, 4, 4 | 0.1845 | 2,448 / 10,823 | 0.1602 ± 0.0008 | 0.4950 / 0.5014 | 0/3 | 0.2554 |

Full-state MI statistics are means ± sample SD over the three stochastic traffic seeds. Random assignment does not produce significant within-module MI concentration: all 12 random H1 tests fail at `p<0.05`. Cologne8 has no H2 spillback events under random partitioning either. Ingolstadt21 again has only 1, 2, and 0 events across seeds; no random partition/seed passes H2 (`p` ranges from 0.0857 to 1.0 when events exist).

**Report-ready read:** random is the chance floor for every instrument and every `(map, k)` — Φ, Ψ(D_MI), and Ψ(D_G) all rank random below both Flow and METIS. The one cell worth flagging explicitly: on Ingolstadt21 `k=4`, METIS's Ψ(D_MI) margin over random is only +0.0015 (0.2181 vs. 0.2166, an order of magnitude below the ± SD), i.e. topology-based partitioning is statistically indistinguishable from chance there, while flow still clears random by +0.0289. H1 pass-count ties (METIS = random at Cologne8, both 0/3; METIS = flow at Ingolstadt21, both beat random) reinforce that Ψ, not the pairwise H1 test, is the statistic that separates flow from METIS specifically. The `k=5` Ψ(D_G) reversal (flow vs. METIS) is unaffected in kind — both remain far above random at that `k` — so the reversal is a second-order effect between two structured methods, not a sign that structure stops mattering.

## Downstream training results

All listed runs completed 1,500 episodes, but only seed 0 is available and normalized held-out testing metrics are absent. Lower values are better for every metric shown.

| Algorithm | Partition | Final waiting time | Final time loss | Final duration | Final queue | Waiting-time AUC | Late-run σ |
|---|---:|---:|---:|---:|---:|---:|---:|
| MAPPO | Global/no partition | 484.189 | 566.429 | 659.064 | 9.586 | 545.209 | 137.995 |
| MAPPO | Flow `k=4` | **140.955** | **191.249** | **326.293** | 4.442 | 589.408 | 154.347 |
| MAPPO | Flow `k=5` | 160.510 | 262.478 | 328.826 | **4.242** | **507.846** | 148.202 |
| MAPPO | METIS `k=4` | 401.166 | 607.964 | 547.388 | 7.884 | 648.332 | **133.184** |
| MAPPO | METIS `k=5` | 640.820 | 746.898 | 828.651 | 11.618 | 654.037 | 157.856 |
| IPPO | Flow `k=4` | 564.961 | 619.426 | 725.577 | 8.047 | 647.102 | 101.458 |
| IPPO | Flow `k=5` | **202.708** | **253.144** | **382.593** | **4.887** | **577.800** | 134.260 |
| IPPO | METIS `k=4` | 846.139 | 1,048.572 | 962.234 | 12.136 | 903.487 | 65.400 |
| IPPO | METIS `k=5` | 526.099 | 694.796 | 670.518 | 7.904 | 795.081 | **50.185** |

Within MAPPO, flow-`k4` reduces final waiting time by 64.9% relative to METIS-`k4`, and flow-`k5` reduces it by 75.0% relative to METIS-`k5`. Relative to global MAPPO, the reductions are 70.9% and 66.8%, respectively. Within IPPO, flow-`k5` outperforms METIS-`k5` by 61.5% in final waiting time, whereas flow-`k4` also outperforms METIS-`k4` but remains worse than global MAPPO. AUC and final-episode rankings differ for MAPPO flow-`k4`, so the report should present both convergence quality and final performance.

## Overall interpretation

The strongest supported conclusion is that flow-aware partitioning better preserves physically meaningful and state-observed inter-signal dependencies than topology-balanced METIS at the same module count. This result is stable across stochastic seeds. The effect is strongest on Cologne8 flow-`k3`, where Φ, `Ψ(P,D_MI)`, H1, and `Ψ(P,D_G)` all agree.

Ingolstadt21 is more nuanced. Flow still wins every physical-flow and state-MI retention comparison, but its full-state MI gain is modest, H1 is inconsistent, spillback data are too sparse, and learned `D_G` favors METIS slightly at `k=5`. The training results favor flow partitions, especially with MAPPO, but require multiple seeds and normalized testing before being presented as confirmatory evidence rather than a case study.

## Report figures and source tables (not available in this repo)

- [Flow-retention table](outputs/flow_retention/flow_retention.csv)
- [Three-seed state-MI summary](outputs/state_diagnostics/state_diagnostics_summary.csv)
- [Ingolstadt21 full-state MI summary](outputs/state_diagnostics_full_state/state_diagnostics_summary.csv)
- [Partition heatmap index](outputs/partition_heatmaps_focus/partition_heatmaps.csv)
- [Cologne8 learned-dependency heatmap](outputs/model_dependency/cologne8_colight_original_seed7_global_dg/influence_heatmap.png)
- [Ingolstadt21 learned-dependency heatmap](outputs/model_dependency/ing21_colight_original_seed7_gpu2_refire_dg/influence_heatmap.png)
- [Cologne8 hop-influence figure](outputs/model_dependency/cologne8_colight_original_seed7_global_dg/hop_influence.png)
- [Ingolstadt21 hop-influence figure](outputs/model_dependency/ing21_colight_original_seed7_gpu2_refire_dg/hop_influence.png)
- [Downstream run summary](outputs/results/result_summary.csv)
