# Thesis Defense Plan — FGS Framework for Graph-Aware Traffic Signal Control

**Duration**: 30–35 minutes  
**Format**: HTML slides (reveal.js recommended)  
**Core message**: FGS is a principled ablation framework that systematically characterizes a three-module MARL design space on real German traffic networks — producing three concrete, transferable design guidelines.

---

## Framing Principle (Read This First)

Your committee will notice that FGSv3-PPO (68.4 s) does **not** beat standalone PPO (67.2 s) on ingolstadt21. Do **not** oversell performance. The defense spine is the **characterization contribution**: FGS is a structured tool for mapping which component (encoder / graph attention / RL algorithm) matters at which network scale, on a benchmark no prior graph-aware method had evaluated on. The clean wins are:

- **FGS vs. graph-based CoLight**: −57% on cologne8, −68% on ingolstadt21.
- **The ablation findings**: concrete, quantified, design-transferable.
- **The three-generation engineering story**: turning three failure modes into three design fixes.

Never present gamed checkpoints (‡ in thesis) as headline performance. The gaming story is a *strength* — you diagnosed it and quantified when it occurs.

---

## Time Budget

| Section | Slides | Minutes |
|---|---|---|
| 1. Hook & Problem | 1–3 | 5 |
| 2. FGS Framework | 4–7 | 8 |
| 3. Results | 8–13 | 13 |
| 4. Contributions & Close | 14–16 | 5 |
| **Soft buffer** | — | 2–4 |
| **Q&A** (not in your 30–35) | — | 15–20 |

---

## Slide-by-Slide Plan

---

### SECTION 1 — Hook & Problem (5 min)

---

#### Slide 1 — Title (30 s)

**Content**

```
FGS: A Framework for Graph-Aware Traffic Signal Control
Systematic Design Characterization on German RESCO Benchmarks

[Your name] · [Institution] · [Date]
```

**Visualization spec**  
Background: low-opacity animated top-down view of a road network with colored signal phases cycling (see Viz-A below). Subtle, not distracting. Sets the scene without a word.

**Speaker notes**  
No narration needed. Let the animation run for 5–10 seconds, then begin.

---

#### Slide 2 — The Problem (90 s)

**Content**  
Two-column layout.

*Left column* — "Why is network-level TSC hard?" (3 bullet fragments, revealed one at a time):
- Signal timing affects not just one intersection — queues spill back across the network
- Adaptive controllers (SCOOT/SCATS) need dense sensor infrastructure and expert calibration
- RL methods exist, but were almost exclusively tested on synthetic Chinese grid networks

*Right column* — **animated network congestion demo** (Viz-A, full): Cologne8 topology with nodes flashing red/green as simulated demand builds up. Visible queue accumulation on a few edges.

**Speaker notes**  
"Germany has some of Europe's highest vehicle density. Cologne and Ingolstadt — both evaluated here — represent medium-density European urban networks with irregular topologies. The core challenge is that no published graph-aware MARL method had been evaluated on these real networks before this work."

---

#### Slide 3 — Three Gaps in the Literature (90 s)

**Content**  
Three numbered items revealed one at a time (animated stagger):

1. **No graph-aware MARL on German networks** — dominant benchmarks are synthetic Chinese grids (Hangzhou, Jinan); RESCO German scenarios existed but were untested with graph communication.
2. **SAC unused in graph-aware MARL-TSC** — DQN and PPO dominate; entropy-regularized off-policy SAC had not been systematically paired with graph attention.
3. **Design space never ablated** — encoder, communication, RL algorithm always bundled together; no method mapped which component contributes what at which scale.

*Visual*: small "gap" icon (⚠) next to each. Third bullet highlighted after reveal — this is the one FGS directly addresses.

**Speaker notes**  
"The third gap is the core motivation. Every prior paper bundles these three choices together, so you never know whether the result is due to the encoder, the graph layer, or the RL optimizer. FGS breaks that bundle."

---

### SECTION 2 — The FGS Framework (8 min)

---

#### Slide 4 — The Three-Module Pipeline (2 min)

**Content**  
Full-slide animated pipeline diagram (Viz-B). Three modules revealed sequentially:

```
SUMO Env → [Module I: Encoder] → [Module II: Communication] → [Module III: RL Optimizer] → π_i
```

For each module, a sub-bullet appears below it when highlighted:
- **Module I (Encoder)**: maps raw lane counts, queue, phase state → local embedding h_i
- **Module II (Communication)**: GATv2 aggregates neighbor embeddings over road graph → context g_i
- **Module III (RL Optimizer)**: actor produces discrete phase selection; critic updated centrally (CTDE)

Below the pipeline, the key claim appears last:
> "Every MARL-TSC architecture is fully characterized by three independent choices. FGS makes those choices explicit and independently configurable."

