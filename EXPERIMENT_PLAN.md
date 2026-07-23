# Episode budgets — hmarl_traffic_control

Derived from eval-reward curves pulled from wandb (`jv-fuisl-vietnamese-german-university/hmarl_traffic_control`, 2026-07-23 audit). Map complexity, not algorithm identity, drives convergence speed.

| Algo | Map | Plateau reached | Budget | vs 1500 | Why |
|---|---|---|---|---|---|
| IPPO | cologne8 | ~ep250–300 | **400** | −73% | −3→−0.4 by ep100, then diminishing returns. |
| MAPPO | cologne8 | ~ep350–400 | **500** | −67% | Steeper early drop (−44→−0.5 by ep400). |
| CoLight | cologne8 | ~ep100 | **300** | −80% | Tight −2.6 to −2.9 plateau by ep100, holds exactly. |
| IPPO | ingolstadt21 | ~ep400–500, never fully flat | **800** | −47% | Settles −40s→−20s by ep400, then oscillates ±10 for the rest of the run. |
| MAPPO | ingolstadt21 | ~ep150–200, never fully flat | **900** | −40% | Early jump, then noisy −5 to −30 swings through ep1500. |
| CoLight | ingolstadt21 | not reached in any run checked (up to ep1050) | **1000**, don't cut further yet | −33% | Baseline oscillates without tightening; k4 runs still improving when they stopped at ep420–440. |
| FMA2C | cologne8, `paperalign_goalfix` recipe | ~ep700–800 | **1000** | −33% | Converges but noisy — use last-200ep moving average, not final episode. |
| FMA2C | ingolstadt21, any recipe | never plateaus at 1500 | **keep full length** | 0% | Recipe-drift problem, not an episode-budget problem — `paperalign_goalfix` was never run here. Cutting episodes just gets a worse number faster. |

## Rules

1. **Checkpoint on best windowed eval, don't hard-stop.** Runs already log `save_best: True` — set `episodes` to the budget above as a ceiling, but report the best checkpoint, not necessarily the last one. Matters most for FMA2C (late-run divergence seen in `ingolstadt21+fma2c+flow_k4`, good window ep1150–1470 then crashed) and anything on ingolstadt21 (never cleanly flat).
2. **ingolstadt21 CoLight and ingolstadt21 FMA2C budgets are unverified** — extrapolated from cologne8 pattern-matching, not confirmed by a full-length curve. Run one full-length pilot per cell before committing the remaining ~15–20 planned runs there to a shortened budget.
