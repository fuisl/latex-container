# Report Plan — Causal Pipeline: Metrics, Formulas, Literature, Computed Evidence

**Purpose:** outline for today's presentation/report. This is presentation-facing (narrative, selected numbers) — the full raw detail lives in `ANALYSIS_PLAN.md`, `MANUSCRIPT_RESULTS_LOG.md`, `RUN_LOG_2026-07-02.md`, `L2_CRITIC_DIAGNOSTIC_DESIGN.md`; pull from those if asked for more than what's here.

**Framing for the talk:** the whole argument is a five-stage causal chain. Each stage below states the claim, the metric that tests it, the formula and what it means, the literature that grounds the choice of metric, and — critically — what's already been computed. Stages 2, 3, and 4 are where this paper's actual evidence lives and get full treatment; stages 1 and 5 are brief because the literature already establishes them and the paper isn't re-proving them from scratch.

```
1. InfoMap preserves flow  ⇒  2. Flow preserved → dependency preserved  ⇒  3. Dependency retention → coordination quality  ⇒  4. Coordination quality → RL learning quality  ⇒  5. Better RL → better TSC outcome
     (literature)                    (H1, H2, ρ(W,D))                        (Ψ, per-level instruments)                         (AUC-LC, ET, Late-σ, ΔΨ-vs-Δperf)                    (ATT / waiting time)
```

---

## Stage 1 — InfoMap preserves flow *(brief — literature-established)*

**Claim:** InfoMap retains more within-module OD flow than a topology-based partition (METIS).

**Metric:** Φ(P,W) — flow retention ratio.
```
Φ(P, W) = Σ_k Σ_{i,j∈M_k} W_ij  /  Σ_{i,j} W_ij
```
Fraction of total OD flow volume that stays within partition modules. This is close to definitional — InfoMap's whole objective is minimizing the description length of a random walk on the flow graph, which is mathematically equivalent to maximizing within-module flow retention.

**Literature:** the map equation itself guarantees this (Rosvall & Bergstrom 2008, `rosvall2008maps`; Rosvall, Axelsson & Bergstrom 2009, `rosvall2009mapequation`) — minimizing description length L(M) directly maximizes within-module random-walk (flow) retention. Empirically confirmed on real urban OD networks by Lucchini et al. 2023 (`lucchini2023intraod`): 82.9% of regions maintain stable community membership across time windows.

**Already computed:** yes, both networks, both k — InfoMap wins at every point (C8 k3: 0.939 vs 0.614; k5: 0.569 vs 0.415; I21 k4: 0.817 vs 0.643; k5: 0.792 vs 0.636). Not a research question in itself — it's the necessary first link, and the paper's real contribution starts at Stage 2.

---

## Stage 2 — Flow preserved → dependency preserved

**Claim:** pairs of intersections with high OD flow between them are also the pairs with high *inter-agent dependency* — i.e., flow is a good proxy for the thing that actually matters for coordination (shared future state, spillback coupling), not just a graph-theoretic artifact.

This is the stage that needs the most methodological grounding, because it's where the paper switches from "flow" (an observable, physical quantity) to "dependency" (a statistical/causal quantity that has to be *estimated*). Two complementary tests:

### 2.1 H1 — Spatial Mutual Information Advantage

**Claim:** within-module agent pairs share higher mutual information about future traffic states than cross-module pairs.
```
E[I(X_i(t); X_j(t+τ))]_{i,j∈M_k}  >  E[I(X_i(t); X_l(t+τ))]_{i∈M_k, l∉M_k}
```
averaged over propagation lags τ ∈ {1, 5, 15, 30} steps.

### Introduction to Mutual Information

Mutual information between two random variables X and Y:
```
I(X;Y) = ∫∫ p(x,y) log( p(x,y) / (p(x) p(y)) ) dx dy
```
**Interpretation:** how much knowing X reduces uncertainty about Y (and vice versa — MI is symmetric). I(X;Y) = 0 if and only if X and Y are statistically independent. Unlike Pearson correlation, MI captures **nonlinear** dependence — important here because traffic dependency (e.g., how a downstream queue's growth affects an upstream intersection's future state via backward-propagating spillback) is not expected to be linear.