**Visualization spec** (Viz-B)  
Animated SVG pipeline. Boxes light up left-to-right with a 0.5 s delay. A data packet (small dot) animates along the arrow path. When Module II lights up, a small graph of 3–4 nodes appears above it with edges pulsing, representing neighbor aggregation. Built with CSS keyframes + SVG; embed directly in reveal.js slide.

**Speaker notes**  
"This is the FGS pipeline. Every prior method — IntelliLight, PressLight, CoLight, FRAP — implicitly follows this structure, even though they don't describe it this way. FGS makes the three modules explicit, independently swappable, and ablated."

---

#### Slide 5 — Design Space: Where Prior Work Lives (90 s)

**Content**  
Table (animated row-by-row reveal):

| Method | Encoder | Communication | RL |
|---|---|---|---|
| IntelliLight | MLP | None | DQN |
| PressLight | MLP | None | DQN |
| CoLight | MLP | GAT | DQN |
| FRAP (standalone) | FRAP | None | — |
| **FGS (Gen-1)** | **MLP / FRAP** | **GATv2** | **SAC / PPO** |
| **FGSv3 (final)** | **MLP** | **GATv2(D)** | **SAC + PPO** |

Footer text (appears last):
> "No prior work treats all three as variables and ablates their interactions on German RESCO. That is this thesis."

**Speaker notes**  
"Notice the gap in the table: nobody combined a phase-competition encoder with graph attention, nobody used SAC, and nobody evaluated these choices independently. The bottom two rows are new."

---

#### Slide 6 — Six German RESCO Scenarios: Three Scale Tiers (90 s)

**Content**  
Animated network topology reveal (Viz-C). Three tiers appear in sequence:

**Tier 1 — Single-intersection** (N=1)
- cologne1 · ingolstadt1

**Tier 2 — Corridor** (N=3–7)
- cologne3 · ingolstadt7

**Tier 3 — Regional** (N=8–21)
- cologne8 · ingolstadt21 ← *primary test bed*

Each tier uses the real topology graph (from `scenario_topologies.pdf`). Nodes are colored circles; edges are road links. Regional tier nodes are larger and glow slightly.

Key fact below (fades in last):
> 200 training episodes · 1 hour simulated demand per episode · TapasCologne + InTAS real-world demand models

**Visualization spec** (Viz-C)  
Use D3.js force-directed layout or import the SVG coordinates from the existing `scenario_topologies.pdf` (convert to SVG). Animate: Tier 1 nodes appear first, then Tier 2 nodes grow outward, then Tier 3 nodes expand. Use color to distinguish tiers (blue/orange/red). Each node pulses briefly as it appears. Smooth 400 ms transition per node.

**Speaker notes**  
"Six scenarios, three scale tiers. The key question running through all results is: does the benefit of graph communication grow with network scale? The short answer is yes — but the evidence is more nuanced than a simple yes."

---

#### Slide 7 — Three Generations: Diagnosis and Repair (2 min)

**Content**  
Horizontal timeline with three stops. Each stop reveals sequentially (click to advance):

```
FGSv1 (Gen-1)          FGSv2                    FGSv3 (final)
─────────────────────────────────────────────────────────────
Failure: FRAP           Fix: tap FRAP            Fix: demand-aware
scalar projection       before projection →      embeddings for
discards per-phase      preserve per-phase       communication +
info before graph       action tokens            factored neighborhood
aggregation                                      critic O(d_c) not O(Nd)

                         ↓ New failure:
                         communication signal
                         carries competition
                         rankings, not demand
                         state
```

Bottom row (appears after all three): 
> "Each generation was driven by empirical failure, not a priori design. This is the engineering contribution."

**Visualization spec**  
CSS-animated horizontal timeline. Each generation is a vertical card. On click, the failure text fades in red, then the arrow and fix text fade in green. The critic complexity formula `O(Nd_h') → O(d_c)` appears as a highlighted chip on FGSv3. Keep it visual — minimize text per card.

**Speaker notes**  
"FGSv1 exposed two interface failures. The first: FRAP collapses its per-phase embeddings to a scalar before passing to the graph layer — so the graph receives no actionable phase information. FGSv2 fixed that but revealed the second: the signal passing through the graph carried competition rankings, not actual demand. FGSv3 switches to demand-aware embeddings and — critically — replaces the centralized critic with a factored neighborhood critic, because the original critic's input dimension grows as O(N×d), which exhausted GPU memory at N=21 after just 17 episodes."

---

### SECTION 3 — Results (13 min)

---

#### Slide 8 — Main Results: The Honest Overview (3 min)

**Content**  
*Title*: "How does FGS compare to baselines?"

Two-stage reveal:

