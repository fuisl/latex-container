# Theory Direction 2: The Dependency Regime — a Measurable Spatio-Temporal Field, Coarse-Grained by the Map Equation Family

**Date:** 2026-07-06 · **Status:** proposed direction (companion/alternative to `THEORY_DIRECTION_2026-07-06.md`)
**Relation to Direction 1:** Direction 1 makes *retention under a static partition* the primitive and derives bounds downward to MARL. Direction 2 makes the **dependency field itself** the primitive — directed, lag-resolved, regime-conditioned — and asks which flow representation the map equation must run on so that its modules coincide with the space-time modular structure of that field. Direction 1 answers "why does a static flow partition help"; Direction 2 answers "when is a static partition the wrong object, what replaces it, and what law governs the difference." They are complementary; either can stand alone as a proposal.

---

## 0. The core idea

The manuscript's §Spatio-Temporal Dependency Decomposition already names three separate things: spatial dependency, temporal (self-history) dependency, and OD temporal variability. Direction 2 unifies them into **one measurable object**:

```
D_ij(τ | ρ)   —   directed dependency from i to j at lag τ, conditioned on traffic regime ρ
```

with three claims about its structure, each grounded in existing literature and each generating a falsifiable prediction:

1. **It has a cone (spatio-temporal locality).** Dependency propagates at finite speed — forward along flow at ~free-flow speed, backward against flow at the kinematic-wave speed — so D_ij(τ) peaks at a physically predicted lag τ*(i,j) ≈ d_ij / c(ρ), and the dominant direction flips with regime.
2. **It has regimes (piecewise stationarity).** Traffic networks occupy discrete macroscopic states (free-flow / congested; percolation phases), and the dependency structure is approximately stationary within a regime and switches across regimes.
3. **The map equation family is its MDL-optimal coarse-grainer** — provided the flow representation matches the field's order: first-order walk ↔ static aggregate dependency (Direction 1's regime); memory/higher-order walk ↔ path-dependent routing; multilayer/temporal walk ↔ regime switching. The forward/backward two-channel structure of traffic dependency has an exact counterpart in flow-stability's forward/backward random-walk processes.

The MARL payoff: **regime-switching coordination structure** — the T0–T5 temporal ablation already planned in `RESEARCH_PLAN.md` §7.2 stops being an ablation and becomes the centerpiece, with a quantitative law predicting *when* dynamic partitioning beats static.

---

## 1. Pillar A — The dependency cone: lag-resolved, directed instruments