**Why not just correlate raw traffic signals directly?** Correlation only detects linear association; spillback dynamics are threshold-like and nonlinear (queue effects only propagate once a lane saturates). MI is the natural information-theoretic quantity for "how predictive is agent i's current state of agent j's future state," which is exactly the question H1 asks.

### The estimator — KSG (Kraskov–Stögbauer–Grassberger)

MI is hard to estimate directly from finite continuous-valued samples. Naive histogram-binning approaches suffer from the curse of dimensionality and are sensitive to bin-width choice (systematic bias). The KSG estimator (Kraskov, Stögbauer & Grassberger 2004, `kraskov2004ksg`) instead uses a **k-nearest-neighbor** approach:

```
Î(X;Y) = ψ(k) − ⟨ψ(n_x+1) + ψ(n_y+1)⟩ + ψ(N)
```
where `ψ` is the digamma function, `k` is the number of nearest neighbors used (a tunable parameter, typically small, e.g. 3–5), `n_x`/`n_y` are the counts of points within the k-th-neighbor distance projected onto each marginal, and `N` is the sample size. The key idea: for each sample point, find the distance to its k-th nearest neighbor in the **joint** (X,Y) space, then count how many neighbors fall within that same distance in each **marginal** space — this adapts the local density estimate to wherever the data actually is, rather than imposing a fixed grid. This is why it's the standard choice for MI estimation on continuous, non-uniformly-distributed data (exactly the shape of traffic state distributions), and is widely used across physics, neuroscience, and ML for this reason.

**Verification protocol:** classify agent pairs as within-module or cross-module under the candidate partition; compare the two MI distributions via a Wilcoxon signed-rank test (p < 0.05).

**What the test does, and why it's the right tool here.** For each agent i, H1 compares that *same* agent's average MI to its within-module neighbors against its average MI to its cross-module neighbors — a natural per-agent pair (N=8 or N=21 pairs, one per agent). The Wilcoxon signed-rank test ranks the absolute per-agent differences, reattaches their sign, and asks whether the positive-signed ranks dominate enough to reject "no systematic difference." It's non-parametric (no normality assumption on the MI estimates, only rough symmetry of the differences) and paired (controls for agent-level heterogeneity — some intersections are just more central/higher-traffic than others — by comparing each agent against itself, not pooling raw within- vs. cross-module values). *(Pairing structure inferred from H1's mathematical form in §3.3 of the manuscript, not yet confirmed against the actual analysis code.)*

**Why this matters for reading the results below:** the test is sensitive to *consistency* of the sign across agents, not the size of the average gap — which is why average gap alone doesn't predict pass/fail (see flow_k5 anomaly below), and why small-N settings (21 agents, or fewer with both within/cross neighbors) have limited power even when the direction is consistently correct.

**Current H1 results, full breakdown (3 seeds per condition):**

| Network | Partition | k | Mean within-MI | Mean cross-MI | Gap | Pass count (of 3 seeds) |
|---|---|---|---|---|---|---|
| Cologne8 | flow | 3 | 0.5415 | 0.3510 | 0.190 | **3/3** ✓ |
| Cologne8 | metis | 3 | 0.5369 | 0.4251 | 0.112 | 0/3 |
| Cologne8 | flow | 5 | 0.5929 | 0.4149 | 0.178 | 0/3 |
| Cologne8 | metis | 5 | 0.5340 | 0.4434 | 0.091 | 0/3 |
| Ingolstadt21 (full-state) | flow | 4 | 0.5058 | 0.4986 | 0.0072 | 1/3 |
| Ingolstadt21 (full-state) | metis | 4 | 0.5095 | 0.4979 | 0.0117 | 1/3 |
| Ingolstadt21 (full-state) | flow | 5 | 0.5134 | 0.4968 | 0.0166 | 2/3 |
| Ingolstadt21 (full-state) | metis | 5 | 0.5147 | 0.4976 | 0.0171 | 2/3 |

