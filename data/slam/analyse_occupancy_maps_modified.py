#!/usr/bin/env python3
"""
analyse_occupancy_maps_modified.py
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

Peak / middle mass
-------------------
With a single threshold tau, the two metrics partition [0, 1]:
  peak_mass   = fraction of cells in [0, tau] ∪ [1 - tau, 1]
  middle_mass = fraction of cells in (tau, 1 - tau)
so that peak_mass + middle_mass = 1 over the set of valid (observed) cells.

Usage
------
  python analyse_occupancy_maps_modified.py map_a.tiff map_b.tiff

  # Force ROS interpretation of 8-bit PNGs
  python analyse_occupancy_maps_modified.py map_a.png map_b.png --convention ros

  # Use a different partition threshold
  python analyse_occupancy_maps_modified.py map_a.tiff map_b.tiff --tau 0.3

Co-developed with Claude... Thanks!!!
"""

import argparse
import sys
from pathlib import Path

import numpy as np
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


def peak_mass(p: np.ndarray, tau: float = 0.25) -> float:
    """
    Fraction of cells with strong evidence of being free or occupied.

    Cells in [0, tau] ∪ [1 - tau, 1].
    """
    return float(np.mean((p <= tau) | (p >= 1.0 - tau)))


def middle_mass(p: np.ndarray, tau: float = 0.25) -> float:
    """
    Fraction of cells with weak or ambiguous evidence.

    Cells in (tau, 1 - tau). Complementary to peak_mass for the same tau.
    """
    return float(np.mean((p > tau) & (p < 1.0 - tau)))


def summary_stats(p: np.ndarray, label: str, tau: float = 0.25) -> dict:
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
        "peak_mass":    peak_mass(valid, tau=tau),
        "middle_mass":  middle_mass(valid, tau=tau),
    }


def print_stats(stats_a: dict, stats_b: dict, tau: float) -> None:
    keys = ["n_total", "n_valid", "n_unknown", "mean", "std",
            "median", "entropy_bits", "peak_mass", "middle_mass"]
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
    print(f"\nPeak / middle mass partition uses tau = {tau:.3f}")
    print(f"  peak   = cells in [0, {tau:.2f}] union [{1.0 - tau:.2f}, 1]")
    print(f"  middle = cells in ({tau:.2f}, {1.0 - tau:.2f})")
    delta_e = stats_b["entropy_bits"] - stats_a["entropy_bits"]
    sign    = "+" if delta_e >= 0 else ""
    print(f"\nEntropy difference (B - A): {sign}{delta_e:.4f} bits")
    print("  A negative value indicates map B is more resolved.\n")


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
    p.add_argument(
        "--tau", type=float, default=0.25, metavar="TAU",
        help="Threshold for the peak/middle mass partition of [0, 1]. "
             "Peak mass counts cells in [0, tau] union [1 - tau, 1]; "
             "middle mass counts cells in (tau, 1 - tau). "
             "Must satisfy 0 < tau < 0.5. Default: 0.25",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if not (0.0 < args.tau < 0.5):
        sys.exit(f"[error] --tau must be in (0, 0.5); got {args.tau}")

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

    print(f"[info] Map A: shape={raw_a.shape}  #cells={raw_a.size}  "
          f"dtype={raw_a.dtype}  convention={conv_a}")
    print(f"[info] Map B: shape={raw_b.shape}  #cells={raw_b.size}  "
          f"dtype={raw_b.dtype}  convention={conv_b}")

    if conv_a != conv_b:
        print("[warn] The two maps use different conventions; "
              "comparison may be misleading.")

    prob_a = to_probability(raw_a, conv_a, args.unknown_tol)
    prob_b = to_probability(raw_b, conv_b, args.unknown_tol)

    label_a, label_b = args.labels
    stats_a = summary_stats(prob_a, label_a, tau=args.tau)
    stats_b = summary_stats(prob_b, label_b, tau=args.tau)
    print_stats(stats_a, stats_b, tau=args.tau)


if __name__ == "__main__":
    main()