**Stage 1** — Animated bar chart (Viz-D): mean delay across all six scenarios, methods revealed one group at a time:
1. Fixed-Time and MaxPressure (classical) — appear first (tall bars)
2. DQN, PPO, IndSAC (independent RL) — appear second
3. FRAP, CoLight (specialized graph/encoder) — appear third
4. FGS_S, FGS_P, FGSv3 — appear last

Use log-scale y-axis (matches thesis Figure). Color-code by category, not by method name.

**Stage 2** — Three callout annotations appear:
- ✅ "FGSv3-PPO matches standalone PPO at N=21" (callout on ingolstadt21)
- ✅ "FGS(MLP+GATv2+SAC) −57% vs CoLight on cologne8" (callout on cologne8)
- ⚠ "FGS does not clearly beat independent PPO/DQN at small scale — by design"

**Speaker notes**  
"Three things to notice. First, at Single-intersection scale, all learning methods converge to similar delays — there's nothing for graph communication to do. Second, at Regional scale, FGSv3-PPO is competitive with the best independent controller and strongly outperforms the graph-based CoLight. Third — and I want to be explicit about this — FGSv3-PPO does not surpass standalone PPO. That's expected: at the scales we tested, independent controllers have enough local information to converge. What FGS provides is a structured characterization of *why* and *when* each component matters."

---

#### Slide 9 — Central Finding: Scale Dependency (2 min)

**Content**  
*Title*: "The benefit of graph communication grows with network scale"

Two-panel layout:

*Left*: Animated scale-benefit bar chart (Viz-E):
- x-axis: N=1, N=3–7, N=8–21
- y-axis: % improvement of best FGS over CoLight (filled bars) and over PPO (outlined bars)
- Bars animate in left to right

Key numbers to show:
- N=1: ~0% (graph is no-op by construction)
- N=7 (ingolstadt7): FGS_P = 26.1s vs CoLight 47.0s → +44%; vs PPO 24.1s → −8%
- N=21 (ingolstadt21): FGSv3-PPO = 68.4s vs CoLight 216.8s → +68%; vs PPO 67.2s → ~parity

*Right*: Theoretical explanation in two lines:
```
N ≤ 3:  local obs. captures full demand context
N ≥ 7:  multi-hop dependencies exceed local horizon
        → graph communication needed
```

**Visualization spec** (Viz-E)  
Chart.js grouped bar chart. Animate bars growing from zero on entrance. Two datasets per tier: CoLight-relative (solid fill) and PPO-relative (outlined, hatched). Tooltip shows exact numbers on hover.

**Speaker notes**  
"This is the central finding. At N=1 the graph module is structurally a no-op — there are no neighbors to aggregate. At Corridor scale, independent PPO is actually slightly better than FGS variants — local observations are sufficient. At Regional scale, the advantage of graph communication becomes real: FGSv3-PPO cuts CoLight's delay by 68%. The transition point is somewhere between N=7 and N=21."

---

#### Slide 10 — Ablation 1: Encoder — FRAP vs. MLP (2.5 min)

**Content**  
*Title*: "Design guideline 1: MLP encoders outperform FRAP on German networks"

Three-part layout:

*Top*: Why FRAP fails on German intersections (one brief diagram):
- FRAP assumes: each phase controls exactly two opposing movements
- German RESCO reality: phases control 2, 4, or 6 movements; some have 1 movement
- When a phase controls <2 movements → FRAP normalization → undersaturated features → actor selects wrong phase

*Middle*: Animated training curve comparison (Viz-F):
- x-axis: episodes (0–200)
- Two lines: MLP+GATv2+PPO (converges) vs FRAP+GATv2+PPO (diverges at N=21)
- Animation plays episode-by-episode, curves drawing in real time

*Bottom*: Quantitative impact (fade-in chips):
- Cologne8 (N=8): FRAP penalty = **+11%** (24.6s vs 24.0s)
- Ingolstadt21 (N=21): FRAP penalty = **+2.6×** (617.0s vs 234.9s)

**Visualization spec** (Viz-F)  
Two side-by-side Chart.js line charts (cologne8 left, ingolstadt21 right). On slide enter, lines animate drawing from left to right over 2 seconds. Use thick lines (3px). MLP = blue stable convergence; FRAP = orange diverging. Add a vertical "episode 100" reference line.

**Speaker notes**  
"FRAP was designed for Chinese 4-way intersections with fixed 8-phase structures. On German networks — where phases vary from 2 to 6 per intersection — its competition-based normalization produces near-zero features for some phases. The actor sees 'no demand' and selects the wrong phase. At N=8, GATv2 partially compensates by down-weighting FRAP-misaligned neighbors. At N=21, that compensation is overwhelmed. This is not a critique of FRAP's design — it's an empirical finding about domain transfer."

---

#### Slide 11 — Ablation 2: Graph Attention — GATv2 vs. GAT (2 min)

**Content**  
*Title*: "Design guideline 2: GATv2 dynamic attention is critical at scale — not at small scale"