Only Cologne8 flow_k3 passes cleanly. Flow_k5's near-identical gap to flow_k3 (0.178 vs. 0.190) but 0/3 pass rate is the clearest illustration of the point above — the test is failing on per-agent consistency, not on the size of the average effect. Ingolstadt21 improved after switching to full-state MI (no more direction reversals — the earlier `queue_total` proxy had metis_k4/k5 showing cross-MI exceeding within-MI), but effect sizes are an order of magnitude smaller than Cologne8's and pass rate tops out at 2/3, consistent with a small, real, but underpowered effect at this network size.

### 2.2 H2 — Spill-back Containment

**Claim:** spill-back congestion is more likely to stay within a module than cross module boundaries.
```
Pr(spillback_{i→j} | i,j∈M_k)  >  Pr(spillback_{i→l} | i∈M_k, l∉M_k)
```
**Literature:** Zhang et al. 2025 (`dependencydyn2025`) establish that inter-agent coordination is necessary *if and only if* spill-back connects two agents' queues — this is the traffic-theoretic mechanism that H1's MI advantage is hypothesized to arise from. Newly added this session: Tassiulas & Ephremides 1992 (`tassiulas1992stability`, constrained-queueing Lyapunov drift) and Varaiya 2013 (`varaiya2013maxpressure`, max-pressure signal control) — grounding *why* containment matters formally, not just empirically: a decentralized controller only preserves the stability guarantees of a centralized one if it can react to the joint state of *dynamically coupled* queues, so cutting a coordination-graph edge is only "safe" where spillback across it is rare.

**Verification protocol:** extract spillback events from SUMO queue trajectories; one-sample proportion test, within-module vs. cross-module rate.

### 2.3 ρ(W, D) — Flow–Dependency Alignment

**Claim:** flow volume and dependency (MI or Jacobian-based) are positively correlated at the pair level — a direct, partition-agnostic test of "does flow predict dependency," independent of any partition choice.
```
ρ(W, D) = Spearman rank correlation( {W_ij}, {D_ij} )
```
Standard nonparametric monotonic-association test — no special methodological grounding needed beyond that, but it's cheap and directly answers Stage 2's claim without going through a partition at all.

### Already computed — Stage 2

| Instrument | Network | k | Result | Status |
|---|---|---|---|---|
| H1 | both | 3, 4, 5 | see full per-condition breakdown in §2.1 above | Marginal on C8 (1/4 conditions pass), weak-but-directionally-correct on I21 (1–2/3 seeds) |
| H2 | Cologne8 | all | **0 events detected, all conditions** | Untestable with current data |
| H2 | Ingolstadt21 | all | sparse, nonzero, underpowered | Needs longer/stress traces |
| ρ(W, D_MI) | Cologne8 | — | **0.514** | Strong, real correlation |
| ρ(W, D_MI) | Ingolstadt21 (full-state) | — | **0.141** | Weak but present; much smaller than C8 — scale-dependence worth a sentence |
| ρ(W, D_G) | Ingolstadt21 | — | 0.750 (p=4e-77, n=420) | Strong |
| ρ(W, D_G) | Cologne8 | — | 0.796 (p=2e-13) | Strong — D_G notably more scale-robust than D_MI across networks |

**Honest read for the talk:** Stage 2 is empirically the weakest link in the chain right now. The correlation test (ρ) is solid on both instruments; the formal hypothesis tests (H1, H2) are not yet robust. This should be stated plainly, not glossed over — it's exactly the kind of thing a careful audience will probe.

---

## Stage 3 — Dependency retention → coordination quality

