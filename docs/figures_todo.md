# Figures Checklist — Results & Discussion Chapter

Assessed against `070_Results.tex`. Three tiers:
- **MUST** — absent or absent-and-needed to support a direct claim; reviewer will notice the gap
- **SHOULD** — not referenced yet but the text makes an argument that needs a visual to land
- **NICE** — supplements existing content; raises impact without being critical

---

## ✅ Already exist (verify quality before submission)

- [ ] `Figures/training_curves_regional.pdf` — convergence on cologne8 + ingolstadt21; referenced as `fig:training_curves` (§4.3). Check: smoothed envelope, baseline horizontal dashed lines, FGS variants as thick colored lines.
- [ ] `Figures/ablation_encoder.pdf` — MLP vs. FRAP, fixed GATv2+PPO; referenced as `fig:ablation_encoder` (§4.4).
- [ ] `Figures/ablation_graph.pdf` — GATv2 vs. GAT, fixed MLP+PPO; referenced as `fig:ablation_graph` (§4.4).
- [ ] `Figures/ablation_rl.pdf` — SAC vs. PPO, fixed MLP+GATv2; referenced as `fig:ablation_rl` (§4.4).
- [x] `Figures/fgs_framework.pdf` — TikZ inline diagram of Gen-1 / FGSv2 / FGS final architecture; referenced as `fig:fgs_framework` (§4.5). No external file needed.
- [x] `Figures/system_architecture.pdf` — end-to-end pipeline; referenced as `fig:system_arch` (Ch. 5 / Experimental Design).
- [x] `Figures/scenario_topologies.pdf` — six RESCO network maps; referenced as `fig:scenario_topologies` (Methodology).

> **Note:** `training_curves_all.pdf`, `training_curves_cologne8.pdf`, `training_curves_ingolstadt21.pdf` exist but are **not currently referenced** in the text. Either integrate them or keep as working files.

---

## 🔴 MUST — critical figures missing

### M1 · Main results grouped bar chart
**Section:** §4.1 (Main Results) + §4.2 (Baseline Comparison)  
**Why:** Table 1 has 10 columns × 24 rows. Readers cannot compare methods visually. A grouped bar chart of Mean Waiting Time (Wait↓) per scenario is the primary vehicle for communicating the main contribution.

- [ ] **What to plot:** grouped bars, one group per scenario (cologne1, cologne3, cologne8, ingolstadt1, ingolstadt7, ingolstadt21), bars = methods (FT, MP, DQN, PPO, CoLight, FRAP, FGS_S, FGS_P, FGSv3-PPO). Highlight best FGS per scenario.
- [ ] Data available in `src/Figures/best_validation_results.csv`.
- [ ] Mark `†` (partial) and `‡` (transient) entries with hatching or different marker style, consistent with table conventions.
- [ ] Log-scale y-axis recommended (ingolstadt21 FGS_S is 757 s vs. cologne1 PPO at 4 s).
- [ ] Suggested label: `fig:main_results_bar`
- [ ] Add `\ref{fig:main_results_bar}` cross-reference in §4.1 text after Table 1.

---

### M2 · Scale-dependency benefit plot
**Section:** §4.6.2 (Graph-based coordination and network scale) + §4.7.3 (SQ3 answer)  
**Why:** The text claims "graph communication benefit scales with N and topology heterogeneity." This is the central empirical finding. There is no figure backing it.

- [ ] **What to plot:** x-axis = network scale tier (N=1, N=3/7 corridor, N=8 regional, N=21 regional). y-axis = % improvement in mean Wait of best FGS variant over (a) CoLight and (b) standalone PPO. Two lines, one per baseline.
- [ ] Alternatively: bar chart of absolute Wait for FGS best vs. CoLight vs. PPO at each N, with error annotations.
- [ ] Mark N=1 with annotation "graph module = no-op (no neighbors)."
- [ ] Suggested label: `fig:scale_benefit`
- [ ] Cross-reference at §4.6.2 para "The results support a nuanced view of H1..." and at SQ3 answer.

---

### M3 · Reward gaming diagnostic plot
**Section:** §4.7 (Limitations — "Queue-wait discrepancy and differential-reward gaming")  
**Why:** The text spends ~400 words explaining the queue-wait inconsistency. It is the most complex failure-mode discussion in the thesis. Without a figure, readers must take the claim on faith.

