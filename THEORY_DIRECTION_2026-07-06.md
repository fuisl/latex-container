# Theory Direction: Retention-First Grounding (replacing the H1/H2 gate)

**Date:** 2026-07-06 · **Status:** proposed direction, pre-implementation
**Context:** H1 is marginal (only C8 flow_k3 passes 3/3; see `MANUSCRIPT_RESULTS_LOG.md` §1), H2 has no usable events (§2). Meanwhile Φ (flow retention) is robust at every (network, k) (§3) and Ψ(D_MI) is consistent everywhere (§4). This document proposes inverting the paper's epistemic hierarchy: make **retention** the theoretical primitive and demote H1/H2 from gates to derived signatures.

---

## 0. The core move

Current chain in §3.2 of the manuscript:

> H2 (spill-back mechanism) → H1 (MI consequence) → H (partition quality), with H1/H2 as a **mandatory pre-training gate**.

This puts the weakest empirical objects (sparse spill-back events, underpowered pairwise KSG tests) at the foundation. The proposed chain puts the strongest object — retention — at the foundation, and each link sits on an existing formal literature:

```
map equation  ══exact identity══▶  flow retention Φ
     Φ  ──bounded transfer (traffic model)──▶  dependency retention Ψ
     Ψ  ──value-loss bounds (networked MARL / IBA)──▶  regional MARL performance J
```

Headline claim this supports: **minimizing the map equation is minimizing an upper bound on the value loss of regional decomposition in MARL** — InfoMap is a training-free surrogate for coordination-graph design. This is the rigorous version of the ND-POMDP analogy already in §3 ("Map equation as coordination description length"), upgraded from analogy to inequality chain. H1 and H2 become corollaries-in-expectation of the middle link, not axioms.

---

## 1. Link 1 — Map equation ⇒ flow retention (exact identity, prove first)

**Proposition 1.** Let the random walk be the empirical OD walk: stationary edge measure `p_u p_uv = W_uv / Σ_{ab} W_ab`. The map equation's total inter-module transition rate ([Rosvall & Bergstrom 2008]; exact form in the Infomap theory review, [arXiv:2311.04036] Eq. 8: `q_m↷ = Σ_{u∈m, v∉m} p_u p_uv`) satisfies

```
q↷ = Σ_m q_m↷ = Σ_{u,v: c(u)≠c(v)} W_uv / Σ W  =  1 − Φ(P, W).
```

So Φ is not "close to definitional" (current hedge in `MANUSCRIPT_RESULTS_LOG.md` §3) — it **is** the map equation's between-module rate, exactly. The paper should own this as the anchor, not apologize for it.

