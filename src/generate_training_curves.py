"""
Generate training curve figures and best-validation table for FGS thesis.
Pulls data from W&B project marl-traffic-gat.
Saves PDF figures to src/Figures/.
"""
import os, re, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.ndimage import gaussian_filter1d

warnings.filterwarnings("ignore")

import wandb

# ── Config ──────────────────────────────────────────────────────────────────
ENTITY  = "jv-fuisl-vietnamese-german-university"
PROJECT = "marl-traffic-gat"
OUT     = os.path.join(os.path.dirname(__file__), "Figures")
os.makedirs(OUT, exist_ok=True)

SCENARIOS = ["cologne1", "cologne3", "cologne8",
             "ingolstadt1", "ingolstadt7", "ingolstadt21"]

SCENARIO_LABELS = {
    "cologne1":     "Col. Single ($N=1$)",
    "cologne3":     "Col. Corridor ($N=3$)",
    "cologne8":     "Col. Regional ($N=8$)",
    "ingolstadt1":  "Ing. Single ($N=1$)",
    "ingolstadt7":  "Ing. Corridor ($N=7$)",
    "ingolstadt21": "Ing. Regional ($N=21$)",
}

# ── Method colour / style ────────────────────────────────────────────────────
# dict: method → (colour, linewidth, linestyle, zorder, is_proposed)
METHODS = {
    "FGSv3-SAC":              ("#c0392b", 2.8, "-",  6, True),
    "FGSv3-PPO":              ("#e74c3c", 2.2, "--", 5, True),
    "FGSv2-SAC":              ("#e67e22", 2.2, "-",  5, True),
    "FGS(MLP+GATv2+SAC)":    ("#27ae60", 2.0, "-",  5, True),
    "FGS(MLP+GATv2+PPO)":    ("#2980b9", 2.0, "--", 5, True),
    "FGS(MLP+GAT+SAC)":      ("#16a085", 1.6, "-.", 4, True),
    "FGS(FRAP+GATv2+PPO)":   ("#8e44ad", 1.4, "--", 4, True),
    "FGS(FRAP+GATv2+SAC)":   ("#6d4c41", 1.4, "-.", 4, True),
    "FGS(FRAP+GAT+SAC)":     ("#e91e63", 1.2, ":",  3, True),
    "CoLight":                ("#7f8c8d", 1.4, "--", 3, False),
    "FRAP":                   ("#95a5a6", 1.3, "-.", 3, False),
    "DQN":                    ("#566573", 1.3, "--", 2, False),
    "PPO":                    ("#85929e", 1.3, "-.", 2, False),
    "IndSAC":                 ("#aab7b8", 1.2, ":",  2, False),
    "Fixed Time":             ("#b2babb", 1.0, ":",  1, False),
    "Max Pressure":           ("#d5d8dc", 1.0, ":",  1, False),
}

METHOD_ORDER = list(METHODS.keys())
STATIC_METHODS = {"Fixed Time", "Max Pressure"}

# ── Name → method label ─────────────────────────────────────────────────────
def classify_run(name: str):
    """Return method label or None to skip."""
    n = name.lower()
    for tok in ["average_speed", "nash", "weighted", "dcrnn", "fma2c", "sac_custom"]:
        if tok in n:
            return None

    if n.startswith("resco_"):
        if "__fgsv3_frap_gatv2_sac"  in n: return "FGSv3-SAC"
        if "__fgsv3_frap_gatv2_ppo"  in n: return "FGSv3-PPO"
        if "__fgsv2_sac"             in n: return "FGSv2-SAC"
        if "__fgs_mlp_gatv2_sac"     in n: return "FGS(MLP+GATv2+SAC)"
        if "__fgs_mlp_gatv2_ppo"     in n: return "FGS(MLP+GATv2+PPO)"
        if "__fgs_mlp_gat_sac"       in n: return "FGS(MLP+GAT+SAC)"
        if "__fgs_mlp_gat_ppo"       in n: return "FGS(MLP+GAT+SAC)"
        if "__fgs_frap_gatv2_ppo"    in n: return "FGS(FRAP+GATv2+PPO)"
        if "__fgs_frap_gatv2_sac"    in n: return "FGS(FRAP+GATv2+SAC)"
        if "__fgs_frap_gat_sac"      in n: return "FGS(FRAP+GAT+SAC)"
        if "__fixed_time"            in n: return "Fixed Time"
        if "__static_max_pressure"   in n: return "Max Pressure"
        if "__frap"                  in n: return "FRAP"
        if "__colight"               in n: return "CoLight"
        return None

    m = re.match(r'^(cologne\d+|ingolstadt\d+)__(\w+)__(\w+)$', n)
    if m:
        alg = m.group(2)
        if alg == "dqn":         return "DQN"
        if alg == "ppo":         return "PPO"
        if alg == "colight":     return "CoLight"
        if alg == "frap":        return "FRAP"
        if alg == "sac_builtin": return "IndSAC"
        return None

    if name == "fgsv2_cologne8_default": return "FGSv2-SAC"
    return None