- [ ] **What to plot:** Dual y-axis time series (x = training episode). Left axis: mean waiting time (Wait, s). Right axis: mean queue length (veh./lane). Show early episodes (0–40) for `FGS_P MLP+GATv2+PPO` on cologne1 or cologne3, where the `‡` transient appears.
- [ ] Highlight the episode where best-checkpoint occurs (episode ≤35) with a vertical dashed line.
- [ ] Annotation: "Best-checkpoint Wait ≈ 0.1 s, Queue ≈ 120 veh./lane — physically inconsistent."
- [ ] Suggested label: `fig:reward_gaming`
- [ ] Cross-reference at §4.7, paragraph "Queue-wait discrepancy."
- [ ] Data: requires W&B training trace CSV for cologne3/cologne1 FGS_P early episodes. Check `docs/wandb_results.csv/` subdirectories.

---

## 🟡 SHOULD — strongly reinforces discussion

### S1 · FGS generation improvement trajectory (ingolstadt21)
**Section:** §4.5 (Design Evolution)  
**Why:** Table 4 (`tab:fgs_generation_summary`) lists what changed per generation, but no figure shows the training-curve improvement across generations. The 74% improvement from Gen-1 to FGSv3 is the headline performance number.

- [ ] **What to plot:** Training validation Wait (s) vs. episode for ingolstadt21: Gen-1 FGS_P (88.6 s), FGSv2-SAC (transient ~14 s, stable ~28 s), FGSv3-PPO (converges ~23 s), FGSv3-SAC (transient ~11 s, stable ~26 s). Include DQN and PPO as flat reference lines.
- [ ] Annotate generations with vertical spans or arrows showing "Gen-1 → FGSv2: factored encoder" and "FGSv2 → FGS: demand branch + factored critic."
- [ ] Note: `training_curves_ingolstadt21.pdf` already exists — inspect if it already covers this content; if yes, reference it instead of generating a new file.
- [ ] Suggested label: `fig:generation_improvement`
- [ ] Cross-reference in §4.5 after Table 4.

---

### S2 · Critic input dimension scaling chart
**Section:** §4.6.3 (SAC convergence and network complexity) + Appendix (critic complexity)  
**Why:** The text cites "3,133 dimensions (centralized) vs. 204 dimensions (factored) — a 15× reduction." This is the quantitative argument for scalability. A bar chart makes the bottleneck concrete.

- [ ] **What to plot:** Grouped bars for centralized critic vs. factored critic, x-axis = N (1, 3, 7, 8, 21). Show dimension count per N for each design. Log-scale y-axis.
- [ ] Annotate "OOM threshold" with a horizontal red dashed line where training failed at N=21 (centralized).
- [ ] Formula annotation: "Centralized: O(Nd + NA_max)" vs. "Factored: O(d_c + A_max)".
- [ ] Suggested label: `fig:critic_scaling`
- [ ] Cross-reference at §4.6.3 paragraph "CTDE scalability and the centralization tradeoff."

---

### S3 · Corridor scenario training curves
**Section:** §4.3 (Training Convergence Analysis)  
**Why:** The current convergence figure only covers Regional tier (cologne8, ingolstadt21). Corridor scenarios (cologne3, ingolstadt7) are discussed in §4.2 and §4.7.3 but have no convergence plot. The `‡` transient issue on cologne3 (FGS_P) also merits visualization.

- [ ] **What to plot:** Same format as `training_curves_regional.pdf`. Left panel: cologne3 (N=3) — FGS_S, FGS_P, DQN, PPO, CoLight as baselines. Right panel: ingolstadt7 (N=7) — FGS_P, DQN, PPO, CoLight.
- [ ] Annotate cologne3 FGS_P early-transient best-checkpoint (episode ≤5) with arrow and `‡` marker.
- [ ] Check `training_curves_all.pdf` — it may already contain this content.
- [ ] Suggested label: `fig:training_curves_corridor`
- [ ] Add a sentence in §4.3 referencing this figure alongside `fig:training_curves`.

---

### S4 · Ablation bar chart (companion to Table 3)
**Section:** §4.4 (Ablation Study)  
**Why:** `ablation_encoder/graph/rl.pdf` show training curves; Table 3 shows final numbers. A two-panel bar chart (cologne8 left, ingolstadt21 right) with all ablation variants on x-axis and Wait on y-axis would let readers see the magnitude of each component's contribution at a glance.

