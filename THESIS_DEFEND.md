# Thesis Defense — 30-Minute Presentation Plan

**Title:** FGS: A Modular Graph-Aware Multi-Agent Reinforcement Learning Framework for Traffic Signal Control on German Road Networks
**Format:** 30 min talk + Q&A · ~22 content slides + backup slides
**Golden rule (from supervisor notes):** structure focuses on *your* work — quick related work, no DQN/GNN tutorials, diagrams over text, keep time.

---

## Timing Budget (rehearse against this)

| Block | Slides | Time | Cumulative |
|---|---|---|---|
| 1. Hook + Problem & Motivation | 1–4 | 4:00 | 4:00 |
| 2. Related Work (only what frames the gap) | 5–6 | 2:30 | 6:30 |
| 3. Research Questions | 7 | 1:30 | 8:00 |
| 4. Idea: The FGS Pipeline (own solution) | 8–12 | 7:00 | 15:00 |
| 5. Experimental Setup | 13–14 | 3:00 | 18:00 |
| 6. Results + Demo | 15–20 | 8:30 | 26:30 |
| 7. Answering the RQs + Conclusion | 21–22 | 3:30 | 30:00 |

**Timing discipline:** put a printed cue card with the cumulative column next to the laptop. Checkpoints: slide 7 by minute 8, slide 13 by minute 15, slide 21 by minute 26. If behind at minute 15, compress Setup (slides 13–14) to 90 seconds — the committee has read the thesis; results matter more.

---

# PART 1 — HOOK + PROBLEM & MOTIVATION (4:00)

## Slide 1 — Title (0:30)
**On slide:** Thesis title, your name, supervisors, university logos, date. One full-bleed background image: screenshot of the ingolstadt21 SUMO network rendered as a clean map (use `Figures/scenario_topologies.pdf` cropped, or a sumo-gui screenshot with white background).
**Say:** One sentence: "This thesis asks whether traffic lights that *talk to each other* can control real German road networks better than traffic lights that act alone — and which architectural choices actually matter."

## Slide 2 — The Problem, Visually (1:15)
**Visual (this is your hook — no bullet points at all):**
- **Animation A (build in 2 clicks):** A schematic 3-intersection arterial. Click 1: green wave works, cars flow (animated arrows/GIF). Click 2: one badly timed signal → queue grows backwards and **blocks the upstream intersection** (spillback). Color queue red as it grows.
- Make this in PowerPoint morph / Keynote Magic Move with simple rectangles as cars, or export a 10-second sumo-gui clip of cologne3 under FixedTime (see Asset List, A1).
**Say:** Congestion is not a per-intersection problem. A red phase at one junction blocks vehicles from reaching the next; queues spill back and cascade network-wide. Optimal timing depends on demand that is non-stationary — fixed-time plans designed for *average* demand fail at the tails.

## Slide 3 — Why Existing Control Falls Short (1:00)
**Visual:** Three-column diagram with icons, one line each:
| Fixed-time | Adaptive (SCOOT/SCATS) | RL per intersection |
|---|---|---|
| static plans, average demand | needs dense sensors + expert calibration | learns locally, **ignores neighbors** |
**Say:** Two classical tracks — engineered adaptive systems and learning-based control. Single-agent RL adapts, but each agent optimizing its own local reward ignores upstream/downstream consequences. That is exactly the spillback failure from the previous slide.

## Slide 4 — Motivation: The Three Gaps (1:15)
**Visual:** Three gap cards (icon + max 6 words each):
1. 🗺 **Wrong benchmarks** — MARL-TSC validated on synthetic/Chinese grids, not irregular German networks
2. 🎲 **Missing algorithm** — SAC never systematically tried in graph-aware MARL-TSC
3. 🧩 **Unmapped design space** — encoder × communication × RL never ablated as independent choices
Underneath: a side-by-side image — a regular grid (Hangzhou-style, draw 4×4 lattice) vs. the actual irregular ingolstadt21 topology (`scenario_topologies.pdf`). Caption: "Does coordination that works *here* transfer *here*?"
**Say:** The grid-vs-ingolstadt picture *is* the motivation: regular topology and uniform 8-phase intersections on the left; irregular topology mixing 2-, 4- and 6-phase junctions on the right. Nobody had checked whether graph-based coordination transfers.