def extract_scenario(run):
    sc = run.config.get("scenario", {})
    if isinstance(sc, dict):
        sc = sc.get("name", "")
    sc = str(sc).lower().replace("resco_", "")
    for s in SCENARIOS:
        if sc == s:
            return s
    nm = run.name.lower().replace("resco_", "")
    for s in SCENARIOS:
        if nm.startswith(s + "__") or nm.startswith(s + "_"):
            return s
    return None


def run_val_wait(r):
    """Lowest validation waiting time from summary."""
    s = dict(r.summary)
    for k in ["validation/resco_wait_mean", "validation/resco/wait"]:
        v = s.get(k)
        if isinstance(v, (int, float)) and not np.isnan(v):
            return float(v)
    return float("inf")


def run_last_episode(r):
    s = dict(r.summary)
    v = s.get("train/episode_index", 0)
    return int(v) if isinstance(v, (int, float)) else 0


def get_summary_metrics(r):
    s = dict(r.summary)
    def pick(*keys):
        for k in keys:
            v = s.get(k)
            if isinstance(v, (int, float)) and not np.isnan(v):
                return round(float(v), 2)
        return None
    return {
        "wait_s":  pick("validation/resco_wait_mean", "validation/resco/wait"),
        "delay_s": pick("validation/resco_delay_mean", "validation/resco/avg_delay"),
        "trip_s":  pick("validation/resco_trip_time_mean", "validation/resco/trip_time"),
        "queue":   pick("validation/resco_queue_mean", "validation/resco/queue"),
    }


# ── Fetch all runs ───────────────────────────────────────────────────────────
print("Connecting to W&B …")
api = wandb.Api(timeout=120)
all_runs = list(api.runs(f"{ENTITY}/{PROJECT}", per_page=300))
print(f"  Total runs fetched: {len(all_runs)}")

catalogue = {}
for r in all_runs:
    method = classify_run(r.name)
    if method is None:
        continue
    sc = extract_scenario(r)
    if sc is None:
        continue
    catalogue.setdefault((sc, method), []).append(r)

print(f"  Unique (scenario, method) pairs: {len(catalogue)}")

# Pick best for TABLE (lowest val_wait, any length)
# Pick best for CURVE (lowest val_wait among runs >= MIN_EP, fallback to any)
MIN_EP = 100  # prefer runs that ran at least this many episodes for curves

best_for_table = {}
best_for_curve = {}

for key, rlist in catalogue.items():
    # Table: absolute best
    best_t = min(rlist, key=run_val_wait)
    best_for_table[key] = best_t

    # Curve: best among long runs, or fallback to any best
    long_runs = [r for r in rlist if run_last_episode(r) >= MIN_EP]
    if long_runs:
        best_c = min(long_runs, key=run_val_wait)
    else:
        best_c = best_t
    best_for_curve[key] = best_c

    vt = run_val_wait(best_t)
    vc = run_val_wait(best_c)
    ep = run_last_episode(best_c)
    same = "=" if best_t.id == best_c.id else f"curve={vc:.1f}s@{ep}ep"
    print(f"  {key[0]:15s} | {key[1]:30s} | table={vt:.1f}s | {same}")

# ── Export best-validation CSV ───────────────────────────────────────────────
rows = []
for (sc, method), r in sorted(best_for_table.items()):
    m = get_summary_metrics(r)
    rows.append({"scenario": sc, "method": method, **m})

df_results = pd.DataFrame(rows)
csv_path = os.path.join(OUT, "best_validation_results.csv")
df_results.to_csv(csv_path, index=False)
print(f"\nSaved results CSV → {csv_path}")

