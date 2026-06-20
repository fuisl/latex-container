"""Generate publication-quality training curve figures for the FGS thesis."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.ndimage import gaussian_filter1d

import wandb

E = "jv-fuisl-vietnamese-german-university"
P = "marl-traffic-gat"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Figures")
os.makedirs(OUT, exist_ok=True)

TW = "train/resco_wait_mean"
VW = "validation/resco_wait_mean"

# ── Design spec ──────────────────────────────────────────────────────────────
# (color, linewidth, linestyle, zorder, label)
STYLE = {
    "FGSv3-SAC":           ("#c0392b", 2.5, "-",  6, "FGSv3-SAC (Proposed)"),
    "FGSv2-SAC":           ("#e67e22", 2.2, "-",  5, "FGSv2-SAC (Proposed)"),
    "FGSv3-PPO":           ("#27ae60", 2.2, "--", 5, "FGSv3-PPO (Proposed)"),
    "FGS_S":               ("#2980b9", 1.8, "-.",  4, "FGS(MLP+GATv2+SAC)"),
    "FGS_P":               ("#8e44ad", 1.8, ":",  4, "FGS(MLP+GATv2+PPO)"),
    "PPO":                 ("#7f8c8d", 1.3, "--", 3, "PPO (baseline)"),
    "DQN":                 ("#95a5a6", 1.3, "-.", 3, "DQN (baseline)"),
    "CoLight":             ("#bdc3c7", 1.0, ":", 2, "CoLight (baseline)"),
    "FRAP":                ("#c8d6e5", 1.0, ":", 2, "FRAP (baseline)"),
    "Fixed Time":          ("#d5dbdb", 1.0, ":", 1, "Fixed Time"),
    "Max Pressure":        ("#eaeded", 1.0, ":", 1, "Max Pressure"),
}

# Static baseline best-val values (for horizontal lines)
STATIC = {
    "cologne8": {
        "PPO":        4.25,
        "DQN":        6.43,
        "CoLight":    11.02,
        "FRAP":       13.93,
        "Fixed Time": 30.27,
        "Max Pressure": 159.54,
    },
    "ingolstadt21": {
        "PPO":        25.34,
        "DQN":        33.78,
        "CoLight":    95.21,
        "FRAP":       50.98,
        "Fixed Time": 96.38,
        "Max Pressure": 68.35,
    },
}

# Key runs to fetch training history from
KEY_RUNS = {
    "cologne8": {
        "FGSv3-PPO": "73f4ilpr",
        "FGSv3-SAC": "3efrqs9n",
        "FGSv2-SAC": "fm7rg86a",
        "FGS_S":     "m0pvd51d",
        "FGS_P":     "5qnfc0c0",
    },
    "ingolstadt21": {
        "FGSv3-SAC": "76dz4us4",
        "FGSv2-SAC": "4pn2fg93",
        "FGSv3-PPO": "iwd3hutz",
        "FGS_P":     "b04863fh",
    },
}

api = wandb.Api(timeout=120)

def fetch_history(run_id):
    """Fetch training history; return DataFrame with [episode, wait]."""
    r = api.run(f"{E}/{P}/{run_id}")
    hist = r.history(samples=500, pandas=True)
    if TW not in hist.columns:
        return None
    df = hist[[TW]].copy()
    df["episode"] = np.arange(len(df))
    df = df.rename(columns={TW: "wait"}).dropna(subset=["wait"])
    df = df[df["wait"] < 9000]
    return df

def smooth(y, sigma=5):
    if len(y) < 4:
        return y
    return gaussian_filter1d(y.astype(float), sigma=sigma)

# ── Matplotlib style ─────────────────────────────────────────────────────────
matplotlib.rcParams.update({
    "font.family":       "serif",
    "font.size":         9,
    "axes.labelsize":    9,
    "axes.titlesize":    10,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
    "legend.fontsize":   7.5,
    "figure.dpi":        180,
    "pdf.fonttype":      42,
    "ps.fonttype":       42,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.25,
    "grid.linewidth":    0.5,
})

SIGMA = 5

def plot_scenario(ax, sc, ylim=None, show_legend=True, title=None):
    handles_labels = []

    # Collect training runs
    for method, run_id in KEY_RUNS.get(sc, {}).items():
        col, lw, ls, zo, lbl = STYLE[method]
        df = fetch_history(run_id)
        if df is None or len(df) < 3:
            continue
        x = df["episode"].values
        y = df["wait"].values
        # Raw (very faint)
        ax.plot(x, y, color=col, lw=0.5, alpha=0.12, zorder=zo - 1)
        # Smoothed
        ys = smooth(y, SIGMA)
        h, = ax.plot(x, ys, color=col, lw=lw, ls=ls, zorder=zo, alpha=0.95)
        handles_labels.append((lbl, h, True, method))

    # Static baselines — horizontal lines at best-val
    # (don't repeat PPO/DQN if they appear as training runs)
    training_methods = set(KEY_RUNS.get(sc, {}).keys())
    for bname, bval in STATIC.get(sc, {}).items():
        if bname in training_methods:
            continue  # already drawn as training curve
        col, lw, ls, zo, lbl = STYLE[bname]
        h = ax.axhline(bval, color=col, lw=lw, ls=ls, zorder=zo, alpha=0.7)
        handles_labels.append((lbl, h, False, bname))

    # Style
    ax.set_xlabel("Training Episode")
    ax.set_ylabel("Mean Waiting Time (s)")
    if title:
        ax.set_title(title, pad=5)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_xlim(left=0)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.0f"))

    if show_legend and handles_labels:
        # Proposed first, then baselines
        handles_labels.sort(key=lambda x: (not x[2],
            list(STYLE.keys()).index(x[3]) if x[3] in STYLE else 99))
        ax.legend([h for _, h, _, _ in handles_labels],
                  [l for l, _, _, _ in handles_labels],
                  loc="upper right", framealpha=0.9,
                  edgecolor="#cccccc", borderpad=0.6,
                  labelspacing=0.3, handlelength=2.0, ncol=1)
    return handles_labels

# ════════════════════════════════════════════════════════════════════════════
# Figure 1: Cologne Regional (N=8)
# ════════════════════════════════════════════════════════════════════════════
print("Generating cologne8 figure…")
fig, ax = plt.subplots(figsize=(6.5, 4.2))
plot_scenario(ax, "cologne8", ylim=(0, 180),
              title="Cologne Regional ($N=8$) — Training Convergence")
plt.tight_layout(pad=0.8)
p = os.path.join(OUT, "training_curves_cologne8.pdf")
plt.savefig(p, bbox_inches="tight"); plt.close()
print(f"  → {p}")

# ════════════════════════════════════════════════════════════════════════════
# Figure 2: Ingolstadt Regional (N=21)
# ════════════════════════════════════════════════════════════════════════════
print("Generating ingolstadt21 figure…")
fig, ax = plt.subplots(figsize=(6.5, 4.2))
plot_scenario(ax, "ingolstadt21", ylim=(0, 600),
              title="Ingolstadt Regional ($N=21$) — Training Convergence")
plt.tight_layout(pad=0.8)
p = os.path.join(OUT, "training_curves_ingolstadt21.pdf")
plt.savefig(p, bbox_inches="tight"); plt.close()
print(f"  → {p}")

# ════════════════════════════════════════════════════════════════════════════
# Figure 3: Side-by-side two-panel
# ════════════════════════════════════════════════════════════════════════════
print("Generating combined figure…")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))

hl1 = plot_scenario(ax1, "cologne8", ylim=(0, 180), show_legend=False,
                    title="(a) Cologne Regional ($N=8$)")
hl2 = plot_scenario(ax2, "ingolstadt21", ylim=(0, 600), show_legend=False,
                    title="(b) Ingolstadt Regional ($N=21$)")

# Shared legend under panels
all_hl = {}
for lbl, h, isp, meth in (hl1 + hl2):
    if meth not in all_hl:
        all_hl[meth] = (lbl, h, isp)
ordered = sorted(all_hl.items(),
    key=lambda x: (not x[1][2], list(STYLE.keys()).index(x[0]) if x[0] in STYLE else 99))
fig.legend([h for _, (_, h, _) in ordered],
           [lbl for _, (lbl, _, _) in ordered],
           loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.07),
           framealpha=0.9, edgecolor="#cccccc",
           fontsize=8, handlelength=2.2, columnspacing=1.2)

plt.tight_layout(pad=0.8, w_pad=2.0)
plt.subplots_adjust(bottom=0.18)
p = os.path.join(OUT, "training_curves_regional.pdf")
plt.savefig(p, bbox_inches="tight"); plt.close()
print(f"  → {p}")

print("\nAll figures saved.")