---

# PART 2 — RELATED WORK, ONLY WHAT FRAMES THE GAP (2:30)

## Slide 5 — The Landscape in One Table (1:30)
**Visual:** Reuse your thesis design-space table (`tab:pipeline_design_space`) as a graphic — prior methods mapped onto the three modules, with the empty cells highlighted:

| Method | Encoder | Communication | RL |
|---|---|---|---|
| IntelliLight | MLP | — | DQN |
| PressLight | Pressure | — | DQN |
| FRAP | **FRAP** | — | DQN |
| CoLight | MLP | **GAT** | DQN |
| MPLight | Pressure | — | DQN |
| **FGS (this thesis)** | **MLP / FRAP** | **GATv2** | **SAC / PPO / factored critic** |

Highlight with color: every graph method uses GAT+DQN; every phase-aware encoder has *no* communication; the SAC column is empty everywhere. Animate the FGS row appearing last.
**Say:** This one table is my related-work section. Each prior method is a *single point* in a three-dimensional design space. No published work varies all three axes — and no graph-based method has been evaluated on German RESCO scenarios. My thesis fills the marked cells.

## Slide 6 — The Two Directly Relevant Baselines (1:00)
**Visual:** Two panels, one diagram each (no text blocks):
- **FRAP** (reuse `Figures/FRAP.pdf`): phase-competition encoder — assumes each phase = a fixed pair of opposing movements.
- **CoLight**: intersection graph with dot-product attention, *shared* weights across all nodes.
Annotate each with a ⚠ flag: "assumes regular phase structure" / "assumes homogeneous neighbors".
**Say:** Two methods matter for my story because I test their assumptions directly. FRAP encodes a strong prior about phase structure; CoLight's static attention treats all neighbors alike. Both priors were validated on regular Chinese grids. Keep the two ⚠ flags in mind — they come back in the results.

---

# PART 3 — RESEARCH QUESTIONS (1:30)

## Slide 7 — MRQ and Three Sub-Questions (1:30)
**Visual:** MRQ in a single box at top (shortened!), three SQ cards below with icons. **Do not paste the full thesis wording — compress:**

> **MRQ:** Can a modular pipeline — encoder + graph attention + RL algorithm as *independent choices* — deliver competitive, scalable signal control on real German networks? Which choices matter most, at which scale?

- **SQ1 — External validity:** How does FGS compare against classical + deep-RL baselines across three scale tiers?
- **SQ2 — Design space:** How do encoder (MLP vs FRAP) and attention (GAT vs GATv2) affect performance and stability?
- **SQ3 — Scale dependency:** How does each component's benefit change from N=1 to N=21?

