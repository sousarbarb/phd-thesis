#!/usr/bin/env python3
"""
plot_trajectories.py
--------------------
Plot a ground-truth TUM trajectory together with one or more estimated
trajectories. Estimates are SE(3) Umeyama-aligned to the reference using the
same procedure as eval_iilabs3d.py, so the visual overlay is consistent with
the ATE/RTE/RRE numbers reported in Chapter 5.

The plot style mirrors year.py (Chapter 2 literature review): tab-colour
palette with black edges, bold title, "x [m] -> / y [m] ->" axis labels,
tight layout, and EPS output ready for inclusion in LaTeX.

Usage:
    python3 plot_trajectories.py REFERENCE.tum EST1.tum [EST2.tum ...]
                                 [--labels LBL1 LBL2 ...]
                                 [--output FIG.eps]
                                 [--title TITLE]
                                 [--no-align]
                                 [--no-show]

Dependencies:
    pip install evo numpy matplotlib

Co-developed with Claude... Thanks!!!
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from evo.core import sync
from evo.tools import file_interface

# ---------------------------------------------------------------------------
# Plot / alignment parameters
# ---------------------------------------------------------------------------

MAX_TIME_DIFF = 0.01    # seconds, matches eval_iilabs3d.py

# Estimate colour cycle (leading with tab:blue / tab:orange to match year.py;
# extend the list if more than nine estimates are ever plotted together).
EST_COLORS = [
    'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
    'tab:brown', 'tab:pink', 'tab:olive', 'tab:cyan',
]

LINESTYLES = ['-.', ':', '--', '-']

REF_COLOR     = 'black'
REF_LINESTYLE = '--'
REF_LINEWIDTH = 1
EST_LINEWIDTH = 1
# START_MARKER  = 'o'
START_MS      = 6

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_trajectory(path: Path):
    """Read a TUM-format trajectory and return an evo PoseTrajectory3D."""
    return file_interface.read_tum_trajectory_file(str(path))


def align_to_reference(traj_ref, traj_est):
    """
    Synchronise and SE(3) Umeyama-align an estimate to a reference, returning
    the (synced_ref, aligned_est) pair. Matches eval_iilabs3d.py exactly.
    """
    ref_s, est_s = sync.associate_trajectories(
        traj_ref, traj_est, max_diff=MAX_TIME_DIFF)
    est_s.align(ref_s, correct_scale=False)
    return ref_s, est_s


def xy(positions_xyz, swap: bool) -> np.ndarray:
    """Return Nx2 horizontal/vertical coordinates, swapping columns if asked."""
    xy_arr = positions_xyz[:, :2]
    return xy_arr[:, [1, 0]] if swap else xy_arr


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Plot a reference TUM trajectory together with one or "
                    "more estimates (top-down x-y view).")
    parser.add_argument("reference", type=Path,
                        help="Reference (ground truth) TUM trajectory.")
    parser.add_argument("estimates", type=Path, nargs="+",
                        help="One or more estimate TUM trajectories.")
    parser.add_argument("--labels", type=str, nargs="*", default=None,
                        help="Optional labels for the estimates "
                             "(default: file stems).")
    parser.add_argument("--output", type=Path, default=None,
                        help="Optional output figure path "
                             "(format inferred from extension: .eps/.pdf/.png).")
    parser.add_argument("--title", type=str, default="Trajectory Comparison",
                        help="Plot title (default: 'Trajectory Comparison').")
    parser.add_argument("--no-align", action="store_true",
                        help="Disable SE(3) Umeyama alignment of estimates.")
    parser.add_argument("--no-show", action="store_true",
                        help="Do not call plt.show() (useful in headless runs).")
    parser.add_argument("--xlim", type=float, nargs=2, default=None,
                        metavar=('XMIN', 'XMAX'),
                        help="Override x-axis limits, in metres. "
                             "Equal-scale aspect is preserved; the axes box "
                             "is resized to fit the new window.")
    parser.add_argument("--ylim", type=float, nargs=2, default=None,
                        metavar=('YMIN', 'YMAX'),
                        help="Override y-axis limits, in metres.")
    parser.add_argument("--swap-xy", action="store_true",
                        help="Swap x and y data (and axis labels) before "
                             "plotting. Useful for laying out long-thin "
                             "trajectories along the page width.")
    args = parser.parse_args()

    # ---- validation -------------------------------------------------------
    if not args.reference.exists():
        sys.exit(f"[ERROR] Reference not found: {args.reference}")
    for est in args.estimates:
        if not est.exists():
            sys.exit(f"[ERROR] Estimate not found: {est}")

    if args.labels is not None and len(args.labels) != len(args.estimates):
        sys.exit(f"[ERROR] --labels expects {len(args.estimates)} value(s), "
                 f"got {len(args.labels)}.")

    labels = (args.labels if args.labels is not None
              else [p.stem for p in args.estimates])

    print(f"Reference : {args.reference}")
    print(f"Estimates : {len(args.estimates)} file(s)")
    print(f"Labels    : {labels}")
    print(f"Settings  : max_time_diff={MAX_TIME_DIFF}s, "
          f"alignment={'off' if args.no_align else 'SE(3) Umeyama'}\n")

    # ---- load reference ---------------------------------------------------
    traj_ref = load_trajectory(args.reference)

    # ---- figure -----------------------------------------------------------
    fig, ax = plt.subplots()

    # Reference: black dashed line so it stays distinct from the tab palette.
    ref_xy = xy(traj_ref.positions_xyz, args.swap_xy)
    ax.plot(ref_xy[:, 0], ref_xy[:, 1],
            color=REF_COLOR, linestyle=REF_LINESTYLE,
            linewidth=REF_LINEWIDTH, label='gt')
    # ax.plot(ref_xy[0, 0], ref_xy[0, 1],
    #         marker=START_MARKER, color=REF_COLOR,
    #         markersize=START_MS, markerfacecolor='white',
    #         linestyle='None')

    # ---- load + align + plot each estimate --------------------------------
    for i, est_path in enumerate(args.estimates):
        traj_est = load_trajectory(est_path)
        if args.no_align:
            est = traj_est
        else:
            try:
                _, est = align_to_reference(traj_ref, traj_est)
            except Exception as e:
                print(f"[ERROR] Could not align {est_path}: {e}")
                continue

        color = EST_COLORS[i % len(EST_COLORS)]
        est_xy = xy(est.positions_xyz, args.swap_xy)
        ax.plot(est_xy[:, 0], est_xy[:, 1],
                color=color,
                linestyle=LINESTYLES[i % len(LINESTYLES)],
                linewidth=EST_LINEWIDTH,
                alpha=0.8,
                label=labels[i])
        # ax.plot(est_xy[0, 0], est_xy[0, 1],
        #         marker=START_MARKER, color=color,
        #         markersize=START_MS, markerfacecolor='white',
        #         linestyle='None')

        print(f"  [{i+1}/{len(args.estimates)}] {est_path}  "
              f"({len(est_xy)} poses plotted)")

    # ---- styling (matches year.py) ----------------------------------------
    if args.swap_xy:
        ax.set_xlabel(r'y [m] $\rightarrow$', fontsize='small')
        ax.set_ylabel(r'x [m] $\rightarrow$', fontsize='small')
    else:
        ax.set_xlabel(r'x [m] $\rightarrow$', fontsize='small')
        ax.set_ylabel(r'y [m] $\rightarrow$', fontsize='small')
    ax.set_title(args.title, fontweight='bold', fontsize='small')
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle=':', linewidth=0.5, alpha=0.7)
    ax.legend(loc='best', frameon=True,
              fontsize='small',
              handlelength=1.5,
              handletextpad=0.4,
              borderpad=0.3,
              labelspacing=0.3)

    if args.xlim is not None:
        ax.set_xlim(args.xlim)
    if args.ylim is not None:
        ax.set_ylim(args.ylim)

    plt.tight_layout()

    # ---- save -------------------------------------------------------------
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fmt = args.output.suffix.lstrip('.').lower() or 'eps'
        plt.savefig(str(args.output), format=fmt, bbox_inches='tight')
        print(f"\nSaved figure to {args.output}")

    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