**Replace lagged MI with lag-specific transfer entropy (TE).** The H1 instrument `I(X_i(t); X_j(t+τ))` has two known confounds that plausibly *caused* the H1 statistical failure:
- **self-memory:** each node's autocorrelation inflates pairwise lagged MI regardless of interaction;
- **common demand:** network-wide demand fluctuations create MI between non-interacting nodes (Direction 1 §2's confounder; grows with network size — consistent with the C8→I21 collapse of the MI gap, 0.190 → 0.007–0.017).

TE_{i→j}(τ) = I(X_i(t); X_j(t+τ) | past of X_j) removes the first confound by construction and is **directed** — it distinguishes the forward (arrival) channel from the backward (spill-back) channel, which symmetric MI cannot do. Lag-specific TE is established methodology for estimating congestion-propagation delays in urban networks ([arXiv:2108.06717](https://arxiv.org/pdf/2108.06717)). Conditioning on an aggregate-demand covariate (Direction 1's fix) handles the second confound.

**The cone prediction (traffic physics → information theory).** Kinematic-wave/CTM theory fixes propagation speeds: disturbances travel downstream at ~free-flow speed in the uncongested branch and upstream at the backward-wave speed in the congested branch. Therefore:

```
τ*_{i→j}(ρ)  =  d_ij / c(ρ),    with  c(free-flow) = v_f (forward),  c(congested) = |w| (backward)
```

- TE_{i→j}(τ) should be maximal near τ* and near zero far outside the cone;
- in free flow, TE along flow direction dominates; in congestion, TE against flow direction (upstream) dominates;
- **test statistic concentration:** evaluating dependency *at the predicted lag* τ*(i,j) instead of averaging over τ ∈ {1,5,15,30} concentrates the effect instead of diluting it — a direct statistical-power fix for the H1-style tests.

This yields the **directed, lag-resolved retention** ratio as the new central metric:

```
Ψ_TE(P; τ, ρ) = Σ_{c(i)=c(j)} TE_{i→j}(τ | ρ) / Σ_{i≠j} TE_{i→j}(τ | ρ)
```

a strict generalization of Ψ(P, D_MI): recovering it when TE is symmetrized, lag-averaged, and regime-pooled — which makes "why did H1 fail" answerable *within the new framework* (pooling destroyed the structure).

---

## 2. Pillar B — Regimes are real, detectable, and few

**Percolation evidence.** Traffic networks exhibit a percolation transition in the functional (speed-thresholded) network with evolving critical bottlenecks ([Li et al., PNAS 2015 line of work](https://arxiv.org/pdf/1512.00182); [computational cluster dynamics](https://arxiv.org/pdf/2408.08122)). Sharper: **the same road network switches between two distinct critical percolation modes** — non-rush hours behave like a small-world network, rush hours like a 2D lattice ([arXiv:1709.03134](https://arxiv.org/pdf/1709.03134)) — i.e., the *universality class* of connectivity changes with regime, not just parameters. Congestion spreading also shows multistability and hysteresis ([arXiv:2507.06659](https://arxiv.org/pdf/2507.06659)), so regime is a genuine state variable, not a smooth covariate.

**Operationalization.** Define the regime variable ρ(t) from network state: MFD position (density/flow), or percolation state of the speed-thresholded functional graph (giant-component size / critical threshold q_c(t)). Both computable from SUMO output directly.

**Hypothesis D1 (piecewise stationarity of dependency).** D_ij(τ | ρ) is approximately stationary within a regime and differs across regimes — specifically, the backward channel's TE mass is near zero in free flow and dominant near saturation (this *contains* the observed H2 outcome: Cologne8's zero spill-back events = the network never left the free-flow regime, so the backward channel was never active; not a failed test but a measured regime label).

Existing anchors in the manuscript already point here: `flowstability2022` ("communities stable within a regime, differ across regimes") and `lucchini2023intraod` (82.9% membership stability, boundary nodes shift) — currently used as *defensive* citations for the static-partition assumption; Direction 2 turns them into the *object of study*.

---

## 3. Pillar C — The map equation family as the matching coarse-grainer

The map-equation ecosystem has a representation for each structural feature of the dependency field — this is what makes InfoMap (rather than generic clustering) the natural spine of the proposal:

| Dependency-field feature | Flow representation | Map-equation variant | Key source |
|---|---|---|---|
| Static aggregate coupling | first-order OD walk | classic two-level map equation | Rosvall & Bergstrom 2008 (already cited) |
| Path-dependent routing (temporal correlation of the *flow process*) | second-/variable-order memory network on trip paths | memory map equation; sparse memory networks | [Rosvall et al., Nat. Comms 2014 (arXiv:1305.4807)](https://arxiv.org/pdf/1305.4807); [arXiv:1606.08328](https://arxiv.org/pdf/1606.08328); [Infomap higher-order (arXiv:1706.04792)](https://arxiv.org/pdf/1706.04792) |
| Regime switching / time-sliced structure | multilayer network, layers = time slices, interlayer relax | multilayer map equation | [De Domenico et al., PRX 2015](https://link.aps.org/doi/10.1103/PhysRevX.5.011027); [intermittent communities (arXiv:1711.07649)](https://arxiv.org/pdf/1711.07649) |
| Forward vs backward channels | forward + time-reversed random walks on the temporal network | **flow stability** (clusters covariance of forward and backward processes) | [Bovet, Delvenne, Lambiotte, Sci. Adv. 2022] (already cited as `flowstability2022`) |

**Two linking observations worth making explicit in the proposal (both, to our knowledge, unexploited):**

1. **Flow stability's forward/backward construction is the exact community-detection counterpart of traffic's two dependency channels.** Flow stability clusters a forward-in-time diffusion *and* a backward-in-time diffusion on the temporal network; traffic dependency propagates forward via routed arrivals and backward via spill-back. So the method-pair (forward walk ↔ arrival channel, backward walk ↔ blocking channel) is not an analogy but a structural match — the backward random walk on the time-reversed flow graph is precisely the propagation medium of spill-back. This gives the proposal a distinctive, citable theoretical hook.
2. **SUMO provides complete vehicle trajectories, so higher-order path statistics are *observed, not inferred*.** The usual obstacle to memory networks — exponential data requirements for fitting higher-order models ([PMC4814833](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4814833/)) — largely vanishes in simulation: every trip's full intersection sequence is logged. The pipeline already builds W from these sequences (`main.tex` OD construction); upgrading to second-order state nodes is an incremental change to the same extraction code. This is a practical advantage most empirical memory-network studies don't have.

**Theory target (the "fundamental claim" of Direction 2).** A codelength–dependency correspondence: modules that compress the (appropriately-ordered) walk are modules that concentrate directed dependency. Concretely, aim for a proposition of the form

```
within-module TE mass under partition P  ≥  g( L_full − L(P) )
```

i.e., the codelength saving of a partition lower-bounds (a function of) its directed-dependency retention, per regime — with the *order* of the walk model controlling which lags τ the bound covers (first-order: one-step; k-th order: k-step cone). The proof route mirrors Direction 1's Prop 2 (coupling bounded by flow, data-processing along paths), but now per-regime and per-direction, using the time-reversed walk for the backward channel. Even the honest partial version ("under assumptions A1–A3, per-step directed coupling is bounded by the regime-conditioned edge flow, hence cut TE mass is bounded by cut flow *of that regime's* graph") is a publishable formalization — and it fails visibly (measurably) when the regime is pooled, which *explains the H1 failure as a theorem-shaped statement about mixtures*.

---

## 4. The MARL program: regime-switching coordination

**Reframe T0–T5 (RESEARCH_PLAN §7.2) from ablation to main experiment.** Conditions already planned: no-partition · METIS · InfoMap off-peak · peak · 24h · dynamic re-partition. Add the regime-*indexed* condition: partitions per detected regime, switched online at regime boundaries (hysteresis-aware, per Pillar B).

**Hypotheses:**
- **D2 (regime-matched benefit):** regional MARL with regime-matched partitions ≥ single static partition, with equality when regimes' partitions coincide — the Lucchini 82.9% figure predicts *small* gains on networks whose regimes share structure, so the honest prediction is conditional, not universal.
- **D3 (the quantitative law — the distinctive claim):** the dynamic-over-static gain scales with the inter-regime partition distance:
  ```
  ΔJ(dynamic − static)  ∝  VI(P_peak, P_offpeak)   (variation of information)
  ```
  or equivalently with the regime-conditioned retention gap ΔΨ_TE. Networks/demand profiles whose regimes differ more benefit more. This turns "does dynamic partitioning help?" (yes/no, easily confounded) into a *dose–response* prediction testable across networks and synthetic demand schedules (FGS-Synthetic can generate controlled regime contrast — a concrete use for the FGS scalability track).
- **D4 (mechanism):** cold-start instability at partition switches is the L1 lesson replayed — apply the existing α-annealing at each switch; predicted to matter at L1, not L2 (per Direction 1's per-level reading).

**Relation to learned dynamic-grouping MARL** ([GACG, IJCAI 2024 (arXiv:2404.10976)](https://arxiv.org/abs/2404.10976); [deep meta coordination graphs (arXiv:2502.04028)](https://arxiv.org/html/2502.04028v3); VAST): those learn time-varying groups end-to-end, inheriting nonstationarity and opacity. The proposal's position is deliberately different: **the switching signal is a measured physical regime variable and the partitions are precomputed map-equation optima** — cheap, interpretable, and the theory (Pillar C) says *what* the groups should be rather than hoping attention discovers it. Cite these as the learned-alternative baseline family, and (budget permitting) include one as a comparison condition.

---

## 5. Measurement plan (deltas over what already exists)

| # | New measurement | Builds on | Cost |
|---|---|---|---|
| 1 | TE tensor TE_{i→j}(τ | ρ) on SUMO traces; lag grid resolved enough to see the cone (Δτ ≈ 5–15 s) | existing KSG/state-diagnostics pipeline (analysis repo) | moderate: TE estimator (KSG-style or discretized) + regime labels |
| 2 | Regime detection: MFD position + percolation q_c(t) per time slice | SUMO edge speeds | low |
| 3 | Cone check: TE peak lag vs d_ij/c(ρ) regression, per regime and direction | #1, #2 | low, headline figure |
| 4 | Ψ_TE(P; τ, ρ) for {InfoMap static, per-regime InfoMap, METIS, memory-InfoMap, multilayer/flow-stability} | #1 + Infomap variants (all open-source at mapequation.org) | low–moderate |
| 5 | Memory Infomap on second-order trip paths; compare modules vs first-order (overlap, VI) | existing trip-sequence extraction | low |
| 6 | T0–T5 + regime-indexed MARL runs; D2/D3 regression across nets/demand schedules | planned T-ablation infra | high (the main compute item) |

Note the front-loading: #1–#5 need **no MARL training at all** — the dependency-field characterization stands alone as a paper-sized empirical contribution even before the MARL experiments run (parallel to how Φ/Ψ carried Direction 1).

## 6. Risks / honest limits

- **TE estimation is data-hungry and biased at small samples**; per-regime conditioning shrinks samples further. Mitigations: SUMO traces are extendable at will (simulation, not field data); discretized/binned TE with permutation nulls; report effect sizes with surrogate-data significance (time-shifted surrogates standard in the TE literature).
- **Small networks may be regime-degenerate** — C8 apparently never leaves free flow (zero spill-backs). Then Direction 2's predictions are *vacuously* satisfied there (no regime contrast → static suffices → matches observed data). I21 and FGS-Synthetic with stressed demand are where the contrast must come from; a stressed-demand C8 variant is a cheap add.
- **Dynamic re-partitioning injects nonstationarity into MARL** — known cold-start failure mode from L1. D4/annealing addresses it, but a negative result at L1 is plausible; L2 (MAPPO) is the safest level for the D2/D3 tests, consistent with all existing evidence.
- **Memory Infomap may fragment modules** (higher-order structure often yields more, overlapping modules) — overlapping modules don't map cleanly onto disjoint MARL regions. Fallback: use memory-Infomap as *diagnostic* (does routing memory change the boundaries?) while keeping first-order partitions for control; overlap itself is informative (boundary agents ↔ Lucchini's shifting peripheral nodes).
- **Flow stability at scale**: covariance clustering is O(N²) in state nodes over time — fine at N=8–21 intersections, check before FGS scaling.

## 7. How the two directions fit together (if ever merged)

Direction 1: static bounds — map equation ⇒ Φ ⇒ Ψ ⇒ value loss, per regime.
Direction 2: identifies the regime decomposition within which Direction 1's bounds hold, quantifies the cross-regime nonstationarity that violates them, and supplies the switching policy that restores them.
One-sentence merged thesis: *the map equation family, applied at the order and time-resolution of the traffic dependency field, yields coordination structures whose retention bounds regional-MARL value loss regime-by-regime.*

## 8. Verified sources (this session)

- Memory/higher-order map equation: [Rosvall et al., Nat. Comms 2014 (arXiv:1305.4807)](https://arxiv.org/pdf/1305.4807) · [sparse memory networks (arXiv:1606.08328)](https://arxiv.org/pdf/1606.08328) · [Infomap for higher-order flows (arXiv:1706.04792)](https://arxiv.org/pdf/1706.04792) · [higher-order models reveal flow communities (PMC4814833)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4814833/)
- Multilayer/temporal map equation: [De Domenico et al., PRX 2015](https://link.aps.org/doi/10.1103/PhysRevX.5.011027) ([arXiv:1408.2925](https://arxiv.org/pdf/1408.2925)) · [intermittent communities in temporal networks (arXiv:1711.07649)](https://arxiv.org/pdf/1711.07649) · [mapequation.org publications](https://www.mapequation.org/publications.html)
- Flow stability: Bovet, Delvenne & Lambiotte, Science Advances 8(19), 2022 (already `flowstability2022` in refs.bib; forward/backward covariance construction confirmed via search this session)
- Lag-specific transfer entropy for congestion propagation delays: [arXiv:2108.06717](https://arxiv.org/pdf/2108.06717)
- Traffic percolation regimes: [percolation in a traffic model (arXiv:1512.00182)](https://arxiv.org/pdf/1512.00182) · [switch between critical percolation modes (arXiv:1709.03134)](https://arxiv.org/pdf/1709.03134) · [multistability & hysteresis in congestion spreading (arXiv:2507.06659)](https://arxiv.org/pdf/2507.06659) · [percolation-based traffic cluster dynamics (arXiv:2408.08122)](https://arxiv.org/pdf/2408.08122)
- Learned dynamic coordination baselines: [GACG (arXiv:2404.10976)](https://arxiv.org/abs/2404.10976) · [deep meta coordination graphs (arXiv:2502.04028)](https://arxiv.org/html/2502.04028v3)
- (Li & Havlin PNAS 2015 "percolation transition in dynamical traffic network" — located via secondary sources above; pull the primary DOI before adding to refs.bib.)