- [ ] **What to plot:** x-axis = ablation variant (MLP+GATv2+SAC, MLP+GATv2+PPO, MLP+GAT+PPO, FRAP+GATv2+PPO); two panels per scenario; y-axis = Wait (s).
- [ ] Use color coding consistent with the training-curve plots (same method = same color across all figures).
- [ ] Note: `ablation_cologne8.pdf` and `ablation_ingolstadt21.pdf` already exist — check if they cover this; if they are bar charts, reference them.
- [ ] Suggested label: `fig:ablation_bars`
- [ ] Cross-reference in §4.4 intro paragraph alongside the table.

---

## 🟢 NICE — optional impact boosters

### N1 · FRAP structural mismatch diagram
**Section:** §4.6.1 (FRAP encoding and German intersection geometry)  
**Why:** The text explains why FRAP fails on German intersections (~250 words of explanation). A simple two-panel cartoon — "FRAP works here" (4-phase uniform grid intersection) vs. "FRAP fails here" (6-phase heterogeneous German intersection) — would make this immediately clear.

- [ ] Can be a TikZ diagram (no external data needed).
- [ ] Show phase slots with movement arrows; highlight the "undersaturated competition weight" for a single-movement phase.
- [ ] Suggested label: `fig:frap_mismatch`

---

### N2 · Multi-metric radar chart (best methods on Regional tier)
**Section:** §4.7 (SQ1–SQ4 answers) / conclusion figures  
**Why:** The SQ answers discuss all four metrics (Wait, Delay, Trip, Queue). A spider/radar chart for cologne8 and ingolstadt21, showing 4–5 best methods, gives a holistic at-a-glance comparison that the individual metric columns cannot.

- [ ] Include: FT (outer bound), CoLight, DQN, PPO, FGS_S (cologne8), FGSv3-PPO (ingolstadt21).
- [ ] Normalize each metric to 0–1 (0 = best, 1 = FixedTime baseline).
- [ ] Suggested label: `fig:radar_comparison`

---

### N3 · Attention weight heatmap (future work marker)
**Section:** §4.7.4 (SQ4 tentative answer)  
**Why:** The text explicitly notes "Full attention-weight visualization is left to future work." If attention weights were logged in any W&B run, even a single-step heatmap on the ingolstadt21 topology (edge width ∝ attention weight) would be compelling evidence for SQ4.

- [ ] Check W&B logs for `attn_weights` or `edge_weights` keys in ingolstadt21 FGSv3-PPO runs.
- [ ] If no data: keep as future-work note; do NOT fabricate.
- [ ] If data available: overlay on `scenario_topologies.pdf` ingolstadt21 network map.
- [ ] Suggested label: `fig:attention_heatmap`

---

## Figure consistency checklist (apply to all figures)

- [ ] All figures use the same color palette for the same methods across the chapter (FGS_S = one color, FGS_P = another, CoLight = another, DQN = another, PPO = another).
- [ ] Caption ends with a sentence interpreting the key takeaway (not just describing what is shown).
- [ ] All ablation and training curve figures: faint lines = raw per-episode; bold line = smoothed (Gaussian kernel σ=5 ep), consistent with §4.3 description.
- [ ] Log-scale y-axis used wherever range spans >1 order of magnitude (ingolstadt21 Wait ranges from 11 to 757 s).
- [ ] `†`, `‡`, `*` annotation symbols match table legend definitions exactly.
- [ ] All figures placed with `[htbp]` and `\label` immediately after `\caption`.
- [ ] Font sizes in figures legible at final print size (minimum 9pt equivalent after scaling).
- [ ] All PDF figures generated at vector resolution (no rasterized curves).

---

## Priority summary

| ID | Figure | Priority | Data available |
|----|--------|----------|----------------|
| M1 | Main results grouped bar chart | 🔴 MUST | `best_validation_results.csv` |
| M2 | Scale-dependency benefit plot | 🔴 MUST | `best_validation_results.csv` |
| M3 | Reward gaming diagnostic | 🔴 MUST | Needs W&B training trace (early eps) |
| S1 | Generation improvement trajectory | 🟡 SHOULD | `training_curves_ingolstadt21.pdf` / W&B |
| S2 | Critic dimension scaling chart | 🟡 SHOULD | Computed from formulas in Appendix |
| S3 | Corridor training curves | 🟡 SHOULD | `training_curves_all.pdf` / W&B |
| S4 | Ablation bar chart | 🟡 SHOULD | `best_validation_results.csv` |
| N1 | FRAP mismatch diagram | 🟢 NICE | TikZ only |
| N2 | Multi-metric radar chart | 🟢 NICE | `best_validation_results.csv` |
| N3 | Attention heatmap | 🟢 NICE | Check W&B first |