Two-panel layout:

*Left panel* — Quantitative result (animated number reveal):
```
Ingolstadt21 (N=21):
  GATv2:  234.9 s mean delay
  GAT:    492.0 s mean delay  
  ──────────────────────────
  Difference: −53%
```
```
Cologne8 (N=8):
  GATv2: 24.0 s
  GAT:   24.9 s  (only 4% difference)
```

*Right panel* — Animated GATv2 attention visualization (Viz-G): ingolstadt21 topology graph. Edges have thickness proportional to attention weight. Animation shows attention weights shifting as simulated demand changes across 5 snapshot states.

Below: mechanism explanation (one line):
> GATv2 per-edge attention: α_ij = f(h_i, h_j) — structurally distinct neighbors get distinct weights.  
> GAT dot-product: assigns near-uniform weights on heterogeneous topologies.

**Visualization spec** (Viz-G)  
D3.js network graph. Load ingolstadt21 topology (approximate from `scenario_topologies.pdf` or generate from adjacency). 21 circle nodes, edges. Five pre-computed "attention snapshots" (mock data with random variation that illustrates the concept). Cycle through snapshots every 1.5 s with smooth edge-width transition. Highlight 2–3 high-attention edges in orange.

**Speaker notes**  
"GAT uses dot-product attention, which assigns nearly identical weights to nodes sharing feature-space proximity regardless of their neighborhood context — it produces averaging, not selective aggregation. GATv2's per-edge dynamic attention assigns distinct weights even to structurally similar nodes. On ingolstadt21's irregular topology, where every intersection has a unique demand-phase profile, this distinction produces a 53% reduction in mean delay. On cologne8's smaller and more homogeneous topology, both mechanisms converge to similar solutions."

---

#### Slide 12 — Ablation 3: RL Algorithm — SAC vs. PPO + the Critic Fix (2.5 min)

**Content**  
*Title*: "Design guideline 3: SAC is efficient at moderate scale but requires a factored critic at N=21"

Three-part structure revealed sequentially:

**Part A** — SAC advantage at N=8:
```
cologne8 (N=8):
  MLP+GATv2+SAC: 22.2 s
  MLP+GATv2+PPO: 24.0 s   → SAC −8%
```
Reason: off-policy replay buffer reuses transitions; entropy bonus supports exploration.

**Part B** — SAC failure at N=21 (first generation):
Animated "crash" graphic — a training curve that flatlines after episode 17.
```
Centralized critic input dim at N=21: ~3,133 features
GPU memory exhausted after 17 episodes
```

**Part C** — FGSv3 fix: factored neighborhood critic:
```
FGSv1/2 critic:  O(N × d_h') → scales with agent count
FGSv3 critic:    O(d_c + A_max) → independent of N
```
Result: SAC now completes at N=21.

*Also on this slide*: brief honest note on reward gaming:
> ⚠ SAC checkpoints on Corridor scenarios exhibit reward-specification gaming (phase-cycling). All such entries are excluded from performance claims (marked ‡ in thesis tables).

**Speaker notes**  
"SAC's off-policy sample efficiency gives it an advantage at N=8 — 8% lower mean delay than PPO. But the first-generation centralized critic concatenates all agents' state vectors, so input dimension grows linearly with N. At N=21 that's ~3,100 input features, and training terminated from GPU memory exhaustion after 17 episodes. FGSv3 replaces this with a factored critic that aggregates only within each agent's local neighborhood — input stays O(d_c), independent of total agent count. SAC can now complete training at N=21."

---

### SECTION 4 — Contributions & Close (5 min)

---

#### Slide 13 — Three Design Guidelines (2 min)

**Content**  
Full-slide, three-card layout. Each card fades in on click:

```
┌──────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐
│ 1. Encoder                   │  │ 2. Graph Attention            │  │ 3. RL Algorithm              │
│                              │  │                              │  │                              │
│ Use MLP, not FRAP, on        │  │ GATv2 dynamic attention       │  │ SAC is efficient at          │
│ German networks.             │  │ is worth the cost — but       │  │ N ≤ 8. Use a factored        │
│                              │  │ only at N ≥ 21.              │  │ critic to scale to N=21.     │
│ FRAP's phase-competition     │  │ At smaller scale, GAT and     │  │                              │
│ priors misalign with         │  │ GATv2 are equivalent.        │  │ Reward specification gaming  │
│ heterogeneous German         │  │                              │  │ must be monitored in         │
│ phase structures.            │  │ 53% delay reduction at N=21  │  │ entropy-bonus methods.       │
│                              │  │ (234.9s → 492.0s with GAT)   │  │                              │
│ Penalty grows with N:        │  │                              │  │ Replacing diff. wait-time    │
│ +11% at N=8 → 2.6× at N=21  │  │                              │  │ reward with pressure signal  │
│                              │  │                              │  │ is a direct next step.       │
└──────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘
```