print("\n=== Best validation waiting time (s) ===")
try:
    pivot = df_results.pivot(index="method", columns="scenario", values="wait_s")
    pivot = pivot.reindex(index=[m for m in METHOD_ORDER if m in pivot.index],
                          columns=SCENARIOS)
    print(pivot.to_string(float_format=lambda x: f"{x:.1f}" if pd.notna(x) else "—"))
except Exception as e:
    print(e)

# ── Fetch training histories ─────────────────────────────────────────────────
histories = {}

print("\nFetching training histories …")
for (sc, method), r in best_for_curve.items():
    if method in STATIC_METHODS:
        continue
    try:
        # Fetch ALL history without key filtering (W&B API quirk: specifying keys
        # often returns mostly-NaN frames when columns are logged at different steps)
        h = r.history(samples=5000, pandas=True)
        if "train/resco_wait_mean" not in h.columns:
            print(f"  [no train col] {sc}/{method} ({r.name})")
            continue
        # Keep only rows that have training data
        mask = h["train/resco_wait_mean"].notna()
        if not mask.any():
            print(f"  [all NaN] {sc}/{method} ({r.name})")
            continue
        df = h.loc[mask, ["train/episode_index", "train/resco_wait_mean"]].copy()
        df.columns = ["episode", "wait"]
        df = df.dropna().sort_values("episode").reset_index(drop=True)
        # Remove extreme outliers (> 4× the final stable value, or > 2000s)
        clip = min(2000, df["wait"].quantile(0.98) * 2)
        df = df[df["wait"] <= clip]
        if len(df) < 3:
            print(f"  [< 3 pts] {sc}/{method}")
            continue
        histories[(sc, method)] = df
        print(f"  {sc:15s} | {method:30s} | {len(df):3d} pts, ep=[{df['episode'].min():.0f}–{df['episode'].max():.0f}]")
    except Exception as e:
        print(f"  [error] {sc}/{method}: {e}")