**Claim:** a partition that retains more inter-agent dependency produces better-structured coordination — correlated rewards for L1, dependency-aligned critic input for L2, attention concentrated within-module for L3.

**Core metric — dependency retention ratio Ψ:**
```
Ψ(P, D) = Σ_k Σ_{i,j∈P_k} D_ij  /  Σ_{i,j} D_ij
```
Same structural form as Φ(P,W) (Stage 1), but computed on a *dependency* matrix D instead of a raw flow matrix W. Ψ ∈ [0,1]: the fraction of total inter-agent dependency captured within module boundaries. High Ψ means the partition cuts mostly low-dependency edges (preserving coordination capacity); low Ψ means high-dependency edges are severed (imposing coordination cost). **Same instrument, three different D matrices — one per coordination level:**

### 3.1 L1/L2 shared instrument — D^MI (already defined in Stage 2)

Model-free; used directly since IPPO has no cross-agent input path in the policy network (making Jacobian-based measures structurally inapplicable at L1), and reused as a level-agnostic baseline for L2.

### 3.2 L3 instrument — D^G (Jacobian-based)

```
D_{i←j}(F) = Σ_{a,k} | ∂F_{i,a} / ∂X_{j,k} |
```
Aggregated absolute Jacobian of the model's output at agent i with respect to agent j's input features — "how much does perturbing what agent j sees change what agent i's model outputs." Computed on the **global** (unpartitioned) CoLight GAT only — a partitioned model has cross-module inputs structurally absent, making its cross-module Jacobian zero by construction, a structural artefact rather than evidence of low dependency (this exact trap was caught and avoided this session, see §"Caught and fixed" below).

**Literature:** adapted from Lin, Deng et al. (`lrd2025`), who use the same aggregated-Jacobian construction to diagnose GNN over-squashing (whether a GNN can propagate information across long ranges). Here it's repurposed to ask a different question: does a proposed *partition* align with what the model has already learned to depend on.

### 3.3 L2 instrument, reduced — g_j and Γ(P,g) *(new this session, design finalized, implementation pending)*

The paper's originally-planned D^Q (same Jacobian construction as D^G, but on the global MAPPO critic) turned out to be architecturally unavailable — confirmed via code read that MAPPO's global critic feeds every output row an identical input, so there is no per-target-agent index to differentiate against. Reduced, honestly-scoped alternative:
```
g_j = Σ_k |∂V/∂X_{j,k}|                              (source-sensitivity vector, no target index)
Γ(P,g) = − Σ_k p_k log p_k,   p_k = Σ_{j∈M_k} g_j / Σ_j g_j     (Shannon entropy of module-mass concentration)
```
**Not called Ψ or D_Q** — it has no pairwise structure, so it cannot test "is dependency preserved within modules," only "does the partition group the agents the critic is most sensitive to together." A narrower, different, but still meaningful claim.

**Literature:** gradient-based attribution grounding — Simonyan, Vedaldi & Zisserman 2013 (`simonyan2013saliency`), Sundararajan, Taly & Yan 2017 (`sundararajan2017axiomatic`, also the source of the gradient-saturation caveat that applies to the whole Jacobian-instrument family, D^G included). Entropy-as-concentration-diagnostic grounding, directly on-topic: Yu, Qiu, Wang, Zhang & Wang 2023, "Low Entropy Communication in Multi-Agent Reinforcement Learning" (`yu2023lowentropymarl`) — entropy used as the design/diagnostic quantity for MARL communication concentration, the same subfield this paper is in. Full spec: `L2_CRITIC_DIAGNOSTIC_DESIGN.md`.

### Already computed — Stage 3