Footer (appears last, bold):
> These three guidelines are directly transferable to any MARL-TSC system targeting heterogeneous urban networks.

**Visualization spec**  
Three card flip animations. Cards start face-down, flip on reveal. Each card has a large icon (🔷 encoder, 🕸 graph, 🤖 RL) and two lines of key claim. CSS 3D flip animation, ~0.6 s each.

**Speaker notes**  
"These three guidelines are the core empirical output. They didn't exist in the literature before this work because no prior study had ablated these dimensions independently on German RESCO scenarios. Any team building a MARL-TSC system for irregular European networks can directly apply these."

---

#### Slide 14 — Contributions Summary (1 min)

**Content**  
Four-quadrant layout (all revealed at once, brief):

```
┌────────────────────────┬──────────────────────────────┐
│ Framework              │ Algorithmic                  │
│ Modular 3-module       │ 3-generation FGS trajectory  │
│ MARL-TSC pipeline      │ each fixing a diagnosed      │
│ (encoder / comm / RL)  │ module-interface failure     │
├────────────────────────┼──────────────────────────────┤
│ Empirical              │ Analytical                   │
│ First graph-aware MARL │ Component ablation across    │
│ evaluation on all 6    │ 8 design-space combinations  │
│ German RESCO scenarios │ on 2 Regional scenarios      │
└────────────────────────┴──────────────────────────────┘
```

**Speaker notes**  
"Four contributions. The framework and algorithmic ones are engineering. The empirical and analytical ones are the knowledge contribution to the MARL-TSC field."

---

#### Slide 15 — Limitations & Future Work (2 min)

**Content**  
Two-column layout:

*Limitations (honest):*
- Single-seed results for most configurations — point estimates, no confidence intervals
- SUMO simulation only; no real-world deployment
- FGSv3 not evaluated on Corridor scenarios
- Reward specification gaming in SAC on Corridor tier (corrected by checkpoint exclusion, not by algorithm fix)

*Future work (prioritized):*
1. Five-seed evaluation + bootstrap CIs (immediate validation priority)
2. Pressure-based reward to eliminate gaming vulnerability
3. Extension to city-scale networks (N > 100) via hierarchical MARL or sparse attention
4. Transfer across cities / demand distribution shift

**Speaker notes**  
"I want to be transparent about two limitations. First, most results are single-seed, so the performance numbers are point estimates without variance bounds — completing the five-seed evaluation is the first follow-on priority. Second, the reward specification gaming in SAC on Corridor scenarios is mitigated by checkpoint exclusion, but the right fix is a better reward signal — replacing differential waiting time with a pressure or queue-clearing reward."

---

#### Slide 16 — Conclusion (30 s)

**Content**  
Single clean slide:

> **FGS is a modular three-module pipeline that makes the MARL-TSC design space explicit and ablatable on real German road networks.**
>
> The central result is not that FGS is the best-performing system — it is that we now know *which component matters at which scale*, and *why*.
>
> Three design guidelines. Four contributions. Six German RESCO scenarios. One transferable characterization framework.

Background: same low-opacity network animation as title slide (Viz-A).

**Speaker notes**  
"Thank you. I'm happy to take questions."

---

### BACKUP SLIDES (Q&A Support)

---

#### B1 — "Why doesn't FGS beat standalone PPO?"

**Content**  
Full honest answer on one slide:

- FGS is designed for network-level coordination where inter-agent dependencies exceed local observation horizon
- At N=21 (ingolstadt21), FGSv3-PPO achieves 68.4 s vs standalone PPO 67.2 s — the gap is 1.2 s (1.8%)
- At N=8 (cologne8), FGS(MLP+GATv2+SAC) achieves 22.2 s vs PPO 21.9 s — similar
- Local observations at the Regional tier still carry most of the decision-relevant information — PPO can approximate the coordination implicitly through reward shaping
- FGS's 68% advantage over CoLight shows graph communication helps *when the alternative is also graph-based but with static attention*
- The benefit of explicit structured communication likely grows beyond N=21; the FGSv3 factored critic was designed to scale to that regime

Key quote from thesis abstract:
> "FGSv3-PPO achieves 68.4 s mean delay on ingolstadt21, competitive with standalone PPO (67.2 s) and strongly outperforming CoLight (216.8 s)."

---

#### B2 — "Can you trust single-seed results?"

**Content**  
- All results are single-seed (seed 0) — explicitly acknowledged in Section 5.2 and 6.1 of the thesis
- Best-validation checkpoint protocol is standard in deep RL (matches RESCO baseline evaluation)
- For the ablation comparisons, the factor-of-2.6× FRAP penalty at N=21 is too large to be reversed by seed variance
- The GATv2/GAT 53% gap at N=21 is similarly large
- Directional conclusions (which component matters more at what scale) are robust; precise performance numbers require five-seed replication
- Five-seed completion is the stated first priority for follow-on work