# ── Matplotlib style ─────────────────────────────────────────────────────────
matplotlib.rcParams.update({
    "font.family":       "serif",
    "font.size":         9,
    "axes.labelsize":    9,
    "axes.titlesize":    9.5,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
    "legend.fontsize":   6.8,
    "figure.dpi":        200,
    "pdf.fonttype":      42,
    "ps.fonttype":       42,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

SMOOTH_SIGMA = 4


def plot_scenario(ax, sc, show_legend=True, ylim=None, ncol_legend=1):
    """Plot training curves + static lines for one scenario on ax.
    Returns list of (method_label, handle, is_proposed) for shared legend."""
    avail_methods = [m for m in METHOD_ORDER
                     if (sc, m) in histories or
                        (m in STATIC_METHODS and (sc, m) in best_for_table)]
    legend_handles = []

    for method in avail_methods:
        col, lw, ls, zo, is_proposed = METHODS[method]

        if method in STATIC_METHODS:
            val = run_val_wait(best_for_table[(sc, method)])
            if val == float("inf") or val > 1800:
                continue
            h = ax.axhline(val, color=col, linewidth=1.0, linestyle=":",
                           zorder=zo, alpha=0.75)
            legend_handles.append((method, h, False))

        elif (sc, method) in histories:
            df = histories[(sc, method)]
            x = df["episode"].values.astype(float)
            y = df["wait"].values.astype(float)

            # Faint raw
            ax.plot(x, y, color=col, lw=0.55, alpha=0.14, zorder=zo - 1)
            # Smoothed
            y_sm = gaussian_filter1d(y, sigma=SMOOTH_SIGMA) if len(y) > 5 else y
            h, = ax.plot(x, y_sm, color=col, lw=lw, ls=ls,
                         zorder=zo, alpha=0.93)
            legend_handles.append((method, h, is_proposed))

    ax.set_xlabel("Training Episode", labelpad=2)
    ax.set_ylabel("Mean Waiting Time (s)", labelpad=2)
    ax.set_title(SCENARIO_LABELS.get(sc, sc), pad=4)
    ax.grid(True, alpha=0.22, lw=0.5, color="#888")
    ax.set_xlim(left=0)
    if ylim:
        ax.set_ylim(*ylim)
    else:
        ax.set_ylim(bottom=0)

    if show_legend and legend_handles:
        # Proposed first, then baselines
        legend_handles.sort(key=lambda t: (not t[2],
                                           METHOD_ORDER.index(t[0]) if t[0] in METHOD_ORDER else 99))
        handles = [h for _, h, _ in legend_handles]
        labels  = [n for n, _, _ in legend_handles]
        ax.legend(handles, labels, loc="upper right",
                  framealpha=0.88, edgecolor="#ccc",
                  borderpad=0.5, labelspacing=0.25,
                  handlelength=1.7, ncol=ncol_legend)
    return legend_handles


# ════════════════════════════════════════════════════════════════════════════
# Figure A: Cologne Regional (N=8)
# ════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6.8, 4.2))
plot_scenario(ax, "cologne8", ylim=(0, 180), ncol_legend=2)
ax.set_title("Cologne Regional ($N=8$) — Training Curves", pad=5)
plt.tight_layout(pad=0.8)
out_a = os.path.join(OUT, "training_curves_cologne8.pdf")
plt.savefig(out_a, bbox_inches="tight")
plt.close()
print(f"\nSaved → {out_a}")

# ════════════════════════════════════════════════════════════════════════════
# Figure B: Ingolstadt Regional (N=21)
# ════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6.8, 4.2))
plot_scenario(ax, "ingolstadt21", ylim=(0, 550), ncol_legend=2)
ax.set_title("Ingolstadt Regional ($N=21$) — Training Curves", pad=5)
plt.tight_layout(pad=0.8)
out_b = os.path.join(OUT, "training_curves_ingolstadt21.pdf")
plt.savefig(out_b, bbox_inches="tight")
plt.close()
print(f"Saved → {out_b}")

# ════════════════════════════════════════════════════════════════════════════
# Figure C: Side-by-side regional panel
# ════════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
plot_scenario(ax1, "cologne8",     ylim=(0, 180), show_legend=False)
plot_scenario(ax2, "ingolstadt21", ylim=(0, 550), show_legend=False)
ax1.set_title("Cologne Regional ($N=8$)", pad=4)
ax2.set_title("Ingolstadt Regional ($N=21$)", pad=4)

# Shared legend from cologne8 (most populated)
handles_c8 = []
for m in METHOD_ORDER:
    if ("cologne8", m) in histories or (m in STATIC_METHODS and ("cologne8", m) in best_for_table):
        col, lw, ls, zo, _ = METHODS[m]
        if m in STATIC_METHODS:
            h = mlines.Line2D([], [], color=col, lw=1.0, ls=":", label=m)
        else:
            h = mlines.Line2D([], [], color=col, lw=lw, ls=ls, label=m)
        handles_c8.append(h)

fig.legend(handles=[h for h in handles_c8],
           labels=[h.get_label() for h in handles_c8],
           loc="lower center", ncol=5,
           bbox_to_anchor=(0.5, -0.08),
           framealpha=0.9, edgecolor="#ccc",
           fontsize=7.5, handlelength=2.0, columnspacing=0.9)
plt.tight_layout(pad=0.8, w_pad=2.0)
out_c = os.path.join(OUT, "training_curves_regional.pdf")
plt.savefig(out_c, bbox_inches="tight")
plt.close()
print(f"Saved → {out_c}")

# ════════════════════════════════════════════════════════════════════════════
# Figure D: 2×3 grid — all six scenarios
# ════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()
YLIMS = {
    "cologne1": (0, 80), "cologne3": (0, 150), "cologne8": (0, 180),
    "ingolstadt1": (0, 60), "ingolstadt7": (0, 200), "ingolstadt21": (0, 550),
}
all_handles_dict = {}
for ax, sc in zip(axes, SCENARIOS):
    lh = plot_scenario(ax, sc, ylim=YLIMS.get(sc), show_legend=False)
    for lbl, h, _ in lh:
        if lbl not in all_handles_dict:
            all_handles_dict[lbl] = h

ordered_labels  = [m for m in METHOD_ORDER if m in all_handles_dict]
ordered_handles = [all_handles_dict[m] for m in ordered_labels]
fig.legend(ordered_handles, ordered_labels,
           loc="lower center", ncol=5,
           bbox_to_anchor=(0.5, -0.03),
           framealpha=0.9, edgecolor="#ccc",
           fontsize=7.5, handlelength=2.0, columnspacing=0.9)
fig.suptitle("Training Curves — All RESCO Scenarios", fontsize=11, y=1.01)
plt.tight_layout(pad=1.0, h_pad=2.5, w_pad=1.5)
out_d = os.path.join(OUT, "training_curves_all.pdf")
plt.savefig(out_d, bbox_inches="tight")
plt.close()
print(f"Saved → {out_d}")

print("\nAll done.")