**Say:** These three questions structure everything that follows: the architecture is built to answer SQ2, the benchmark to answer SQ1, and the scale tiers to answer SQ3. I return to this slide at the end and answer each one. (Mention hypotheses exist — H1–H4 — but don't read them; keep as backup slide B1.)

---

# PART 4 — IDEA: THE FGS PIPELINE (7:00) ← *the heart of the talk*

## Slide 8 — FGS in One Picture (1:30)
**Visual:** The three-module pipeline diagram (recreate `fig:fgs_pipeline` big and clean):

`SUMO obs xᵢ → [Module I: Encoder] → [Module II: Graph Communication] → [Module III: RL Optimizer] → phase πᵢ`

**Animate module-by-module** (one click each). Under each module, the *swappable options* fade in as chips: I: {MLP, FRAP} · II: {none, GAT, GATv2} · III: {DQN, PPO, SAC}.
**Say:** FGS = Framework for Graph-aware Signal control. Each intersection is an agent. The key idea is *decoupling*: encoder, communication, and RL algorithm are independently pluggable. This is what makes systematic ablation possible — the design space becomes a product of choices, not a fixed architecture. Trained centrally, executed decentrally (CTDE).

## Slide 9 — Module II: What Agents Actually Share (1:30)
**Visual (the coordination intuition — animate):** ingolstadt sub-network with one intersection highlighted. Click 1: queue builds on upstream neighbor (red edge). Click 2: attention arrows from neighbors to the agent, with *thickness = GATv2 attention weight* — the congested neighbor's arrow is thick. Click 3: agent's phase switches to serve the incoming platoon.
**Say:** Each agent aggregates messages from its road-graph neighbors via GATv2 attention. GATv2 vs the older GAT: attention weights depend on *both* sender and receiver features, so two structurally different neighbors get different weights even with similar raw features. On irregular German topologies — where every junction has a unique demand-phase profile — that distinguishability turns out to be decisive. One equation max on the slide (the attention coefficient); no GNN lecture.

## Slide 10 — Not Designed Once — Debugged Into Existence (1:30)
**Visual:** Horizontal timeline of the three generations, styled as a *diagnosis-and-repair* loop (build → evaluate → failure found → fix). Three stations:

`Gen-1 ──✗ scalar bottleneck──▶ FGSv2 ──✗ wrong message + critic OOM──▶ FGS (final)`

Each station: a mini pipeline icon with the *changed module highlighted* and a one-line failure label:
1. **Gen-1:** FRAP scalar output discards per-phase info before the graph sees it
2. **FGSv2:** keep per-phase action tokens → but message encodes phase *rankings*, not *demand*; centralized critic O(N·d) explodes at N=21
3. **FGS final:** demand-aware messages + **factored neighborhood critic O(d_c), independent of N**
**Say (this is your scientific-method moment):** The final architecture wasn't designed on a whiteboard — it was reached through three generations of hypothesis → experiment → diagnosed failure → targeted repair. The modular structure is what made each failure *localizable* to a module interface. This trajectory is itself a contribution.

## Slide 11 — The Scalability Fix: Factored Critic (1:15)
**Visual:** Side-by-side diagram. Left: centralized critic — all 21 agents' observations concatenated into one giant input (draw 21 arrows into one box, label "input dim ≈ 3,133 → **GPU OOM at episode 17**"). Right: factored neighborhood critic — one agent's GATv2-enriched embedding into a small box, label "input dim 204, **O(d_c) — independent of N**". Big annotation: **15× smaller**.
**Say:** The concrete blocker for SAC at 21 agents: the standard centralized critic scales linearly with agent count and simply runs out of memory. The factored critic conditions on the *graph-enriched local embedding* instead of the raw joint observation — neighborhood information still flows in through the communication layer, but the critic input stays constant regardless of network size. This is what let SAC finish training at N=21 at all.

## Slide 12 — Agent Design in 30 Seconds (1:15)
**Visual:** One compact annotated intersection graphic (top-down junction drawing): observation = per-lane density/queue + phase state (highlight lanes); action = pick next phase (show 4 phase diagrams, one highlighted); reward = differential waiting time (small formula: r = W(t−1) − W(t)).
**Say:** For completeness, the MDP interfaces — dwell only 30 seconds: local partial observation, discrete phase selection, dense reward from change in accumulated waiting time. Formally a Dec-POMDP. Remember the reward choice — it comes back in the discussion with an interesting failure mode.

---

# PART 5 — EXPERIMENTAL SETUP (3:00)

## Slide 13 — Six Real German Scenarios, Three Scale Tiers (1:45)
**Visual (map-first, no text):** The six network topologies drawn to relative scale (`scenario_topologies.pdf`), arranged in a 2×3 grid: rows = Cologne / Ingolstadt, columns = **Single (N=1) → Corridor (N=3, 7) → Regional (N=8, 21)**. Each labeled with only name + N. Arrow along columns: "scale tier ↑". Badge: "RESCO benchmark — real demand: TapasCologne (DLR) & InTAS".
**Say:** All six German RESCO scenarios — real road geometry, real demand models, unmodified benchmark files, so results are comparable with published work. The three-tier structure is deliberate: it is the *instrument* for answering SQ3. Each episode = one hour of simulated traffic in SUMO.

## Slide 14 — Protocol & Baselines (1:15)
**Visual:** Two compact panels.
- Left — **7 baselines** as chips grouped: Classical {FixedTime, MaxPressure} · Independent RL {IDQN, IPPO, IndSAC} · Structured {FRAP, CoLight}.
- Right — **protocol** as 4 icon-lines: 200 episodes · eval every 5 episodes on held-out demand seed · best-validation checkpoint · metrics: **mean delay** (primary), waiting time, trip time, throughput.
- Footnote in smaller type, stated honestly out loud: *single seed (seed 0) — resource constrained; results are directional.*
**Say:** Seven baselines spanning classical, independent-RL, and structured methods. Primary metric is mean delay — time lost vs free-flow, robust to reward artefacts. One transparency note up front: these are single-seed runs; I treat differences of a few seconds as trends, not significant rankings. I flag this myself rather than waiting for the committee to ask. Hyperparameters: backup slide B2.

---

# PART 6 — RESULTS + DEMO (8:30)

## Slide 15 — 🎬 DEMO: Watch the Policy Work (1:30)
**Visual (the centerpiece demo):** Side-by-side synced video, ~40–60 s: **FixedTime vs FGSv3-PPO on the same scenario, same demand, same clock** (cologne8 or ingolstadt21 crop). sumo-gui recording with vehicles colored by accumulated waiting time (green→red). Overlay live counters: elapsed time, mean queue. By the end, the FixedTime side has long red queues; FGS side stays green.
See Asset List A1 for exact recording recipe. **Embed the video file in the deck; have a GIF fallback; never rely on a live simulation.**
**Say (over the video, don't talk before it):** Same hour of traffic, same network. Left: the deployed fixed-time plan — watch the queues turn red and spill back. Right: the learned graph-aware policy holding queues short by anticipating incoming platoons. Now let me quantify this.

## Slide 16 — Main Results Across All Scenarios (1:30)
**Visual:** The log-scale grouped bar chart (`main_results_bar.pdf`) — but **decluttered for slides**: keep FixedTime, DQN, PPO, CoLight, best-FGS per scenario; drop the rest to backup B3 (full table). Draw the eye: circle FGS bars; hatch the ‡ gaming artefacts and grey them out.
**Say:** Big picture across all six scenarios. Three patterns: at single intersections everyone converges to similar delay — no room for coordination to help. At corridor scale independent methods hold their own. At regional scale, differences explode — and that's where the interesting science is. Note the hatched bars: physically inconsistent checkpoints I *excluded* — more on that in a minute.

## Slide 17 — Headline: Regional Scale (1:45)
**Visual:** Two clean bar panels, huge numbers, mean delay:
- **ingolstadt21 (N=21):** CoLight 216.8 s → DQN 78.7 s → **FGSv3-PPO 68.4 s** → PPO 67.2 s. Annotate: **−68% vs CoLight · −13% vs DQN · parity with PPO**.
- **cologne8 (N=8):** CoLight 51.8 s → FRAP 44.9 s → **FGS 22.2 s** → PPO 21.9 s. Annotate: **−57% vs CoLight**.
**Say:** The headline. On the largest scenario, FGS beats the *published graph-based* method CoLight by 68% and value-based DQN by 13%, reaching parity with a strong tuned PPO. Two honest readings, and I give both: graph-aware FGS dominates the *other graph method* decisively — CoLight's static attention doesn't transfer to irregular German topologies (remember the ⚠ from slide 6) — but it does not yet *surpass* the best independent baseline. Why that is still a positive result: first-generation FGS scored 234.9 s here; the architecture repairs recovered 71%. And the ablation tells us exactly which components did it.

## Slide 18 — Ablation I: Encoder & Attention (both ⚠ flags cash out) (1:45)
**Visual:** Two panels, each a training-curve pair (from `ablation_encoder` and `ablation_graph` figures, ingolstadt21 side), each with one huge takeaway number:
- **MLP vs FRAP encoder:** FRAP diverges at N=21 — **2.6× worse delay** (617 vs 235 s). Inset cartoon: a German 3-phase junction with a turn-only lane vs FRAP's assumed opposing-pair template → mismatch ⚡.
- **GATv2 vs GAT:** **53% lower delay** at N=21 (234.9 vs 492.0 s); ~no difference at N=8. Inset: attention weights drawn as arrows — GAT nearly uniform, GATv2 sharply focused.
**Say:** This is the design-space payoff — the two assumptions from the related-work slide, tested. First: FRAP's phase-competition prior *assumes* every phase controls an opposing pair of movements. German junctions with 2/4/6-phase mixes violate this; the encoding emits near-zero features for single-movement phases — the agent literally can't see demand — and the penalty *grows with scale* as more mismatched junctions join. FRAP was adopted across the literature without topology validation; this is a finding of independent interest. Second: dynamic per-edge attention (GATv2) only matters where neighbors are heterogeneous — irrelevant at N=8, worth 2× at N=21.

## Slide 19 — Ablation II: RL Algorithm + An Honest Failure Mode (1:30)
**Visual:** Left: SAC vs PPO bars on cologne8 (22.2 vs 24.0 s → "SAC +8% at moderate scale, *if* the critic scales"). Right — **the reward-gaming diagnostic** (`delay_queue_diagnostic_combined_40ep`): dual-axis plot where SAC's "best" checkpoint shows *anomalously low delay + huge queue* — circle the impossible pair, big label **"too good to be true → excluded ‡"**.
**Say:** Algorithm choice is conditional: SAC's off-policy replay wins at moderate scale but needed the factored critic to even run at N=21. And here is the discussion point I most want to share: SAC discovered *reward hacking*. SUMO's waiting-time counter pauses the moment a vehicle moves — so rapid phase cycling nudges every lane briefly, harvesting reward while queues actually grow. SAC's entropy bonus *doubly* rewards this cycling. I caught it because delay and queue told contradictory stories — a physical-consistency check — and I excluded those checkpoints rather than reporting them as wins. PPO is structurally immune: on-policy updates immediately see the queue blow-up. Fix for future work: pressure-based reward.

## Slide 20 — The Central Finding: Benefit Grows with Scale (0:30)
**Visual:** The scale-benefit chart (`scale_benefit.pdf`): x = N (1 → 3/7 → 8/21), y = % delay improvement of best FGS over CoLight (filled) and over PPO (outline). The CoLight curve rises from ~0 to 68%. One line under it: **"Coordination pays where local observation ends (N ≳ 8)."**
**Say:** One chart summarizing the thesis: graph communication is a no-op at one intersection, unnecessary at corridor scale where local sensing suffices, and decisive at regional scale where congestion propagates beyond any single agent's horizon. (Optionally mention the MFD analysis connects this to traffic-flow theory — backup B5.)

---

# PART 7 — ANSWERS + CONCLUSION (3:30)

## Slide 21 — Back to the Research Questions (2:00)
**Visual:** The same three SQ cards from slide 7, now each stamped with a verdict + one number (visual callback — the committee sees the loop close):
- **SQ1 ✓** Competitive at scale: −68% vs CoLight, −13% vs DQN, parity with PPO on ingolstadt21; envelope grows with N.
- **SQ2 ✓** Encoder is the dominant choice (FRAP mismatch up to 2.6×); GATv2 > GAT only at scale (53%); SAC > PPO at N≤8 but needs the factored critic and a gaming-proof reward.
- **SQ3 ✓** Component benefits are scale-gated: threshold for consistent graph advantage ≈ N = 8–21 on German topologies.
- **MRQ:** *Yes — competitive and scalable*, with priority order: ① encoder–topology compatibility ② attention expressiveness ③ critic scalability.
**Say:** Walk each card in ~25 s. Phrase the MRQ answer as the thesis's takeaway design guideline for anyone building MARL-TSC on European networks.

## Slide 22 — Contributions & Future Work (1:30)
**Visual:** Left: four contribution tiles — **Framework** (open-source SUMO/RLlib/PyG stack) · **Algorithmic** (3-generation FGS, factored O(d_c) critic) · **Empirical** (first graph-MARL evaluation on all 6 German RESCO scenarios, 7 baselines) · **Analytical** (design guidelines; FRAP-transfer negative result). Right: three future-work arrows: pressure-based reward · multi-seed validation (top priority) · hierarchical scaling beyond N=21 + attention interpretability. Close with the title-slide network image + "Thank you".
**Say:** End on the analytical contribution — the field gets reusable *design guidelines*, not just one more architecture. Name multi-seed validation yourself as the first follow-on step (it defuses the question). Last sentence, memorized: "Coordination between traffic lights pays off exactly where a single intersection can no longer see the whole problem — and FGS shows how to build for that, one diagnosed failure at a time." Thank the committee; invite questions.

---

# BACKUP SLIDES (have ready, don't present)

- **B1 — Hypotheses H1–H4 with verdicts** (H1 partial support; H2 confirmed in selected scenarios; H3 confirmed; H4 confirmed) — for "what were your hypotheses?"
- **B2 — Full hyperparameter tables** (`tab:hyperparams`, `tab:arch_params`) — for reproducibility questions.
- **B3 — Full main-results table** (all 10 methods × 6 scenarios, four metrics pointer) with †/‡ legend.
- **B4 — Dec-POMDP formalization + reward equation** — for the formal-definition question.
- **B5 — MFD plot** (`resco_ingolstadt21_mfd_density_flow`): FGSv3-PPO stays on the high-flow branch — the traffic-engineering interpretation.
- **B6 — Training/validation curves regional** (`fgs_versions_..._train_validation_delay_200ep`) — for overfitting/convergence questions (FGS_P train 78 s vs val 234.9 s gap; FGSv3-PPO stable from ep. 7).
- **B7 — Factored critic math**: input-dim derivation 3,133 → 204; why FGSv2→FGSv3 changed two things at once and can't be decomposed (pre-empts the sharpest methodological question).
- **B8 — GATv2 vs GAT equation difference** (static vs dynamic attention, Brody et al.) — only if a committee member digs in.
- **B9 — Why best-validation checkpoint selection** (Henderson et al.; optimistic bound; conservative alternative = mean of last 10 checkpoints).
- **B10 — Limitations summary** (single seed · reward gaming · SAC variance at N=21 · train→val demand shift) — shows you know them cold.

## Likely Committee Questions → Where the Answer Lives
| Question | Answer strategy |
|---|---|
| "FGS only ties PPO — why is this a contribution?" | Slide 17 framing + B7: goal was *characterizing the design space* (MRQ), not leaderboard; 71% recovered via diagnosis-and-repair; decisive win over the graph-based SOTA; guidelines generalize. |
| "Single seed — how do I trust anything?" | You flagged it on slide 14. Ablation *magnitudes* (2.6×, 2.1×) dwarf seed noise; 3–4 s differences explicitly called trends; multi-seed = named top priority. |
| "Isn't excluding ‡ checkpoints cherry-picking?" | Inverse: it's *anti*-cherry-picking — excluded results that *flattered* FGS because they were physically impossible (queue-delay inversion). Objective criterion, applied uniformly. |
| "Why didn't you fix the reward instead?" | Root cause found late in the trajectory; fixing mid-study breaks comparability with RESCO baselines; pressure reward is the stated next step. |
| "Why no FGSv3 on corridor tier?" | Prioritized the Regional tier where the scalability claim lives; corridor already showed independent methods suffice at N≤7 (scale argument makes it low-information). |
| "Two changes at once in FGSv2→v3?" | Concede directly (thesis says it): contributions not decomposable from current data; partial ablation named as follow-on. Honesty > defensiveness. |

---

# ASSET PRODUCTION CHECKLIST

**A1 — Hero demo video (slide 15) — highest priority**
1. Run evaluation rollouts in `sumo-gui` for (a) FixedTime and (b) FGSv3-PPO best checkpoint, same scenario + demand seed.
2. In sumo-gui: Edit → Edit Visualisation → color vehicles by *accumulated waiting time* (green→yellow→red); hide POIs; white background; delay ~50 ms.
3. Record with OBS / `ffmpeg -f x11grab` (or sumo-gui screenshot-per-step → `ffmpeg -framerate 30` stitch). Speed up 10–20× so one sim-hour ≈ 45 s.
4. Compose side-by-side: `ffmpeg -i fixed.mp4 -i fgs.mp4 -filter_complex hstack out.mp4`; add labels + running clock.
5. Export a GIF fallback; test playback on the *presentation machine and projector*.
   *Fallback if rendering fails: three timestamped screenshots (t = 10/30/50 min) side by side — still beats no visual.*

**A2 — Spillback hook animation (slide 2):** PowerPoint morph with rectangles, or trim a FixedTime cologne3 clip from the A1 pipeline.

**A3 — Attention animation (slide 9):** static network figure + arrows whose width you animate in 3 clicks; if trained attention weights are loggable, use a real snapshot (stronger in Q&A: "these are learned weights, not a cartoon").

**A4 — Re-export thesis charts for slides:** white background, font ≥ 18 pt equivalent, thicker lines, *max 4–5 series* per chart (full versions → backup). Keep method colors identical across every slide (one legend, learned once). Sources: `main_results_bar`, `scale_benefit`, `ablation_encoder`, `ablation_graph`, `delay_queue_diagnostic_combined_40ep`, `fgs_versions_ingolstadt21_validation_4metrics_200ep`.

**A5 — Diagrams to draw fresh (don't screenshot the PDF):** pipeline (slide 8), generation timeline (slide 10), centralized-vs-factored critic (slide 11), grid-vs-ingolstadt comparison (slide 4).

---

# DELIVERY RULES (mapped to the supervisor's "common mistakes")

1. **Time:** rehearse 3× full runs; target 28 min so you land ≤30 with adrenaline. Cue-card checkpoints at slides 7 / 13 / 21. Pre-planned cut if late: compress slides 13–14; *never* cut slides 17–19 (the contribution).
2. **No text blocks:** every slide above is specified visual-first; hard cap ~20 words of prose per slide. If a slide can't be drawn, it's a speaker note, not a slide.
3. **Diagrams and charts:** every results claim has exactly one chart with one circled takeaway number. One idea per slide.
4. **Formatting & demos:** one template, one font, one persistent method-color mapping; video embedded + GIF fallback + screenshot fallback; test on the actual room hardware the day before.
5. **Focus on YOUR work:** related work = 2 slides / 2.5 min; background theory = 0 slides (Dec-POMDP and GATv2 equations live in backup). Method + results + answers = 19 of 30 minutes.
6. **Scientific approach on display:** the narrative arc is gap → questions → designed instrument (modular pipeline + scale tiers) → iterate via diagnosed failures → quantified ablation → answered questions → stated limits. Say the words "to answer SQ2…" when introducing the ablation — make the committee *hear* the method.