**Corollary 1.1.** `L(M) = q↷ H(Q) + Σ_m p_m^⟲ H(P_m)`: for a fixed module-size/usage profile, L is monotone increasing in `1 − Φ`. InfoMap maximizes an entropy-regularized Φ; the regularizer (codebook entropies) is what prevents the degenerate all-in-one-module solution. Hence Φ_flow ≥ Φ_METIS at fixed k is a theorem-shaped statement, and the empirical §3 table is its confirmation with real OD data (where the walk model ≠ actual routing, so it's still worth showing).

**Information-theoretic reading (for the "fundamental" framing):** `1 − Φ = q↷` is the per-step probability that the coarse-grained state (module label m(t)) changes. Low q↷ ⇔ the module-label sequence is highly compressible ⇔ the coarse-grained dynamics are maximally predictable. This connects to:
- **Markov stability** ([Delvenne, Yaliraki, Barahona 2010, arXiv:0812.1811]; [Lambiotte, Delvenne, Barahona 2014, arXiv:1502.04381]): Φ is (up to the null-model term) the one-step clustered autocovariance — "probability the walker is in the same community at t and t+1." Map equation and Markov stability are the two canonical *flow-based* (vs. combinatorial/METIS-style) partition objectives; this is the cleanest citable statement of *why* flow-based and geometric partitions are categorically different objects.
- **Markov aggregation / lumpability**: a partition with low exit rate makes the chain nearly lumpable; InfoMap ≈ finding the coarse-graining that loses least description length. (Candidate citation: Deng, Mehta & Meyn, "Optimal Kullback-Leibler aggregation via spectral theory of Markov chains," IEEE TAC 2011 — **not verified this session, check before citing**; the lumpability framing is also surveyed in [arXiv:2204.13896].)

Cost: ~1 page, no new experiments. This is the cheapest, highest-certainty piece.

---

## 2. Link 2 — Flow retention ⇒ dependency retention (the transfer lemma; H1/H2 become corollaries)

**Claim to formalize (Proposition 2).** In a mesoscopic traffic model (spatial-queue / CTM abstraction), inter-intersection statistical dependency is carried **only along flow-carrying edges**, through exactly two channels:

1. **Forward (arrival) channel:** downstream queue state depends on upstream state only through the vehicles actually routed between them; one-step coupling strength bounded by (a function of) edge flow W_uv.
2. **Backward (blocking/spill-back) channel:** finite link capacity couples upstream service feasibility to downstream queues; blocking propagates on the *reverse* flow graph, with incidence proportional to turning flows (CTM: inadequate downstream capacity throttles upstream senders in proportion to their sending flow).

Formal shape: a one-step Dobrushin-style coupling bound, entrywise

```
C_{j←i}  ≤  α · (W_ij + W_ji) / cap  +  (common-demand term)
```

then a data-processing / path-composition argument gives: total dependency mass D_ij between i and j decays with flow-weighted path capacity, hence

```
1 − Ψ(P, D)  ≤  κ · (1 − Φ(P, W̃))  + (demand confounder),   W̃ = symmetrized flow.
```

**Cut flow upper-bounds cut dependency.** The `C^π ≤ E^s + E^a Π(π)` decomposition in [Chakraborty, Rege, Monteleoni & Chen, L4DC 2026, arXiv:2602.16966] is the right modern formalism for the one-step matrix: bound the environment channel E^s entrywise by flow; the policy channel Π is what training modifies. The mechanism premise (coordination needed iff spill-back couples queues) is already cited as `dependencydyn2025` ([arXiv:2502.16608]).

**Consequences — this is where H1/H2 get rescued:**

- **H1 becomes a corollary in expectation**, not a uniform pairwise law. The theory bounds *aggregate dependency mass*, not the ordering of every (i,j,l) pair. Testing all pairs with a Wilcoxon at 3 seeds tests a *stronger claim than the theory makes* — a principled explanation for the marginal pass rates, to state in the manuscript instead of hiding it.
- **H2 becomes the mechanism of the backward channel**, only active near saturation. Cologne8's zero spill-back events don't refute anything: they say the backward channel was inactive there, so C8 dependency is forward/arrival-driven — consistent with C8's positive-but-modest MI gaps. No gate needed.
- **The ρ(W, D) scale-drop gets an explanation and a fix.** ρ(W, D_MI): 0.514 (C8) → 0.141 (I21); ρ(W, D_G): stable 0.75–0.80. The demand-confounder term predicts this: network-wide demand fluctuations create MI between nodes that exchange *no* flow (common cause), and this confounder grows with network size — inflating cross-module D_MI on I21. D_G (the trained model's Jacobian) doesn't inherit the common cause because the model has no incentive to route gradient through non-informative agents. **Concrete fix: estimate D_MI as conditional/partial MI given an aggregate demand covariate** (e.g., total network occupancy at t). Prediction: partialled ρ(W, D_MI|demand) recovers on I21. This is a cheap, falsifiable, theory-driven analysis — arguably the single best new experiment this direction generates.

**Better-powered replacement for the H1 test (statistical rescue):** the theory's testable quantity is coarse-grained predictability, so test at module level, not pair level:
- `I(m(t); m(t+τ))` — predictive information of the module label under the vehicle/walk process (directly the quantity Link 1 says InfoMap maximizes), or
- block MI between module aggregate states `I(X_{M_k}(t); X_{M_k}(t+τ))` vs. cross-block, or a permutation test on total within-module dependency mass `Σ_{c(i)=c(j)} D_ij` against size-matched random partitions (this is exactly Ψ_rel from `metrics.md` #13, now as the *hypothesis test*).
One statistic per (network, k, seed) instead of hundreds of noisy pairwise KSG estimates → the power problem largely dissolves.

Cost: lemma + proof sketch under explicit assumptions (A1: transition kernel factorizes over road graph; A2: one-step coupling bounded ∝ flow; A3: demand stationarity within regime) — honest "stylized model" framing, ~1.5 pages + appendix. Plus the partial-MI rerun (analysis-repo change only).

---

## 3. Link 3 — Dependency retention ⇒ MARL performance (imported bounds)

Three literatures give the theorem shape `J_global − J_regional(P) ≤ f(1 − Ψ(P, ·))`:

1. **Networked MARL exponential decay** ([Qu, Lin, Wierman, Li 2020, arXiv:1912.02906] + [NeurIPS 2020 average-reward version, arXiv:2006.06626]): if one-step influence is local, Q/value sensitivity to agent j decays exponentially in graph distance, and κ-hop truncated policies are `O(ρ^{κ+1})`-approximations. Regional decomposition = truncation to the module; the discarded influence mass is exactly the cut dependency. The new spectral certificate ([arXiv:2602.16966]) weakens the classical Dobrushin row-sum condition to `ρ(H^π) < 1` and makes the bound policy-dependent — directly usable as "assumption A2 ⇒ value-locality ⇒ truncation bias bounded by cut mass."
2. **Influence-based abstraction loss bounds** ([Congeduti, Mey & Oliehoek, AAMAS 2021, arXiv:2011.01788]): a regional critic is a local model that approximates (or ignores) the influence the rest of the network exerts; value loss is bounded by the influence-approximation error. Ignored influence = cross-module dependency ⇒ loss ≤ g(1−Ψ). This is the cleanest citation for **L2**, the paper's strongest empirical result.
3. **ND-POMDP / factored value + weakly coupled MDPs** (already in the manuscript; [Meuleau et al. 1998] for the weakly-coupled ancestry): value decomposes along the coordination graph; regional critics are exact when cut dependency is zero, and CriticFactorizationError (`metrics.md` #26) measures the violation.

**Per-level reading (matches the observed level-dependence):**
- **L1 (regional reward):** shared reward is a noisy surrogate for own reward; its bias/noise scales with within-module reward *misalignment*, which the forward channel ties to flow coherence. Predicts flow ≻ METIS most strongly where reward coupling is rawest — matches IPPO results (6.7 s/veh gap, 26 vs 83 spikes).
- **L2 (regional critic):** IBA bound — matches MAPPO being robust and strongest.
- **L3 (attention masking):** truncation bound has a *second term that grows as modules shrink below the influence-decay length*: masking removes edges the decay bound still needs. **This gives the k-reversal (`MANUSCRIPT_RESULTS_LOG.md` §5, replicated cross-network) a theoretical home: a predicted phase boundary (module diameter vs. decay length ρ), not an anomaly.** Smaller k ⇒ modules ≥ decay length ⇒ flow wins; larger k ⇒ modules < decay length ⇒ truncation term dominates and geometric compactness (METIS) can win. This upgrades the existing "module-size saturation" conjecture into a quantitative prediction: the reversal point should shift with network size and demand level. Worth a small dedicated result/figure.

Cost: no new proofs from scratch — state a theorem that *imports* (1)/(2) conditional on Proposition 2's coupling bound, with assumptions explicit. ~1 page + appendix.

---

## 4. What the empirical program becomes

The `metrics.md` §4 chain stays, but its role changes: **the experiments now estimate the slope/constants of stated bounds instead of gating on hypothesis tests.**

| Stage | Quantity | Status | New role |
|---|---|---|---|
| 1 | Φ(P,W) vs. L(M) | done, robust | confirms Prop 1 identity on real OD data |
| 2 | corr(Φ, Ψ) across partition family | partial | estimates Prop 2 transfer constant κ |
| 2b | ρ(W, D_MI \| demand) partial MI | **new, cheap** | tests the confounder explanation of the I21 drop |
| 2c | Ψ_rel permutation test (size-matched random partitions) | planned (metrics #13) | **replaces the H1 Wilcoxon as the headline significance test** |
| 3 | corr(Ψ, J) across {InfoMap, METIS, spectral, random, none, global} | planned | tests the value-loss bound's monotonicity |
| 3b | k-sweep of Ψ(D_G) and J at L3 | partially exists | locates the predicted reversal boundary |

Partition family sweep (InfoMap / METIS / spectral / random-size-matched / none / global) is what makes stage 3 a real test rather than a two-point comparison — already anticipated in `metrics.md` §4.

---

## 5. Manuscript surgery implied (ordered by cost/benefit)

1. **§3.2 rewrite:** replace "mandatory gate; halt on H1/H2 failure" with the three-link chain; H1/H2 re-labeled *operational signatures* of Link 2 (H1 = forward channel, H2 = backward channel), reported with the honest stats already in `MANUSCRIPT_RESULTS_LOG.md`.
2. **Add Proposition 1 + Corollary** (exact, ~1 page). Reframe the Φ table as its empirical confirmation.
3. **Add Proposition 2 as a stylized-model lemma** with explicit assumptions; move proof to appendix.
4. **Add the imported value-loss theorem (Link 3)** with the per-level table; use it to *predict* the k-reversal and present §5's reversal as confirming evidence.
5. **Analysis-repo asks** (user's private repo): partial-MI D_MI rerun; Ψ_rel permutation test; module-level predictive information I(m(t); m(t+τ)).
6. Contributions list (§1) updates: "first formal derivation connecting map equation minimization to an upper bound on regional-MARL value loss" replaces the current H1/H2-gated phrasing.

## 6. Risks / honest limits (state these, don't hide them)

- **One-directional bounds.** High Φ/Ψ is (approximately) *necessary* for lossless regional decomposition, not sufficient — METIS also retains substantial flow. The theory predicts ordering and bounds, not that InfoMap is optimal for J.
- **Walk model ≠ routing.** The map equation's memoryless-walk assumption vs. real trip routing is already acknowledged in the manuscript (§ map-equation caveat); Prop 1 uses the *empirical* OD walk, which sidesteps part of this, but path-dependence of real trips remains a gap (higher-order map equation is the standard pointer).
- **Prop 2's constant is network-dependent** — the C8 vs I21 alignment drop is real; the demand-confounder fix is a hypothesis until 2b runs.
- **Ψ(D_G) diagnostic vs. trained performance mismatch** (log §5 caveat, I21 Variant B k=5) is still open; the Link-3 framing predicts the diagnostic and performance *can* diverge when the truncation term dominates, but that check (C8 CoLight k=5) should still run.
- **Deng–Mehta–Meyn citation unverified this session**; verify before adding to refs.bib.

## 7. Verified sources (this session)

- Map equation exact q↷ formula: [Community Detection with the Map Equation and Infomap: Theory and Applications (arXiv:2311.04036)](https://arxiv.org/html/2311.04036v2)
- Markov stability / flow-based vs combinatorial partitions: [Delvenne et al., Stability of graph communities across time scales (arXiv:0812.1811)](https://arxiv.org/pdf/0812.1811); [Lambiotte, Delvenne, Barahona (arXiv:1502.04381)](https://arxiv.org/pdf/1502.04381); [Schaub et al., dynamics-based framework (arXiv:1308.1605)](https://arxiv.org/pdf/1308.1605)
- Lumpability / info-theoretic Markov reduction survey: [arXiv:2204.13896](https://arxiv.org/pdf/2204.13896)
- Networked MARL decay bounds: [Qu, Lin, Wierman, Li (arXiv:1912.02906)](https://arxiv.org/abs/1912.02906); [average-reward version (arXiv:2006.06626)](https://arxiv.org/abs/2006.06626)
- Policy-dependent spectral value-locality certificate: [Chakraborty, Rege, Monteleoni, Chen, L4DC 2026 (arXiv:2602.16966)](https://arxiv.org/pdf/2602.16966) — read pp.1–4 directly; abstract: `C^π ≤ E^s + E^a Π(π)`, `ρ(H^π)<1` certificate, κ-hop truncation bias decays exponentially
- Influence-based abstraction loss bounds: [Congeduti, Mey, Oliehoek, AAMAS 2021 (arXiv:2011.01788)](https://arxiv.org/abs/2011.01788)
- Dependency dynamics in TSC (already cited as dependencydyn2025): [arXiv:2502.16608](https://arxiv.org/pdf/2502.16608)
- CTM/spatial-queue spill-back propagates upstream ∝ sending flows: [link queue model (arXiv:1209.2361)](https://arxiv.org/pdf/1209.2361); [turn-level queue transmission (arXiv:2310.12249)](https://arxiv.org/pdf/2310.12249)
- MFD/perimeter-control partitioning (traffic-engineering precedent for regional decomposition): [community detection in congested urban networks (PMC8629316)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8629316/)