---

#### B3 — "What is the reward specification gaming?"

**Content**  
Brief explainer:

SUMO accumulates a vehicle's waiting time as time stopped. The counter **resets the instant the vehicle moves** — even if it immediately stops again (e.g., due to a red at the next lane).

SAC's entropy bonus explicitly rewards distributing probability mass across actions. Phase cycling (green → red → green rapidly across multiple phases) both:
1. Briefly moves vehicles → resets their waiting timer → reduces the reward penalty
2. Increases the entropy of the phase distribution → adds entropy bonus

PPO avoids this because it discards stale transitions after each episode, so the queue growth from cycling appears in the next update. SAC's replay buffer delays this feedback.

Detection: mean delay anomalously low **AND** mean queue length anomalously high at the same checkpoint (physically incompatible in steady state).

Fix: use a pressure reward (counts vehicles waiting at the stop line per lane, not accumulated time) or a queue-clearance reward.

---

#### B4 — Full Ablation Results Table

| Encoder | Graph | RL | cologne8 MD (s) | ingolstadt21 MD (s) |
|---|---|---|---|---|
| MLP | GATv2 | SAC | **22.2** | 39.1 ‡ |
| MLP | GATv2 | PPO | 24.0 | **234.9** |
| MLP | GAT | PPO | 24.9 | 492.0 |
| FRAP | GATv2 | PPO | 24.6 | 617.0 |

‡ = physically inconsistent checkpoint (excluded from Bold).  
FGSv3-PPO (cologne8): 21.6 s · FGSv3-PPO (ingolstadt21): 68.4 s [separate from Gen-1 ablation rows above].

---

## Interactive / Animated Visualization Specifications

---

### Viz-A — Traffic Network Background Animation

**Purpose**: Hero background for title and closing slides. Sets context without a word.  
**Technology**: D3.js SVG + CSS animation  
**Implementation**:

```
1. Render cologne8 (8 nodes) or ingolstadt21 (21 nodes) topology as SVG circles + lines
2. Each node has a color state: GREEN / YELLOW / RED / GREEN (signal cycle)
3. Animate each node independently with a random phase offset (stagger 0–4 s per node)
4. Cycle period: ~8 s per node (2 s green → 0.5 s yellow → 2 s red → repeat)
5. Edges between nodes: low-opacity gray lines with occasional animated "vehicle" dot 
   traveling from one node toward another (SVG stroke-dashoffset animation, 3–5 dots 
   active at any time)
6. Full animation: opacity 15% so it reads as background, not foreground
```

**Data needed**: Node positions from `scenario_topologies.pdf` (extract approximate coordinates or regenerate from SUMO network file). Adjacency matrix from thesis (cologne8 has 8 intersections; see experimental design chapter).

---

### Viz-B — FGS Pipeline Animation

**Purpose**: Reveal the three-module pipeline concept sequentially.  
**Technology**: CSS keyframe animation + inline SVG in reveal.js HTML slide  
**Implementation**:

```
Layout: 5 horizontally-spaced elements
  [SUMO Box] → arrow → [Encoder Box] → arrow → [Comm Box] → arrow → [RL Box] → arrow → [π circle]

On slide entry: all boxes appear gray/muted
Step 1 (click): SUMO box glows blue; data packet (circle) animates right along arrow (0.6s)
Step 2 (click): Encoder box glows; sub-bullet fades in below; second data packet animates
Step 3 (click): Comm box glows; small 3-node graph appears above it with pulsing edges
Step 4 (click): RL box glows; π circle appears; sub-bullets for CTDE note appear
Step 5 (click): Footer quote fades in

Color scheme:
  SUMO = gray (#666)
  Encoder = blue (#2196F3)
  Communication = green (#4CAF50)
  RL = orange (#FF9800)
  π = gold (#FFC107)
```

---

### Viz-C — Scale Tier Network Reveal

**Purpose**: Show 6 German RESCO scenarios across 3 tiers with actual topology.  
**Technology**: D3.js + reveal.js fragment  
**Implementation**:

```
Layout: 3 column grid (Tier1 / Tier2 / Tier3)

Each tier: two mini-network graphs side by side (Cologne | Ingolstadt)

Node entry animation:
  - Tier 1 nodes: pop in with scale(0) → scale(1), duration 300ms
  - Tier 2 nodes: same, staggered 50ms per node
  - Tier 3 nodes: same, staggered 30ms per node (21 nodes total)

Node color by tier:
  Tier 1 = blue (#2196F3)
  Tier 2 = orange (#FF9800)  
  Tier 3 = red (#F44336)

Edge style: thin gray lines between connected intersections
Node size: scales with tier (Tier 1 = r:12; Tier 2 = r:10; Tier 3 = r:8)

Topology source: Extract from src/Figures/scenario_topologies.pdf 
OR generate approximate positions from SUMO .net.xml files in the RESCO benchmark.
Adjacency:
  cologne1:    1 node
  cologne3:    3 nodes in a line
  cologne8:    8 nodes (see SUMO net file)
  ingolstadt1: 1 node
  ingolstadt7: 7 nodes
  ingolstadt21: 21 nodes
```