| Instrument | Network | k | Ψ_flow | Ψ_metis | Direction |
|---|---|---|---|---|---|
| Ψ(D_MI) | Cologne8 | 3 | 0.640 | 0.296 | ✓ flow wins |
| Ψ(D_MI) | Cologne8 | 5 | 0.280 | 0.126 | ✓ flow wins |
| Ψ(D_MI) | Ingolstadt21 | 4 | 0.2455 | 0.2181 | ✓ flow wins |
| Ψ(D_MI) | Ingolstadt21 | 5 | 0.2199 | 0.1665 | ✓ flow wins |
| Ψ(D_G) | Cologne8 | 3 | 0.754 | 0.591 | ✓ flow wins |
| Ψ(D_G) | Cologne8 | 5 | 0.370 | 0.476 | **✗ reverses** |
| Ψ(D_G) | Ingolstadt21 | 4 | 0.798 | 0.669 | ✓ flow wins |
| Ψ(D_G) | Ingolstadt21 | 5 | 0.700 | 0.731 | **✗ reverses** |
| Γ(P,g) | both | — | not yet computed | — | implementation pending |

**Headline finding to lead the talk with:** the Ψ(D_G) reversal at larger k **replicated independently on both networks** — small k favors flow, large k favors METIS, on both C8 and I21, while Φ(P,W) favors flow at every k on both. This is real, not noise, and gives the existing "L3 module-size saturation" hypothesis a quantitative signature instead of a qualitative conjecture.

---

## Stage 4 — Coordination quality → RL learning quality

**Claim:** better-structured coordination (higher Ψ) improves sample efficiency and training stability, not just final performance.

**Metrics:**
```
AUC-LC = ∫₀ᴺ ATT(e) de     (trapezoidal rule; lower = less cumulative delay incurred while learning = faster learning)
ET(≤t) = first episode e such that ATT(e) ≤ t     (episodes-to-threshold; convergence speed)
Late-σ = std( ATT(e) )  over the final training window     (stability of the converged policy)
```

