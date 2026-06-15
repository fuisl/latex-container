"""
Generate methodology figures for the FGS thesis.
Outputs two PDF figures to src/Figures/.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "Figures")

# ── Shared colours ─────────────────────────────────────────────────────────────
C_FILE   = "#B6D2E4"   # blue-light  – data files
C_FILE_B = "#2D89CC"   # blue-dark
C_PROC   = "#F5D9A0"   # amber-light – environment / interface
C_PROC_B = "#C47B10"
C_MODEL  = "#D4EAB5"   # green-light – model components
C_MODEL_B= "#6A9B30"
C_LOG    = "#E8E8E8"   # gray-light  – logging / storage
C_LOG_B  = "#888888"
C_ATTN   = "#FDD5D0"   # red-light   – attention / critic
C_ATTN_B = "#C4432D"


def rounded_box(ax, x, y, w, h, label, fc, ec, fs=8, lw=1.2, ra=0.07):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=f"round,pad=0,rounding_size={ra}",
                         facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2)
    ax.add_patch(box)
    ax.text(x, y, label, ha="center", va="center", fontsize=fs,
            fontfamily="serif", zorder=3, wrap=True,
            multialignment="center")


def arrow(ax, x0, y0, x1, y1, color="#444444", lw=1.4, style="-|>",
          connectionstyle="arc3,rad=0.0"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, connectionstyle=connectionstyle),
                zorder=4)


# ══════════════════════════════════════════════════════════════════════════════
# Figure 1 — System Architecture
# ══════════════════════════════════════════════════════════════════════════════
def fig_system_arch():
    fig, ax = plt.subplots(figsize=(11, 6.8))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6.8)
    ax.axis("off")

    BW, BH = 2.2, 0.52   # box width / height
    SBH    = 0.45

    # ── Row 0: Input files ────────────────────────────────────────────────────
    rounded_box(ax, 2.0, 6.3, BW, BH, ".net.xml\n(Network topology)", C_FILE, C_FILE_B)
    rounded_box(ax, 4.5, 6.3, BW, BH, ".rou.xml\n(Demand routes)",    C_FILE, C_FILE_B)

    # ── Row 1: Pre-processing ─────────────────────────────────────────────────
    rounded_box(ax, 2.0, 5.35, 2.6, SBH,
                "Graph Construction\n(Dijkstra super-edges)", C_PROC, C_PROC_B)
    rounded_box(ax, 4.9, 5.35, 1.6, SBH, "graph.pkl", C_FILE, C_FILE_B, fs=7.5)

    arrow(ax, 2.0, 6.04, 2.0, 5.61)
    arrow(ax, 4.5, 6.04, 2.9, 5.61)
    arrow(ax, 3.3, 5.35, 4.1, 5.35)

    # ── Row 2: Simulation interface ────────────────────────────────────────────
    y2 = 4.3
    rounded_box(ax, 1.2, y2, 1.7, SBH, "SUMO\nSimulator",     C_PROC, C_PROC_B)
    rounded_box(ax, 3.2, y2, 2.0, SBH, "SUMO-RL\nEnv Wrapper",C_PROC, C_PROC_B)
    rounded_box(ax, 5.7, y2, 2.4, SBH, "FGSGraphParallelEnv\n(graph obs. builder)", C_PROC, C_PROC_B)

    # TraCI double-headed arrow
    ax.annotate("", xy=(2.25, y2), xytext=(2.05, y2),
                arrowprops=dict(arrowstyle="<->", color="#444", lw=1.3))
    ax.text(2.17, y2+0.16, "TraCI", ha="center", fontsize=6.5, color="#444")

    arrow(ax, 4.2, y2, 4.5, y2)
    arrow(ax, 4.9, 5.12, 4.9, 4.56)     # graph.pkl → FGSGraphParallelEnv
    arrow(ax, 4.5, 6.04, 4.5, 4.56)     # .rou.xml → SUMO (via demand)

    # ── Row 3: FGS Model ──────────────────────────────────────────────────────
    y3 = 3.1
    rounded_box(ax, 1.4, y3, 2.2, SBH, "Local Encoder\n(FRAP  or  MLP)", C_MODEL, C_MODEL_B)
    rounded_box(ax, 3.9, y3, 2.0, SBH, "GATv2\nCommunication\n(optional)", C_MODEL, C_MODEL_B)
    rounded_box(ax, 6.5, y3, 1.8, SBH, "Actor  $\\pi_\\phi$\n(shared params)", C_MODEL, C_MODEL_B)
    rounded_box(ax, 8.6, y3, 1.8, SBH, "Centralised\nCritic  $Q_\\theta$", C_ATTN, C_ATTN_B)

    arrow(ax, 5.7, y2-0.22, 2.6, y3+0.22)   # FGSGraphParallelEnv → encoder
    arrow(ax, 2.5, y3, 2.9, y3)
    arrow(ax, 4.9, y3, 5.6, y3)
    arrow(ax, 6.5, y3+0.22, 6.5, y2-0.22,   # actor → SUMO (actions)
          connectionstyle="arc3,rad=0.25", style="-|>")
    ax.text(7.05, 3.7, "phase\nselection", ha="center", fontsize=6, color="#555")
    arrow(ax, 5.6, y3, 7.7, y3)              # GAT output → critic

    # ── Row 4: Replay buffer ──────────────────────────────────────────────────
    y4 = 2.05
    rounded_box(ax, 5.0, y4, 3.0, SBH,
                "Prioritised Replay Buffer  (PER)", C_LOG, C_LOG_B)

    arrow(ax, 6.5, y3-0.22, 5.5, y4+0.22)
    arrow(ax, 8.6, y3-0.22, 6.0, y4+0.22)

    # gradient update back to model
    ax.annotate("", xy=(2.5, y3-0.22), xytext=(3.5, y4-0.22),
                arrowprops=dict(arrowstyle="-|>", color="#1a7a1a", lw=1.3,
                                connectionstyle="arc3,rad=0.0",
                                linestyle="dashed"))
    ax.text(2.4, 1.75, "gradient\nupdates", ha="center", fontsize=6.2,
            color="#1a7a1a")

    # ── Row 5: Logging ────────────────────────────────────────────────────────
    y5 = 1.1
    rounded_box(ax, 5.0, y5, 3.0, SBH, "Weights & Biases\n(experiment tracking)", C_LOG, C_LOG_B)
    arrow(ax, 5.0, y4-0.22, 5.0, y5+0.22)

    # ── Section labels ────────────────────────────────────────────────────────
    for lbl, y, x_l in [
        ("Pre-processing", 5.7, 0.05),
        ("Simulation Interface", 4.65, 0.05),
        ("FGS / FGSv2 Model", 3.5, 0.05),
        ("Training Infrastructure", 2.4, 0.05),
    ]:
        ax.text(x_l, y, lbl, fontsize=7, color="#666", fontstyle="italic",
                va="top", ha="left")

    # ── RLlib brace ───────────────────────────────────────────────────────────
    ax.text(10.85, 3.1, "RLlib", fontsize=7.5, color="#888", va="center",
            ha="right", rotation=90)
    ax.plot([10.7, 10.7], [y4+0.22, y3+0.22], color="#aaa", lw=1.2)

    ax.set_title("End-to-End System Architecture", fontsize=11,
                 fontfamily="serif", pad=4, color="#222")
    plt.tight_layout(pad=0.3)
    out = os.path.join(OUT, "system_architecture.pdf")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ══════════════════════════════════════════════════════════════════════════════
# Figure 2 — FGS / FGSv2 Framework Overview
# ══════════════════════════════════════════════════════════════════════════════
def fig_fgs_framework():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    titles = ["FGS Architecture", "FGSv2 Architecture"]

    for ax, title in zip(axes, titles):
        ax.set_xlim(0, 6); ax.set_ylim(0, 5.2)
        ax.axis("off")
        ax.set_title(title, fontsize=10, fontfamily="serif", color="#222", pad=3)

    # ── Helper ────────────────────────────────────────────────────────────────
    def rb(ax, x, y, w, h, lbl, fc, ec, fs=7.8):
        rounded_box(ax, x, y, w, h, lbl, fc, ec, fs=fs)

    def ar(ax, x0, y0, x1, y1, **kw):
        arrow(ax, x0, y0, x1, y1, **kw)

    BW, BH = 2.4, 0.48

    # ── FGS (left panel) ─────────────────────────────────────────────────────
    ax = axes[0]

    # Observation
    rb(ax, 3.0, 4.75, 5.8, 0.44,
       r"Graph observation: node features $\mathbf{X}\in\mathbb{R}^{N\times d}$,"
       r" edge index $\mathcal{E}$, action mask",
       C_FILE, C_FILE_B, fs=7.2)

    # Local encoder (two options shown as sub-box)
    rb(ax, 1.5, 3.85, 2.6, 0.44, "Option A: MLP encoder\n(2-layer ReLU)", C_MODEL, C_MODEL_B)
    rb(ax, 4.4, 3.85, 2.6, 0.44, "Option B: FRAP encoder\n(phase-competition)", C_PROC, C_PROC_B)
    ax.text(3.0, 3.85, "or", ha="center", va="center", fontsize=8, color="#666")
    # merge arrow
    ar(ax, 1.5, 3.62, 1.5, 3.15)
    ar(ax, 4.4, 3.62, 4.4, 3.15)
    # brace
    ax.plot([1.5, 1.5, 4.4, 4.4], [3.15, 3.05, 3.05, 3.15], color="#888", lw=1)
    ax.annotate("", xy=(3.0, 2.9), xytext=(3.0, 3.05),
                arrowprops=dict(arrowstyle="-|>", color="#666", lw=1))

    # Node embeddings H
    rb(ax, 3.0, 2.65, BW, BH,
       r"Node embeddings $\mathbf{H}=\{\mathbf{h}_i\}\in\mathbb{R}^{N\times d_h}$",
       C_MODEL, C_MODEL_B, fs=7.2)

    # GATv2 (dashed = optional)
    ar(ax, 3.0, 2.41, 3.0, 1.98)
    rb(ax, 3.0, 1.74, BW+0.3, BH,
       "GATv2 Communication\n(optional; disabled → skip)",
       C_MODEL, C_MODEL_B)
    # dashed border override
    r_opt = FancyBboxPatch((3.0 - (BW+0.3)/2, 1.74 - BH/2),
                           BW+0.3, BH,
                           boxstyle="round,pad=0,rounding_size=0.07",
                           facecolor=C_MODEL, edgecolor=C_MODEL_B,
                           linewidth=1.4, linestyle="dashed", zorder=2.5)
    ax.add_patch(r_opt)

    ar(ax, 3.0, 1.50, 3.0, 1.08)

    # Updated embeddings H'
    rb(ax, 3.0, 0.84, BW, BH,
       r"Updated embeddings $\mathbf{H}'\in\mathbb{R}^{N\times d_h'}$",
       C_MODEL, C_MODEL_B, fs=7.2)

    # Split to actor / critic
    ar(ax, 2.1, 0.60, 1.5, 0.22)
    ar(ax, 3.9, 0.60, 4.5, 0.22)

    rb(ax, 1.3, 0.0, 2.2, 0.40,
       r"Actor $\pi_\phi$: ego row $\to$ logits", C_ATTN, C_ATTN_B, fs=7)
    rb(ax, 4.7, 0.0, 2.2, 0.40,
       r"Critic $Q_\theta$: $\mathrm{vec}(\mathbf{H}')+\boldsymbol{\Pi}\to Q$",
       C_ATTN, C_ATTN_B, fs=7)

    ar(ax, 3.0, 4.53, 3.0, 4.07)

    # ── FGSv2 (right panel) ──────────────────────────────────────────────────
    ax = axes[1]

    rb(ax, 3.0, 4.75, 5.8, 0.44,
       r"Graph observation (same as FGS)  +  phase-pair mask $\mathbf{M}_\mathrm{pair}$,"
       r"  competition mask $\mathbf{M}_\mathrm{comp}$",
       C_FILE, C_FILE_B, fs=7.2)

    # FRAP action-token encoder
    rb(ax, 3.0, 3.92, BW+0.6, BH,
       "FRAP action-token encoder\n"
       r"(tapped at $\mathbf{c}_{i,a,b}$ — before scalar projection)",
       C_PROC, C_PROC_B, fs=7.2)
    ar(ax, 3.0, 4.53, 3.0, 4.16)
    ar(ax, 3.0, 3.68, 3.0, 3.28)

    # Action tokens Z
    rb(ax, 3.0, 3.06, BW+0.4, BH,
       r"Action tokens $\mathbf{Z}_i\in\mathbb{R}^{A_\max\times d_z}$"
       "\n" r"(one token per candidate phase)",
       C_MODEL, C_MODEL_B, fs=7.2)

    # Node summary
    ar(ax, 3.0, 2.82, 3.0, 2.42)
    rb(ax, 3.0, 2.20, BW, BH,
       r"Node summary $\mathbf{s}_i$ (masked mean-pool)"
       "\n" r"$\to$ GATv2 + residual gate ($\lambda$, init $=0$)",
       C_MODEL, C_MODEL_B, fs=7.2)
    ar(ax, 3.0, 1.96, 3.0, 1.56)

    rb(ax, 3.0, 1.34, BW, BH,
       r"Gated graph context $\mathbf{g}_i$",
       C_MODEL, C_MODEL_B, fs=7.2)
    ar(ax, 3.0, 1.10, 3.0, 0.70)

    # Action-conditioned actor
    rb(ax, 3.0, 0.48, BW+0.8, BH,
       r"Action-cond. actor: $[\mathbf{z}_{i,a}\,\|\,\mathbf{g}_i\,\|\,\mathbf{e}_a]\to l_a$"
       "\n" r"+ Centralised action-token critic $Q_k(a)$",
       C_ATTN, C_ATTN_B, fs=7.2)

    # Token feedback arrow from Z to actor
    ax.annotate("", xy=(1.2, 0.48), xytext=(1.2, 3.06),
                arrowprops=dict(arrowstyle="-|>", color="#777", lw=1.1,
                                linestyle="dotted",
                                connectionstyle="arc3,rad=0.0"))
    ax.text(0.8, 1.8, r"$\mathbf{z}_{i,a}$", ha="center", fontsize=7.5, color="#555")

    plt.suptitle(
        "FGS and FGSv2 Framework Overview",
        fontsize=11, fontfamily="serif", y=1.01, color="#222"
    )
    plt.tight_layout(pad=0.6)
    out = os.path.join(OUT, "fgs_framework.pdf")
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


if __name__ == "__main__":
    fig_system_arch()
    fig_fgs_framework()
    print("Done.")
