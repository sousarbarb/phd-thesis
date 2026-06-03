#!/usr/bin/env python3
"""
analyse_occupancy_maps.py
--------------------------
Compares the occupancy probability distributions of two 2D occupancy grid
maps (e.g. with vs. without dynamic object removal).

Supported inputs
-----------------
  *.tiff / *.tif (float32)   Lossless probability map. NaN = unobserved cell.
                             Produced by GridMap2D::toOccupancyGridMapWithUnknown
                             + cv::imwrite.
  *.png / *.pgm (uint8)      ROS map_server convention:
                                254 ≈ free, 205 ≈ unknown, 0 ≈ occupied.

The convention is auto-detected from the image dtype but can be forced with
--convention.

Usage
------
  python analyse_occupancy_maps.py map_a.tiff map_b.tiff \\
      --labels "With dynamics" "Without dynamics" \\
      --output comparison.pdf

  # Force ROS interpretation of 8-bit PNGs
  python analyse_occupancy_maps.py map_a.png map_b.png --convention ros

  # Headless export
  python analyse_occupancy_maps.py a.tiff b.tiff --no-show --output out.png
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from PIL import Image
from scipy.stats import gaussian_kde


# ---------------------------------------------------------------------------
# Pixel → probability conversion
# ---------------------------------------------------------------------------

ROS_FREE_VALUE    = 254   # white  (free)
ROS_UNKNOWN_VALUE = 205   # grey   (unknown / unmapped)
ROS_OCC_VALUE     = 0     # black  (occupied)

COLOUR_A = "#73726c"
COLOUR_B = "#185FA5"


def load_map(path: Path) -> np.ndarray:
    """
    Load a map image and return its raw array.

    For float TIFFs the returned dtype is float32/float64 with NaN preserved.
    For 8/16-bit PNG/PGM, the dtype is uint8 or uint16.
    """
    img = Image.open(path)
    if img.mode == "F":
        return np.asarray(img, dtype=np.float32)
    if img.mode == "I;16":
        return np.asarray(img, dtype=np.uint16)
    if img.mode != "L":
        img = img.convert("L")
    return np.asarray(img, dtype=np.uint8)


def detect_convention(arr: np.ndarray, override: str | None) -> str:
    if override:
        return override
    if np.issubdtype(arr.dtype, np.floating):
        return "prob"
    return "ros"


def to_probability(arr: np.ndarray, convention: str,
                   unknown_tol: int) -> np.ndarray:
    """
    Return a float array in [0, 1] with NaN for cells excluded from analysis.
    """
    if convention == "prob":
        # NaN already encodes unobserved cells
        return arr.astype(np.float32)

    if convention == "ros":
        arr_f = arr.astype(np.float32)
        scale = 255.0 if arr.dtype == np.uint8 else float(np.iinfo(arr.dtype).max)
        unknown_mask = np.abs(arr_f - ROS_UNKNOWN_VALUE) <= unknown_tol
        prob = 1.0 - arr_f / scale     # white → free → 0,  black → occupied → 1
        prob[unknown_mask] = np.nan
        return prob

    raise ValueError(f"Unknown convention: {convention}")


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def differential_entropy(p: np.ndarray) -> float:
    """KDE-based differential entropy in bits."""
    kde = gaussian_kde(p, bw_method="scott")
    xs  = np.linspace(0.0, 1.0, 500)
    pdf = np.clip(kde(xs), 1e-12, None)
    dx  = xs[1] - xs[0]
    return float(-np.sum(pdf * np.log2(pdf) * dx))


def middle_mass(p: np.ndarray, lo: float = 0.3, hi: float = 0.7) -> float:
    return float(np.mean((p >= lo) & (p <= hi)))


def peak_mass(p: np.ndarray, width: float = 0.15) -> float:
    return float(np.mean((p <= width) | (p >= 1.0 - width)))


def summary_stats(p: np.ndarray, label: str) -> dict:
    valid = p[~np.isnan(p)]
    return {
        "label":        label,
        "n_total":      p.size,
        "n_valid":      valid.size,
        "n_unknown":    int(np.sum(np.isnan(p))),
        "mean":         float(np.mean(valid)),
        "std":          float(np.std(valid)),
        "median":       float(np.median(valid)),
        "entropy_bits": differential_entropy(valid),
        "middle_mass":  middle_mass(valid),
        "peak_mass":    peak_mass(valid),
    }


def print_stats(stats_a: dict, stats_b: dict) -> None:
    keys = ["n_total", "n_valid", "n_unknown", "mean", "std",
            "median", "entropy_bits", "middle_mass", "peak_mass"]
    width = 22
    la, lb = stats_a["label"], stats_b["label"]
    header = f"{'Metric':<{width}}  {la:>18}  {lb:>18}"
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for k in keys:
        va, vb = stats_a[k], stats_b[k]
        if isinstance(va, int):
            print(f"{k:<{width}}  {va:>18d}  {vb:>18d}")
        else:
            print(f"{k:<{width}}  {va:>18.4f}  {vb:>18.4f}")
    print("-" * len(header))
    delta_e = stats_b["entropy_bits"] - stats_a["entropy_bits"]
    sign    = "+" if delta_e >= 0 else ""
    print(f"\nEntropy difference (B - A): {sign}{delta_e:.4f} bits")
    print("  A negative value indicates map B is more resolved.\n")


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def build_figure(prob_a: np.ndarray, prob_b: np.ndarray,
                 stats_a: dict, stats_b: dict, n_bins: int) -> plt.Figure:

    valid_a = prob_a[~np.isnan(prob_a)]
    valid_b = prob_b[~np.isnan(prob_b)]

    fig = plt.figure(figsize=(13, 9))
    fig.patch.set_facecolor("white")
    gs  = gridspec.GridSpec(
        2, 3, figure=fig,
        hspace=0.45, wspace=0.35,
        top=0.88, bottom=0.10, left=0.07, right=0.97,
    )
    fig.suptitle("Occupancy grid - probability distribution analysis",
                 fontsize=14, color="#2C2C2A")

    # Colour-mapped grids
    for col, (prob, stats) in enumerate([(prob_a, stats_a), (prob_b, stats_b)]):
        ax = fig.add_subplot(gs[0, col])
        disp = np.where(np.isnan(prob), 0.5, prob)
        im   = ax.imshow(disp, cmap="RdYlGn_r", vmin=0, vmax=1,
                         interpolation="nearest", origin="upper")
        ax.set_title(stats["label"], fontsize=11, color="#2C2C2A", pad=6)
        ax.axis("off")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                     label="p(occ)", shrink=0.85)

    # Summary statistics table
    ax_stats = fig.add_subplot(gs[0, 2])
    ax_stats.axis("off")
    rows = [
        ["Metric", stats_a["label"], stats_b["label"]],
        ["Valid cells",
         f"{stats_a['n_valid']:,}", f"{stats_b['n_valid']:,}"],
        ["Unknown cells",
         f"{stats_a['n_unknown']:,}", f"{stats_b['n_unknown']:,}"],
        ["Mean p(occ)",
         f"{stats_a['mean']:.4f}", f"{stats_b['mean']:.4f}"],
        ["Std dev",
         f"{stats_a['std']:.4f}", f"{stats_b['std']:.4f}"],
        ["Entropy (bits)",
         f"{stats_a['entropy_bits']:.4f}", f"{stats_b['entropy_bits']:.4f}"],
        ["Middle mass\n(0.3 - 0.7)",
         f"{stats_a['middle_mass']:.4f}", f"{stats_b['middle_mass']:.4f}"],
        ["Peak mass\n(<=0.15, >=0.85)",
         f"{stats_a['peak_mass']:.4f}", f"{stats_b['peak_mass']:.4f}"],
    ]
    tbl = ax_stats.table(cellText=rows[1:], colLabels=rows[0],
                         loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.0, 1.55)
    for j in range(3):
        tbl[0, j].set_facecolor("#D3D1C7")
        tbl[0, j].set_text_props(fontweight="bold", color="#2C2C2A")
    ax_stats.set_title("Summary statistics", fontsize=11,
                       color="#2C2C2A", pad=6)

    # Overlaid histogram + KDE
    ax_main = fig.add_subplot(gs[1, :])
    bin_edges = np.linspace(0, 1, n_bins + 1)
    bin_cx    = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    for valid, colour, label, ls in [
        (valid_a, COLOUR_A, stats_a["label"], "--"),
        (valid_b, COLOUR_B, stats_b["label"], "-"),
    ]:
        counts, _ = np.histogram(valid, bins=bin_edges, density=True)
        ax_main.fill_between(bin_cx, counts, alpha=0.18, color=colour)
        kde = gaussian_kde(valid, bw_method="scott")
        xs  = np.linspace(0, 1, 500)
        ax_main.plot(xs, kde(xs), color=colour, lw=2.0,
                     linestyle=ls, label=label)
        for peak in (0.0, 1.0):
            ax_main.axvline(peak, color=colour, lw=0.6,
                            linestyle=":", alpha=0.6)

    ax_main.set_xlabel("Occupancy probability  p(occ)", fontsize=11)
    ax_main.set_ylabel("Density", fontsize=11)
    ax_main.set_xlim(0, 1)
    ax_main.set_ylim(bottom=0)
    ax_main.tick_params(labelsize=9)
    ax_main.spines[["top", "right"]].set_visible(False)
    ax_main.grid(axis="y", linewidth=0.4, color="#D3D1C7", linestyle="--")

    legend_elements = [
        Line2D([0], [0], color=COLOUR_A, lw=2, linestyle="--",
               label=stats_a["label"]),
        Line2D([0], [0], color=COLOUR_B, lw=2, linestyle="-",
               label=stats_b["label"]),
    ]
    ax_main.legend(handles=legend_elements, fontsize=10,
                   frameon=False, loc="upper center")
    ax_main.set_title(
        "Probability distribution of occupancy across all cells",
        fontsize=11, color="#2C2C2A", pad=6,
    )

    return fig


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("map_a", type=Path, help="First map (TIFF/PNG/PGM)")
    p.add_argument("map_b", type=Path, help="Second map (TIFF/PNG/PGM)")
    p.add_argument(
        "--convention", choices=["auto", "ros", "prob"], default="auto",
        help="Pixel convention. 'auto' picks 'prob' for float inputs and "
             "'ros' for integer inputs. Default: auto",
    )
    p.add_argument(
        "--labels", nargs=2, default=["Map A", "Map B"],
        metavar=("LABEL_A", "LABEL_B"),
    )
    p.add_argument(
        "--unknown-tol", type=int, default=5, metavar="TOL",
        help="[ros only] Tolerance around pixel value 205 to mark as unknown. "
             "Default: 5",
    )
    p.add_argument("--bins", type=int, default=60,
                   help="Histogram bin count. Default: 60")
    p.add_argument("--output", type=Path, default=None,
                   help="Save figure to this path (PNG/PDF/SVG)")
    p.add_argument("--no-show", action="store_true",
                   help="Do not open the interactive figure window")
    p.add_argument("--dpi", type=int, default=150,
                   help="Figure DPI for saved output. Default: 150")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    for path in (args.map_a, args.map_b):
        if not path.exists():
            sys.exit(f"[error] File not found: {path}")

    print(f"[info] Loading {args.map_a} ...")
    raw_a = load_map(args.map_a)
    print(f"[info] Loading {args.map_b} ...")
    raw_b = load_map(args.map_b)

    override = None if args.convention == "auto" else args.convention
    conv_a = detect_convention(raw_a, override)
    conv_b = detect_convention(raw_b, override)

    print(f"[info] Map A: shape={raw_a.shape}  dtype={raw_a.dtype}  "
          f"convention={conv_a}")
    print(f"[info] Map B: shape={raw_b.shape}  dtype={raw_b.dtype}  "
          f"convention={conv_b}")

    if conv_a != conv_b:
        print("[warn] The two maps use different conventions; "
              "comparison may be misleading.")

    prob_a = to_probability(raw_a, conv_a, args.unknown_tol)
    prob_b = to_probability(raw_b, conv_b, args.unknown_tol)

    label_a, label_b = args.labels
    stats_a = summary_stats(prob_a, label_a)
    stats_b = summary_stats(prob_b, label_b)
    print_stats(stats_a, stats_b)

    fig = build_figure(prob_a, prob_b, stats_a, stats_b, n_bins=args.bins)

    if args.output:
        fig.savefig(args.output, dpi=args.dpi, bbox_inches="tight")
        print(f"[info] Figure saved to {args.output}")

    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