**The actual Stage-4 test:** scatter of ΔΨ (InfoMap − METIS) vs. Δperformance (e.g., ΔAUC-LC) per (algorithm, network, k) condition — a positive correlation is what closes the "dependency retention → learning quality" link empirically (this is `ANALYSIS_PLAN.md` Tier 1 #4).

**Literature:** Henderson et al. 2018 (`henderson2018matters`) — single-seed, final-episode comparisons are unreliable in deep RL, motivating the use of full learning-curve metrics (AUC-LC, ET, Late-σ) rather than a single final number. Agarwal et al. 2021 (`agarwal2021rliable`) — the rliable protocol (IQM, stratified bootstrap CI, performance profiles) as the rigorous way to aggregate across seeds; adopted as the target statistical standard once multi-seed data exists. ExpoComm (`expocomm2025`) — general precedent that pre-designed structural communication topologies improve MARL sample efficiency, motivating the expectation that coordination-graph *quality* (not just its existence) should measurably affect learning speed.

### Already computed — Stage 4

Sample-efficiency numbers exist from the original single-seed pilot (Cologne8, e.g. IPPO/MAPPO AUC-LC and Late-σ values), but **the actual ΔΨ-vs-Δperformance test (Tier 1 #4) has not been run yet** — it's blocked on Stage 3's instruments and Stage 5's multi-seed performance data both being finished cleanly first.

**One important open data point already found, worth flagging honestly in the talk:** the Ψ(D_G) k=5 reversal (Stage 3) does **not** cleanly predict the one real trained-model comparison available — Ingolstadt21 CoLight Variant B at k=5 still shows flow *winning* on actual wait-time performance (629.34 vs. 656.28, flow better by ~4%), the opposite direction from what the diagnostic predicts. This is either a genuine gap between the global-model diagnostic and what a regionally-trained model learns, or single-seed noise on a small margin — undetermined with current data, and exactly the kind of tension Stage 4 exists to resolve once more data is in.

---

## Stage 5 — Better RL → better TSC outcome *(brief — the measured outcome itself, not a separate claim needing literature support)*

**Metric:** final ATT / average waiting time / queue length — standard MARL-TSC evaluation convention, measured rigorously via the rliable protocol above (Henderson 2018, Agarwal 2021).

**Already computed (existing single-seed pilot):**

| Network | Algorithm | Condition | Result |
|---|---|---|---|
| Ingolstadt21 | MAPPO | flow_k4 vs metis_k4 | 140.96 vs 401.17 (**2.85×**) |
| Ingolstadt21 | MAPPO | flow_k5 vs metis_k5 | 160.51 vs 640.82 (**3.99×**) |
| Ingolstadt21 | IPPO | flow_k5 vs metis_k5 | 202.71 vs 526.10 (**2.60×**) |
| Cologne8 | IPPO / MAPPO | flow vs metis vs baseline | flow best in both, modest margin over METIS for MAPPO |
| Cologne8 | CoLight | flow vs metis vs baseline | flow **diverges** (+73%), METIS ≈ neutral |
| Ingolstadt21 | CoLight (Variant A, incomplete) | flow vs metis vs baseline | flow ahead so far (365.26 vs 702.45 vs 591.26) |

MAPPO's 2.85–3.99× is the strongest single number in the paper — lead the results section with it, while being upfront it's still single-seed.

---

## Methodology discipline (worth its own slide, makes the numbers trustworthy)

1. **Same dependency object, partitions applied post-hoc** — compute each instrument once from the unconstrained/global model, then overlay both partitions on that same matrix. Never compute separately per partition-trained checkpoint.
2. **Same-k comparisons only.**
3. **Two networks, different roles** — Cologne8 is the fast-iteration/pipeline-validation network; Ingolstadt21 is where the headline numbers come from.
4. **Every new metric gets a literature-grounded definition before implementation**, not after (Stage 3's Γ diagnostic, this session).

**Caught and fixed this session:** an early attempt to compute D_G directly from partition-trained CoLight checkpoints would have produced a structural-zero artefact (or, on Cologne8, was architecturally impossible — those checkpoints turned out to be a different model class, `CoLightRegional`, with no unified computational graph at all). Caught via a WandB config check before it corrupted any result.

---

## Honest limitations to state proactively

1. **Stage 2 is the weakest link.** H1 passes 1/8 conditions cleanly on Cologne8, is directionally-correct-but-marginal on Ingolstadt21 (1–2/3 seeds). H2 has zero detected events on Cologne8, sparse on Ingolstadt21.
2. **Stage 3→4 has one open contradiction**, not yet resolved (Ingolstadt21 CoLight k=5).
3. **D^Q, as originally scoped, is architecturally unavailable** — reduced diagnostic designed, not yet implemented.
4. **CoLight's regional mechanism differs across networks** as currently trained — needs an Appendix correction.
5. **Two networks, mostly single-seed** — breadth and statistical rigor both still in progress.

---

## Immediate next steps

1. Implement the Γ(P,g) diagnostic (`L2_CRITIC_DIAGNOSTIC_DESIGN.md`).
2. Cologne8 CoLight at k=5 — cheap test of whether the Stage 3 reversal predicts a real Stage 4/5 performance reversal anywhere.
3. Resolve H2 event sparsity; decide how Stage 2 gets honestly framed in the manuscript.
4. Finish Ingolstadt21 CoLight refires + normalization; multi-seed expansion for rliable statistics (Stage 4/5).
5. Correct the Appendix's CoLight architecture description.

---

## Appendix (for the talk, not necessarily shown) — full documentation trail

| Doc | Contains |
|---|---|
| `ANALYSIS_PLAN.md` | Item-by-item status against the original Tier 1/2/3 plan, and the original causal-pipeline table this report is structured around |
| `MANUSCRIPT_RESULTS_LOG.md` | Full numeric results ledger, organized by manuscript claim |
| `RUN_LOG_2026-07-02.md` | Today's operational run tracking |
| `L2_CRITIC_DIAGNOSTIC_DESIGN.md` | Implementation spec for the new L2 diagnostic |
| `SUBMISSION_TRACKER.md` | Venue-readiness assessment (A*/A/Q1 calibration) |
