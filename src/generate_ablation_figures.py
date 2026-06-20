"""
Generate ablation study figures using validation history fetched from W&B.
Data is embedded directly (fetched via MCP tool, W&B Python API not available).
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Figures")

# ── Matplotlib style ──────────────────────────────────────────────────────────
matplotlib.rcParams.update({
    "font.family":       "serif",
    "font.size":         9,
    "axes.labelsize":    9,
    "axes.titlesize":    10,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
    "legend.fontsize":   8,
    "figure.dpi":        200,
    "pdf.fonttype":      42,
    "ps.fonttype":       42,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.22,
    "grid.linewidth":    0.5,
})

# ── Fetched validation history (episode_index, resco_delay_mean) ──────────────
HISTORIES = {
    # ── Cologne Regional (N=8) ────────────────────────────────────────────────
    "c8_mlp_gatv2_sac": {
        "label": "MLP+GATv2+SAC", "color": "#1f77b4", "ls": "-",
        "ep":    [5, 10, 15, 20, 25, 30, 35, 40, 45],
        "delay": [978.5, 706.0, 80.8, 73.5, 24.0, 23.7, 22.2, 23.2, 23.5],
    },
    "c8_mlp_gatv2_ppo": {
        "label": "MLP+GATv2+PPO", "color": "#ff7f0e", "ls": "--",
        "ep":    [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,
                  105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,
                  180,185,190,195,200],
        "delay": [187.2, 877.5, 654.3, 167.3, 234.0, 91.8, 418.0, 144.0, 29.4,
                  86.1, 29.1, 46.0, 43.2, 30.5, 25.5, 24.8, 26.4, 28.1, 26.3,
                  25.7, 25.9, 25.1, 72.4, 25.2, 25.5, 24.0, 24.9, 26.2, 30.0,
                  25.4, 24.9, 24.2, 24.9, 24.7, 24.5, 32.7, 25.4, 485.2, 512.1,
                  26.7],
    },
    "c8_mlp_gat_ppo": {
        "label": "MLP+GAT+PPO", "color": "#2ca02c", "ls": "-.",
        "ep":    [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,
                  105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,
                  180,185,190,195,200],
        "delay": [369.2, 379.9, 53.1, 134.5, 31.9, 247.5, 201.9, 30.3, 27.8,
                  26.5, 25.8, 26.8, 26.8, 27.7, 25.3, 262.6, 33.4, 27.7, 30.5,
                  27.5, 27.8, 27.2, 26.2, 26.2, 25.8, 25.6, 26.8, 25.1, 25.5,
                  25.0, 25.3, 25.2, 26.7, 26.8, 26.1, 26.7, 426.0, 27.1, 26.0,
                  24.9],
    },
    "c8_frap_gatv2_ppo": {
        "label": "FRAP+GATv2+PPO", "color": "#d62728", "ls": ":",
        "ep":    [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,
                  105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,
                  180,185,190,195,200],
        "delay": [1043.4, 882.9, 882.9, 882.9, 800.9, 837.8, 756.8, 800.9, 800.9,
                  756.8, 800.9, 756.8, 756.8, 635.6, 480.1, 136.8, 176.7, 229.9,
                  111.4, 356.0, 296.4, 29.6, 171.8, 334.1, 246.2, 260.2, 292.1,
                  95.6, 42.8, 38.3, 39.0, 51.5, 132.4, 64.2, 37.9, 55.7, 25.7,
                  24.6, 28.6, 29.0],
    },
    # ── Ingolstadt Regional (N=21) ────────────────────────────────────────────
    "i21_mlp_gatv2_ppo": {
        "label": "MLP+GATv2+PPO", "color": "#ff7f0e", "ls": "--",
        "ep":    [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,
                  105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,
                  180,185,190,195,200],
        "delay": [781.1,845.8,1153.9,996.1,1056.4,1152.6,956.0,963.8,441.8,
                  1142.3,1208.2,1200.6,1080.5,1096.1,1204.1,1022.4,1081.6,
                  1073.9,1091.7,880.8,792.7,953.8,784.2,596.7,365.5,333.6,
                  412.2,386.8,529.1,840.6,490.6,288.7,355.6,259.7,348.8,
                  246.3,297.2,299.7,234.9,288.3],
    },
    "i21_mlp_gat_ppo": {
        "label": "MLP+GAT+PPO", "color": "#2ca02c", "ls": "-.",
        "ep":    [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,
                  105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,
                  180,185,190,195,200],
        "delay": [1250.6,1184.2,1001.1,986.0,857.6,1133.0,724.2,1091.0,758.1,
                  770.5,759.3,938.3,813.6,625.2,985.5,1083.5,821.3,1057.0,
                  812.7,951.9,947.6,853.5,956.2,879.3,1019.1,940.5,1014.4,
                  1113.9,1082.0,749.0,726.6,786.6,910.9,570.4,541.7,492.0,
                  704.2,830.7,657.8,749.2],
    },
    "i21_frap_gatv2_ppo": {
        "label": "FRAP+GATv2+PPO", "color": "#d62728", "ls": ":",
        "ep":    [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,
                  105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,
                  180,185,190,195,200],
        "delay": [1529.3,1417.7,1452.3,1384.6,1338.4,949.6,1326.8,1358.4,
                  1100.1,1337.6,1187.0,1389.9,1273.9,1347.5,1290.3,1358.2,
                  1296.8,1261.0,1309.7,1403.3,1096.4,907.5,1224.3,1047.2,
                  1113.3,894.9,1240.6,1232.3,1237.5,1291.4,1086.0,1337.5,
                  1008.5,1223.3,1331.8,948.3,723.3,883.4,1148.4,617.0],
    },
    "i21_mlp_gatv2_sac": {
        "label": "MLP+GATv2+SAC (terminated)", "color": "#1f77b4", "ls": "-",
        "ep":    [5, 10, 15],
        "delay": [1201.8, 1383.0, 1274.9],
    },
}

COLOGNE8_IDS  = ["c8_mlp_gatv2_sac", "c8_mlp_gatv2_ppo", "c8_mlp_gat_ppo", "c8_frap_gatv2_ppo"]
ING21_IDS     = ["i21_mlp_gatv2_sac", "i21_mlp_gatv2_ppo", "i21_mlp_gat_ppo", "i21_frap_gatv2_ppo"]

# ── Best-validation metrics table (from W&B summary) ─────────────────────────
BEST_VAL = {
    "c8_mlp_gatv2_sac":  {"wait": 4.93,   "delay": 22.20,  "trip": 86.42,  "queue": 0.34},
    "c8_mlp_gatv2_ppo":  {"wait": 6.25,   "delay": 24.02,  "trip": 88.31,  "queue": 0.44},
    "c8_mlp_gat_ppo":    {"wait": 6.72,   "delay": 24.89,  "trip": 89.11,  "queue": 0.47},
    "c8_frap_gatv2_ppo": {"wait": 6.69,   "delay": 24.62,  "trip": 88.88,  "queue": 0.47},
    "i21_mlp_gatv2_ppo": {"wait": 88.60,  "delay": 234.93, "trip": 253.49, "queue": 2.58},
    "i21_mlp_gat_ppo":   {"wait": 261.21, "delay": 491.96, "trip": 406.64, "queue": 4.93},
    "i21_frap_gatv2_ppo":{"wait": 460.66, "delay": 617.00, "trip": 614.76, "queue": 7.77},
    "i21_mlp_gatv2_sac": {"wait": 757.47, "delay": 1201.80,"trip": 875.24, "queue": 13.48},
}

# Print the metrics table
print("=" * 72)
print(f"{'Variant':36s} {'Wait':>7} {'Delay':>8} {'Trip':>7} {'Queue':>7}")
print("-" * 72)
for sc_label, ids in [("Cologne Regional (N=8)", COLOGNE8_IDS),
                       ("Ingolstadt Regional (N=21)", ING21_IDS)]:
    print(f"\n{sc_label}")
    for rid in ids:
        m = BEST_VAL[rid]
        lbl = HISTORIES[rid]["label"]
        print(f"  {lbl:34s} {m['wait']:>7.2f} {m['delay']:>8.2f} {m['trip']:>7.2f} {m['queue']:>7.2f}")
print("=" * 72)

# ── Plot helpers ──────────────────────────────────────────────────────────────
WINDOW = 10   # episodes either side for centred running average

def _running_avg(arr, window=WINDOW):
    arr = np.asarray(arr, dtype=float)
    out = np.empty_like(arr)
    half = window // 2
    for i in range(len(arr)):
        s = max(0, i - half)
        e = min(len(arr), i + half + 1)
        out[i] = arr[s:e].mean()
    return out


def _draw(ax, rid):
    h = HISTORIES[rid]
    eps   = np.array(h["ep"])
    delay = np.array(h["delay"])
    color, ls, label = h["color"], h["ls"], h["label"]
    # raw data — very faint so spikes are visible but don't dominate
    ax.plot(eps, delay, color=color, lw=0.6, alpha=0.18, zorder=1)
    if len(eps) >= 4:
        trend = _running_avg(delay)
        ax.plot(eps, trend, color=color, ls=ls, lw=1.9,
                label=label, alpha=0.92, zorder=2)
    else:
        # Too few points — draw markers only
        ax.plot(eps, delay, color=color, ls=ls, lw=1.6, marker="x",
                label=label, alpha=0.85, zorder=2)


def single_plot(run_ids, title, ylim=None, out_path=None):
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    for rid in run_ids:
        _draw(ax, rid)
    ax.set_xlabel("Training episode")
    ax.set_ylabel("Validation mean delay (s)")
    ax.set_title(title)
    ax.legend(loc="upper right")
    if ylim:
        ax.set_ylim(ylim)
    ax.set_xlim(left=0)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=6))
    fig.tight_layout()
    if out_path:
        fig.savefig(out_path, bbox_inches="tight")
        print(f"Saved: {out_path}")
    plt.close(fig)


def pair_plot(left_ids, right_ids, titles, ylims=(None, None), out_path=None):
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8))
    for ax, rids, title, ylim in zip(axes, [left_ids, right_ids], titles, ylims):
        for rid in rids:
            _draw(ax, rid)
        ax.set_xlabel("Training episode")
        ax.set_title(title, fontsize=10)
        ax.legend(fontsize=8, loc="upper right")
        if ylim:
            ax.set_ylim(ylim)
        ax.set_xlim(left=0)
        ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=5))
    axes[0].set_ylabel("Validation mean delay (s)")
    fig.tight_layout()
    if out_path:
        fig.savefig(out_path, bbox_inches="tight")
        print(f"Saved: {out_path}")
    plt.close(fig)


# ── 1. All-variants per scenario ──────────────────────────────────────────────
single_plot(
    COLOGNE8_IDS,
    title="Cologne Regional ($N=8$) — ablation variants",
    ylim=(0, 100),
    out_path=os.path.join(OUT, "ablation_cologne8.pdf"),
)

single_plot(
    ING21_IDS,
    title="Ingolstadt Regional ($N=21$) — ablation variants",
    ylim=(0, 1600),
    out_path=os.path.join(OUT, "ablation_ingolstadt21.pdf"),
)

# ── 2. Pair A — Encoder: MLP vs FRAP (fixed GATv2+PPO) ──────────────────────
pair_plot(
    left_ids  = ["c8_mlp_gatv2_ppo", "c8_frap_gatv2_ppo"],
    right_ids = ["i21_mlp_gatv2_ppo", "i21_frap_gatv2_ppo"],
    titles    = ["Cologne Regional ($N=8$)", "Ingolstadt Regional ($N=21$)"],
    ylims     = ((0, 100), (0, 1600)),
    out_path  = os.path.join(OUT, "ablation_encoder.pdf"),
)

# ── 3. Pair B — Graph layer: GATv2 vs GAT (fixed MLP+PPO) ───────────────────
pair_plot(
    left_ids  = ["c8_mlp_gatv2_ppo", "c8_mlp_gat_ppo"],
    right_ids = ["i21_mlp_gatv2_ppo", "i21_mlp_gat_ppo"],
    titles    = ["Cologne Regional ($N=8$)", "Ingolstadt Regional ($N=21$)"],
    ylims     = ((0, 100), (0, 1300)),
    out_path  = os.path.join(OUT, "ablation_graph.pdf"),
)

# ── 4. Pair C — RL algorithm: SAC vs PPO (fixed MLP+GATv2) ─────────────────
pair_plot(
    left_ids  = ["c8_mlp_gatv2_sac", "c8_mlp_gatv2_ppo"],
    right_ids = ["i21_mlp_gatv2_sac", "i21_mlp_gatv2_ppo"],
    titles    = ["Cologne Regional ($N=8$)", "Ingolstadt Regional ($N=21$)"],
    ylims     = ((0, 100), (0, 1600)),
    out_path  = os.path.join(OUT, "ablation_rl.pdf"),
)

print("\nDone — all ablation figures saved to Figures/")