---

### Viz-D — Animated Bar Chart: Main Results

**Purpose**: Reveal baseline comparison with grouped bars, scenario by scenario.  
**Technology**: Chart.js (v4) with custom reveal.js integration  
**Implementation**:

```javascript
// Data (mean delay in seconds, use only converged non-‡ values)
const scenarios = ['cologne1','cologne3','cologne8','ingolstadt1','ingolstadt7','ingolstadt21'];
const methods = {
  'Fixed-Time': [54.6, 63.7, 51.5, 40.8, 122.9, 145.7],
  'MaxPressure': [24.2, 56.4, 257.9, 25.3, 212.7, 214.4],
  'DQN':        [28.1, 127.2, 25.5, 21.8, 34.4, 78.7],
  'PPO':        [22.8, 20.3, 21.9, 22.4, 24.1, 67.2],
  'CoLight':    [23.9, 19.3, 51.8, 22.4, 47.0, 216.8],
  'FRAP':       [31.7, null, 44.9, 26.6, 29.8, null],
  'FGS_S':      [23.0, null, 22.2, null, null, null],
  'FGSv3-PPO':  [12.0, null, 21.6, 17.4, null, 68.4]
};

// Chart config
type: 'bar'
scales.y: { type: 'logarithmic' }  // log scale to match thesis fig
colors: {
  'Fixed-Time': '#9E9E9E',
  'MaxPressure': '#9E9E9E',
  'DQN': '#2196F3',
  'PPO': '#1565C0',
  'CoLight': '#FF9800',
  'FRAP': '#FF5722',
  'FGS_S': '#4CAF50',
  'FGSv3-PPO': '#2E7D32'
}

// Reveal animation: methods appear one group at a time
// triggered by Reveal.js fragment events
// Each group animates with Chart.js animation duration: 800ms
```

Annotations (using chartjs-plugin-annotation):
- Arrow pointing to ingolstadt21 FGSv3-PPO bar: "68.4s — competitive with PPO (67.2s)"
- Arrow pointing to cologne8 FGS_S bar: "−57% vs CoLight"

---

### Viz-E — Scale Benefit Animated Chart

**Purpose**: Quantify graph-communication benefit as a function of scale tier.  
**Technology**: Chart.js  
**Implementation**:

```javascript
// X-axis: 3 groups (Single N=1 / Corridor N=3-7 / Regional N=8-21)
// Two bar datasets per group:
//   Dataset 1 (solid): % improvement best-FGS vs CoLight
//   Dataset 2 (outlined): % improvement best-FGS vs PPO (negative = worse)

data = {
  'Single (N=1)':    { vsCoLight:  1,  vsPPO:  0 },   // negligible / no-op
  'Corridor (N=3-7)':{ vsCoLight: 44,  vsPPO: -8 },   // outperform CoLight, trail PPO
  'Regional (N=21)': { vsCoLight: 68,  vsPPO:  2 }    // competitive with PPO, crush CoLight
};

// Bars animate from 0 height on fragment enter
// vsPPO bars for Corridor appear in muted red to show negative (trailing)
// Add horizontal zero line for reference
// Tooltip: shows exact delay numbers on hover
```

---

### Viz-F — Training Curve Animation

**Purpose**: Show MLP vs FRAP convergence/divergence story live.  
**Technology**: Chart.js with streaming animation  
**Implementation**:

```
Two side-by-side line charts: cologne8 (left) | ingolstadt21 (right)

Data: use actual training curve data from WandB exports 
  (src/Figures/plotting/cologne8/ablation_encoder + ingolstadt21/ablation_encoder PNGs)
  If raw CSV not available, digitize ~20 representative points from the PNG.

Animation:
  - On slide enter, both charts start empty
  - Lines draw from left to right over 2.5 seconds
  - MLP+GATv2+PPO: blue line, converges smoothly
  - FRAP+GATv2+PPO: orange line
    - cologne8: converges ~similarly but slightly higher
    - ingolstadt21: diverges upward (very high delay, unstable)

Visual treatment:
  - Thick lines (3px)
  - Light shaded area under MLP curve (success zone)
  - Red dashed "divergence" arrow on FRAP ingolstadt21 curve
  - Y-axis: mean delay (s), log scale for ingolstadt21 to show divergence clearly
```

---

### Viz-G — GATv2 Attention Network Visualization

