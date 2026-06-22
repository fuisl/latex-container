"""
2×3 horizontal panel: rows = cities (Cologne / Ingolstadt),
                       cols = tiers (Single / Corridor / Regional).
Each cell is a square-cropped, cleaned SVG render of the FGS topology.
"""

import os, subprocess, tempfile
import xml.etree.ElementTree as ET
import cairosvg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Row 0 = Cologne, Row 1 = Ingolstadt; cols = Single / Corridor / Regional
GRID = [
    # (dir_key, N, city, tier)
    [("resco_cologne1",     1,  "Cologne",     "Single"),
     ("resco_cologne3",     3,  "Cologne",     "Corridor"),
     ("resco_cologne8",     8,  "Cologne",     "Regional")],
    [("resco_ingolstadt1",  1,  "Ingolstadt",  "Single"),
     ("resco_ingolstadt7",  7,  "Ingolstadt",  "Corridor"),
     ("resco_ingolstadt21", 21, "Ingolstadt",  "Regional")],
]

TIERS      = ["Single", "Corridor", "Regional"]
CITIES     = ["Cologne", "Ingolstadt"]
TIER_COLOR = {"Single": "#0f766e", "Corridor": "#b45309", "Regional": "#7c3aed"}

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
BASE_DIR = os.path.join(os.path.dirname(__file__), "Figures", "network_topology")
DPI = 200

# ── SVG helpers ───────────────────────────────────────────────────────────────

def _tag(e):
    t = e.tag
    return t.split("}")[-1] if "}" in t else t

def agent_coords(root):
    xs, ys = [], []
    for g in root:
        if g.get("id") not in ("fgs-tls-nodes", "fgs-super-edges"):
            continue
        for elem in g:
            tag = _tag(elem)
            if tag == "circle":
                xs.append(float(elem.get("cx", 0)))
                ys.append(float(elem.get("cy", 0)))
            elif tag == "line":
                for a in ("x1", "x2"):
                    v = elem.get(a)
                    if v: xs.append(float(v))
                for a in ("y1", "y2"):
                    v = elem.get(a)
                    if v: ys.append(float(v))
    return xs, ys

def clean_svg(svg_path, out_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    for gid in ("summary", "legend"):
        for g in list(root):
            if g.get("id") == gid:
                root.remove(g)
    for g in root:
        if g.get("id") == "fgs-tls-nodes":
            for e in list(g):
                if _tag(e) == "text":
                    g.remove(e)
    xs, ys = agent_coords(root)
    if xs:
        x0r, x1r = min(xs), max(xs)
        y0r, y1r = min(ys), max(ys)
        span = max(x1r - x0r, y1r - y0r, 1.0)
        pad  = max(160.0, span * 0.28)
        x0, x1 = x0r - pad, x1r + pad
        y0, y1 = y0r - pad, y1r + pad
    else:
        x0, y0, x1, y1 = 0, 0, 1400, 841
    w, h = x1 - x0, y1 - y0
    side = max(w, h)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    vx, vy = cx - side / 2, cy - side / 2
    root.set("viewBox", f"{vx:.2f} {vy:.2f} {side:.2f} {side:.2f}")
    root.set("width", f"{side:.2f}")
    root.set("height", f"{side:.2f}")
    tree.write(out_path, xml_declaration=True, encoding="unicode")

def rasterise(svg_path, png_stem):
    pdf = png_stem + ".pdf"
    cairosvg.svg2pdf(url=svg_path, write_to=pdf)
    subprocess.run(["pdftocairo", "-png", "-r", str(DPI), "-singlefile",
                    pdf, png_stem], check=True, capture_output=True)
    return png_stem + ".png"

# ── figure layout (2 rows × 3 cols, landscape) ────────────────────────────────
CELL  = 1.42   # inches, square
GAP_H = 0.06   # horizontal gap between columns
GAP_V = 0.18   # vertical gap (city title sits here)
ML    = 0.18   # left margin for row label
MR    = 0.03
MT    = 0.22   # top margin for tier column headers
MB    = 0.03

fig_w = ML + 3 * CELL + 2 * GAP_H + MR
fig_h = MT + 2 * CELL + 1 * GAP_V + MB

fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")

with tempfile.TemporaryDirectory() as td:
    for row in range(2):
        for col in range(3):
            key, N, city, tier = GRID[row][col]
            clean = os.path.join(td, f"{key}_clean.svg")
            stem  = os.path.join(td, key)
            clean_svg(os.path.join(BASE_DIR, key, "02_fgs_extracted_topology.svg"), clean)
            img = mpimg.imread(rasterise(clean, stem))

            x0 = (ML + col * (CELL + GAP_H)) / fig_w
            y0 = (MB + (1 - row) * (CELL + GAP_V)) / fig_h
            ax = fig.add_axes([x0, y0, CELL / fig_w, CELL / fig_h])

            ax.imshow(img, interpolation="lanczos", aspect="auto")
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_linewidth(0.3)
                sp.set_color("#cbd5e1")

            # N label inside bottom-left corner
            ax.text(0.04, 0.04, f"$N\\!=\\!{N}$",
                    transform=ax.transAxes,
                    ha="left", va="bottom",
                    fontsize=5.5, color="#475569",
                    bbox=dict(boxstyle="round,pad=0.12", fc="white",
                              ec="none", alpha=0.8))

# tier labels along the top (one per column)
for col, tier in enumerate(TIERS):
    cx = (ML + col * (CELL + GAP_H) + CELL / 2) / fig_w
    fig.text(cx, 1.0 - MT * 0.28 / fig_h, tier,
             ha="center", va="top",
             fontsize=6.2, fontweight="bold", color=TIER_COLOR[tier])

# city row labels on the left
for row, city in enumerate(CITIES):
    yc = (MB + (1 - row) * (CELL + GAP_V) + CELL / 2) / fig_h
    fig.text(ML * 0.30 / fig_w, yc, city,
             ha="center", va="center", rotation=90,
             fontsize=6.0, fontweight="bold", color="#334155")

out = os.path.join(os.path.dirname(__file__), "Figures", "scenario_topologies.pdf")
fig.savefig(out, dpi=DPI, facecolor="white", bbox_inches=None)
print(f"Saved → {out}  ({fig_w:.2f}\" × {fig_h:.2f}\")")
