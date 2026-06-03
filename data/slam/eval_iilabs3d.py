#!/usr/bin/env python3
"""
eval_slam.py
------------
Evaluate SLAM trajectories (TUM format) against a reference using the evo
Python API. Computes, for each estimate:
  - ATE : Absolute Trajectory Error (translation, m) after SE(3) Umeyama
          alignment of the estimate to the reference.
  - RTE : Relative Translation Error (% of segment length, delta = 10 m).
  - RRE : Relative Rotation Error    (deg/m,             delta = 10 m).

Usage:
    python3 eval_slam.py REFERENCE.tum EST1.tum [EST2.tum ...]

Dependencies:
    pip install evo numpy

Co-developed with Claude... Thanks!!!
"""

import argparse
import sys
import numpy as np
from pathlib import Path

from evo.core import metrics, sync
from evo.tools import file_interface

# ---------------------------------------------------------------------------
# Evo evaluation parameters
# ---------------------------------------------------------------------------

MAX_TIME_DIFF = 0.01    # seconds
DELTA         = 10.0    # metres
DELTA_UNIT    = metrics.Unit.meters
REL_DELTA_TOL = 0.1

METRIC_LABELS = {
    "ate": "ATE [m]",
    "rte": "RTE [%]",
    "rre": "RRE [deg/m]",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compute_stats(arr: np.ndarray) -> dict:
    return {
        "rmse":   float(np.sqrt(np.mean(arr ** 2))),
        "mean":   float(np.mean(arr)),
        "std":    float(np.std(arr)),
        "median": float(np.median(arr)),
        "n":      int(len(arr)),
    }


def evaluate(ref_path: Path, est_path: Path) -> dict:
    """Compute ATE, RTE, RRE. Returns {'ate': arr, 'rte': arr, 'rre': arr}."""
    traj_ref = file_interface.read_tum_trajectory_file(str(ref_path))
    traj_est = file_interface.read_tum_trajectory_file(str(est_path))

    traj_ref_s, traj_est_s = sync.associate_trajectories(
        traj_ref, traj_est, max_diff=MAX_TIME_DIFF)
    traj_est_s.align(traj_ref_s, correct_scale=False)

    # ATE: absolute translation error after global SE(3) alignment.
    ape = metrics.APE(metrics.PoseRelation.translation_part)
    ape.process_data((traj_ref_s, traj_est_s))
    ate_arr = ape.get_result().np_arrays["error_array"]

    # RTE: relative translation error, normalised to % of segment length.
    rpe_t = metrics.RPE(
        pose_relation=metrics.PoseRelation.translation_part,
        delta=DELTA, delta_unit=DELTA_UNIT,
        rel_delta_tol=REL_DELTA_TOL, all_pairs=False,
    )
    rpe_t.process_data((traj_ref_s, traj_est_s))
    rte_arr = rpe_t.get_result().np_arrays["error_array"] / DELTA * 100.0

    # RRE: relative rotation error, normalised to deg/m.
    rpe_r = metrics.RPE(
        pose_relation=metrics.PoseRelation.rotation_angle_deg,
        delta=DELTA, delta_unit=DELTA_UNIT,
        rel_delta_tol=REL_DELTA_TOL, all_pairs=False,
    )
    rpe_r.process_data((traj_ref_s, traj_est_s))
    rre_arr = rpe_r.get_result().np_arrays["error_array"] / DELTA

    return {"ate": ate_arr, "rte": rte_arr, "rre": rre_arr}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ATE/RTE/RRE evaluation against a reference TUM trajectory.")
    parser.add_argument("reference", type=Path,
                        help="Reference (ground truth) TUM trajectory.")
    parser.add_argument("estimates", type=Path, nargs="+",
                        help="One or more estimate TUM trajectories.")
    args = parser.parse_args()

    if not args.reference.exists():
        sys.exit(f"[ERROR] Reference not found: {args.reference}")
    for est in args.estimates:
        if not est.exists():
            sys.exit(f"[ERROR] Estimate not found: {est}")

    print(f"Reference : {args.reference}")
    print(f"Estimates : {len(args.estimates)} file(s)")
    print(f"Settings  : max_time_diff={MAX_TIME_DIFF}s, "
          f"delta={DELTA:.0f}m, rel_delta_tol={REL_DELTA_TOL}, "
          f"SE(3) Umeyama alignment\n")

    summary = []   # list of (name, stats_per_metric)
    for i, est_path in enumerate(args.estimates, start=1):
        print(f"[{i}/{len(args.estimates)}] {est_path}")
        try:
            arrays = evaluate(args.reference, est_path)
        except Exception as e:
            print(f"  [ERROR] {e}\n")
            continue

        stats = {}
        for key, arr in arrays.items():
            s = compute_stats(arr)
            stats[key] = s
            print(f"  {METRIC_LABELS[key]:12s}  "
                  f"RMSE={s['rmse']:8.4f}  Mean={s['mean']:8.4f}  "
                  f"Std={s['std']:8.4f}  Median={s['median']:8.4f}  n={s['n']}")
        print()
        summary.append((str(est_path), stats))

    # -----------------------------------------------------------------------
    # Compact summary table (RMSE per metric)
    # -----------------------------------------------------------------------
    if len(summary) > 1:
        name_w = max(len(n) for n, _ in summary)
        header = (f"{'File':<{name_w}}  "
                  f"{'ATE [m]':>10}  {'RTE [%]':>10}  {'RRE [deg/m]':>12}")
        print("Summary (RMSE)")
        print("=" * len(header))
        print(header)
        print("-" * len(header))
        for name, stats in summary:
            print(f"{name:<{name_w}}  "
                  f"{stats['ate']['rmse']:>10.3f}  "
                  f"{stats['rte']['mean']:>10.2f}  "
                  f"{stats['rre']['mean']:>12.3f}")


if __name__ == "__main__":
    main()