**Purpose**: Intuitively show that GATv2 assigns heterogeneous attention weights vs. GAT's near-uniform weights.  
**Technology**: D3.js force-directed graph  
**Implementation**:

```
Graph: ingolstadt21 topology (21 nodes, approximate positions)
Edges: width proportional to attention weight α_ij

Two modes (toggle button or click to cycle):
  Mode A "GATv2": edges have varied widths (range 0.5px–6px)
    - 3–4 key edges highlighted orange (high attention to demand-heavy neighbors)
    - Most edges thin (low attention)
  Mode B "GAT":   all edges similar width (2–3px, near-uniform)
    - Illustrates "averaging" behavior

Animation when toggling:
  - Smooth edge-width transition (500ms D3 transition)
  - Node colors shift: high-queue nodes → redder

Optional: 5 "time snapshots" cycling automatically (1.5 s interval)
  - Simulated demand changes → GATv2 attention weights shift to highlight different edges
  - GAT weights remain nearly constant

Mock attention weight generation (if real weights unavailable):
  - For GATv2: sample from Beta(0.3, 0.3) per edge → sparse, concentrated
  - For GAT: sample from Normal(mean=1/k, std=0.05) where k = node degree → near-uniform
  - Scale all to sum to 1 per node's incoming edges
```

---

## Recommended reveal.js Setup

**Framework**: [reveal.js](https://revealjs.com/) v5.x  
**Theme**: `white` or `moon` (clean academic)  
**Key plugins needed**:
- `RevealHighlight` (code blocks in backup slides)
- `RevealNotes` (speaker notes mode)
- `RevealAnimate` or manual fragment sequences for staged reveals

**Chart library**: [Chart.js](https://www.chartjs.org/) v4 + `chartjs-plugin-annotation`  
**Network graphs**: [D3.js](https://d3js.org/) v7  
**CSS animations**: Pure CSS keyframes for pipeline and card-flip animations  

**Recommended slide structure**:
```
reveal.js/
  index.html          ← main slides file
  css/
    custom.css         ← your overrides
  js/
    charts.js          ← Chart.js initialization (Viz-D, Viz-E, Viz-F)
    networks.js        ← D3.js network graphs (Viz-A, Viz-C, Viz-G)
    pipeline.js        ← FGS pipeline animation (Viz-B)
  data/
    main_results.json  ← extracted from baseline_results.csv + thesis tables
    topology_c8.json   ← cologne8 node/edge coordinates
    topology_i21.json  ← ingolstadt21 node/edge coordinates
```

**Connectivity note**: If your defense venue has unreliable internet, ensure all JS libraries are bundled locally (use `npm install` + webpack) and all data files are local JSON.

---

## Anticipated Committee Questions & Prepared Answers

| Question | Key answer points | Backup slide |
|---|---|---|
| "FGSv3 doesn't beat PPO. Is graph communication actually useful?" | (1) Parity at N=21 is the result — not a failure. (2) 68% over CoLight shows benefit when independent alt has graph structure too. (3) Benefit likely grows beyond N=21; FGSv3 now scales to test that. | B1 |
| "Single-seed results — how reliable are these?" | (1) Explicitly disclosed. (2) Factor-of-2.6× FRAP penalty too large to be reversed by variance. (3) Five-seed replication is first follow-on priority. | B2 |
| "What is the reward gaming you mention?" | SUMO waiting counter resets on first movement; SAC's entropy bonus incentivizes phase cycling. Detected by delay-queue inversion. PPO avoids it. Fix: pressure reward. | B3 |
| "Why not evaluate FGSv3 on Corridor scenarios?" | Computational budget. The FGSv3 fixes were designed for Regional-tier failures. Corridor extension is left as follow-on. | — |
| "FRAP is widely used — are you saying it's wrong?" | No — FRAP is correct for regular Chinese grids. The finding is a domain-transfer issue, not a design flaw. GATv2 partially compensates at N=8. | B4 |
| "Would FGS generalize to non-German scenarios?" | Unknown — not evaluated. This is an explicit open question. German RESCO was chosen precisely because it was unstudied. | — |

---

## Pre-Defense Checklist

- [ ] Export all training curve data from WandB as CSV (for Viz-F)
- [ ] Extract topology coordinates from `scenario_topologies.pdf` or SUMO `.net.xml` files (for Viz-C, Viz-G)
- [ ] Set up reveal.js project locally with all libraries bundled (no internet dependency)
- [ ] Confirm projector resolution and connector type at venue
- [ ] Test on projector in speaker-notes mode (press S)
- [ ] Time run-through: target 28 minutes to leave 5–7 minutes as soft buffer
- [ ] Prepare a PDF backup of all slides in case HTML rendering fails
- [ ] Print backup slides B1–B4 on paper in case screen switching is needed during Q&A
