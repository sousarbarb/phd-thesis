#!/usr/bin/env python3
"""
eval_iilabs3d.py
----------------
Batch-evaluates all *_odom.tum trajectories in a directory using the evo
Python API directly, then produces:
  - Box plots (translation RPE + rotation RPE) grouped by a chosen dimension
  - A LaTeX table with RMSE / mean / std / median per configuration

Trajectory naming convention expected:
  {aligner}_{formulation}_{mode}_{data_structure}_{sweep}_{param}_ricoslam_slam_odom.tum

  e.g.  dmap_p2pl_m1_dense_inliers_040_ricoslam_slam_odom.tum
        icp_p2p_m2_sparse_trans_300_ricoslam_slam_odom.tum

Usage:
    python3 eval_iilabs3d.py --dir <path_to_sequence_dir> [options]

Options:
    --dir           Directory containing ground_truth.tum and *_odom.tum files.
    --group-by      Dimension used to split figures: aligner | formulation |
                    mode | data_structure | sweep | param  [default: sweep]
    --filter KEY=VALUE [KEY=VALUE ...]
                    Restrict evaluation to files matching all given field values.
                    Keys: aligner, formulation, mode, data_structure, sweep, param
                    Example: --filter aligner=dmap formulation=p2pl mode=m1

Dependencies:
    pip install evo matplotlib numpy

Co-developed with Claude... Thanks!!!
"""

import argparse
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, fields, asdict
from typing import Optional

from evo.core import metrics, sync
from evo.tools import file_interface

# ---------------------------------------------------------------------------
# Evo evaluation parameters (match the README)
# ---------------------------------------------------------------------------

GT_FILE       = "ground_truth.tum"
MAX_TIME_DIFF = 0.01    # seconds
DELTA         = 10.0    # metres
DELTA_UNIT    = metrics.Unit.meters
REL_DELTA_TOL = 0.1

POSE_RELATIONS = {
    "trans": metrics.PoseRelation.translation_part,
    "rot":   metrics.PoseRelation.rotation_angle_deg,
}
METRIC_LABELS = {
    "trans": f"Translation RPE [%]",
    "rot":   "Rotation RPE [deg]",
}

# ---------------------------------------------------------------------------
# Configuration dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    aligner:        str   # dmap | icp
    formulation:    str   # p2p | p2pl
    mode:           str   # m0 | m1 | m2
    data_structure: str   # dense | sparse
    sweep:          str   # inliers | trans
    param:          str   # zero-padded integer string, e.g. "040"

    PATTERN = re.compile(
        r"(dmap|icp)_(p2pl|p2p)_(m\d+)_(dense|sparse)_(inliers|trans)_(\d+)_"
    )

    @classmethod
    def parse(cls, stem: str) -> Optional["Config"]:
        m = cls.PATTERN.search(stem)
        if not m:
            return None
        aligner, formulation, mode, data_structure, sweep, param = m.groups()
        return cls(aligner, formulation, mode, data_structure, sweep, param)

    def field_names(self):
        return [f.name for f in fields(self)]

    def label(self, group_by: str, x_field: str) -> str:
        """Human-readable x-axis tick: value of x_field."""
        return asdict(self)[x_field]

    def group_key(self, group_by: str) -> str:
        return asdict(self)[group_by]

    def matches(self, filters: dict) -> bool:
        d = asdict(self)
        return all(d.get(k) == v for k, v in filters.items())

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def evaluate(gt_path: Path, odom_path: Path) -> dict:
    """Run translation + rotation RPE. Returns {'trans': array, 'rot': array}."""
    traj_ref = file_interface.read_tum_trajectory_file(str(gt_path))
    traj_est = file_interface.read_tum_trajectory_file(str(odom_path))

    traj_ref_s, traj_est_s = sync.associate_trajectories(traj_ref, traj_est, max_diff=MAX_TIME_DIFF)
    traj_est_s.align(traj_ref_s, correct_scale=False)

    results = {}
    for key, pose_relation in POSE_RELATIONS.items():
        rpe = metrics.RPE(
            pose_relation=pose_relation,
            delta=DELTA,
            delta_unit=DELTA_UNIT,
            rel_delta_tol=REL_DELTA_TOL,
            all_pairs=False,
        )
        rpe.process_data((traj_ref_s, traj_est_s))
        arr = rpe.get_result().np_arrays["error_array"]
        # Normalise translation error to % of segment length
        if key == "trans":
            arr = arr / DELTA * 100.0
        # Normalise rotation error to deg / meter
        else:
            arr = arr / DELTA
        results[key] = arr
    return results


def compute_stats(arr: np.ndarray) -> dict:
    return {
        "rmse":   float(np.sqrt(np.mean(arr ** 2))),
        "mean":   float(np.mean(arr)),
        "std":    float(np.std(arr)),
        "median": float(np.median(arr)),
        "n":      int(len(arr)),
    }

# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

# # Assign a consistent colour to each unique value of the x-axis field
# _PALETTE = [
#     "#2166ac", "#d6604d", "#4dac26", "#7b2182",
#     "#e08214", "#1a9641", "#d73027", "#313695",
# ]

# def _colour_map(labels):
#     return {l: _PALETTE[i % len(_PALETTE)] for i, l in enumerate(sorted(set(labels)))}


# def make_boxplot(ax, data_by_label: dict, colours: dict,
#                  ylabel: str, xlabel: str):
#     labels = list(data_by_label.keys())
#     arrays = [data_by_label[l] for l in labels]
#     rng = np.random.default_rng(42)

#     for i, (label, arr) in enumerate(zip(labels, arrays), start=1):
#         colour = colours.get(label, "#555555")
#         bp = ax.boxplot(
#             [arr], positions=[i],
#             patch_artist=True, notch=False, vert=True, widths=0.55,
#             medianprops=dict(color="white", linewidth=2.0),
#             whiskerprops=dict(color=colour, linewidth=1.2),
#             capprops=dict(color=colour, linewidth=1.5),
#             flierprops=dict(marker="o", markersize=3,
#                             markerfacecolor=colour, markeredgewidth=0, alpha=0.5),
#             boxprops=dict(facecolor=colour + "44", edgecolor=colour, linewidth=1.2),
#         )
#         jitter = rng.uniform(-0.18, 0.18, size=len(arr))
#         ax.scatter(i + jitter, arr, s=7, alpha=0.30, color=colour,
#                    zorder=3, linewidths=0)

#     # Sample-count annotation
#     ymin = min(np.min(a) for a in arrays)
#     for i, arr in enumerate(arrays, start=1):
#         ax.text(i, ymin, f"n={len(arr)}", ha="center", va="top",
#                 fontsize=7, color="#555555")

#     ax.set_xticks(range(1, len(labels) + 1))
#     ax.set_xticklabels(labels, fontsize=9)
#     ax.set_ylabel(ylabel, fontsize=10)
#     ax.set_xlabel(xlabel, fontsize=9)
#     ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
#     ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.6)
#     ax.grid(axis="y", which="minor", linestyle=":", linewidth=0.4, alpha=0.4)
#     ax.set_axisbelow(True)


# def infer_x_field(group_by: str) -> str:
#     """
#     When figures are split by one field, the x-axis naturally shows the
#     parameter that varies most within each group.  Simple heuristic: use
#     'param' if group_by is 'sweep', otherwise use 'param' as a safe default.
#     Override: if group_by == 'param', use 'sweep'.
#     """
#     if group_by == "param":
#         return "sweep"
#     return "param"


# def plot_group(group_key: str, group_by: str, x_field: str,
#                records: list, out_dir: Path):
#     """
#     records: list of (Config, {'trans': array, 'rot': array})
#     The x-axis shows x_field values; one box per unique x_field value,
#     sorted naturally (numeric if possible, else lexicographic).
#     """
#     # Build { x_value: {metric: [arrays...]} }
#     bucket: dict = defaultdict(lambda: defaultdict(list))
#     for cfg, arrays in records:
#         x_val = asdict(cfg)[x_field]
#         for metric_key, arr in arrays.items():
#             if arr is not None and len(arr) > 0:
#                 bucket[x_val][metric_key].append(arr)

#     # Concatenate arrays from multiple configs that share the same x_val
#     data: dict = {}
#     for x_val, mdict in bucket.items():
#         data[x_val] = {k: np.concatenate(v) for k, v in mdict.items()}

#     def _sort_key(v):
#         try:
#             return (0, int(v))
#         except ValueError:
#             return (1, v)

#     sorted_x = sorted(data.keys(), key=_sort_key)
#     colours = _colour_map(sorted_x)

#     xlabel = x_field.replace("_", " ")
#     title = f"{group_by}={group_key}  (delta={DELTA:.0f} m, global alignment)"

#     fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
#     for ax, metric_key in zip(axes, ["trans", "rot"]):
#         ordered = {x: data[x][metric_key] for x in sorted_x if metric_key in data[x]}
#         make_boxplot(ax, ordered, colours,
#                      ylabel=METRIC_LABELS[metric_key], xlabel=xlabel)

#     fig.suptitle(title, fontsize=11, fontweight="bold")
#     fig.tight_layout()

#     safe_key = re.sub(r"[^a-zA-Z0-9_\-]", "_", group_key)
#     for ext in ("pdf", "png"):
#         p = out_dir / f"eval_{group_by}_{safe_key}.{ext}"
#         fig.savefig(p, bbox_inches="tight", dpi=150)
#         print(f"  Saved: {p}")
#     plt.close(fig)

# ---------------------------------------------------------------------------
# LaTeX table
# ---------------------------------------------------------------------------

_FIELD_DISPLAY = {
    "aligner":        "Aligner",
    "formulation":    "Formulation",
    "mode":           "Mode",
    "data_structure": "Structure",
    "sweep":          "Sweep",
    "param":          "Param",
}

LATEX_HEADER_TMPL = r"""\begin{{table}}[htbp]
\centering
\caption{{RPE evaluation on the \textit{{{seq}}} sequence of the IILABS3D dataset
         ($\delta = \SI{{10}}{{\metre}}$, global alignment).}}
\label{{tab:iilabs3d:{seq}:rpe}}
\setlength{{\tabcolsep}}{{4pt}}
\begin{{tabular}}{{{col_spec}}}
\toprule
# {header_cols} & \multicolumn{{4}}{{c}}{{Translation RPE [m]}} & \multicolumn{{4}}{{c}}{{Rotation RPE [\si{{\degree}}]}} \\
{header_cols} & \multicolumn{{1}}{{c}}{{Translation RPE [\%]}} & \multicolumn{{1}}{{c}}{{Rotation RPE [\\textdegree{{}}/m]}} \\
\cmidrule(lr){{{trans_cols}}}\\cmidrule(lr){{{rot_cols}}}
# {sub_header} & RMSE & Mean & Std & Median & RMSE & Mean & Std & Median \\
{sub_header} & Mean & Mean \\
\midrule"""

LATEX_FOOTER = r"""\bottomrule
\end{tabular}
\end{table}"""


def make_latex_table(records: list, key_fields: list, out_dir: Path, seq_name: str):
    """
    records: list of (Config, {'trans': array, 'rot': array})
    key_fields: ordered list of Config field names to use as row identifiers
                (all fields that actually vary in this dataset)
    """
    n_key = len(key_fields)
    # Column spec: n_key left-aligned key cols + 8 numeric cols
    col_spec = "l" * n_key + "r" * 8
    # Column numbers for cmidrule
    trans_start = n_key + 1
    rot_start   = n_key + 5
    header_cols = " & ".join(_FIELD_DISPLAY.get(f, f) for f in key_fields)
    sub_header  = " & ".join("" for _ in key_fields)  # blank under multi-col headers

    header = LATEX_HEADER_TMPL.format(
        seq=seq_name,
        col_spec=col_spec,
        header_cols=header_cols,
        trans_cols=f"{trans_start}-{rot_start - 1}",
        rot_cols=f"{rot_start}-{rot_start + 3}",
        sub_header=sub_header,
    )

    def fmtt(arr, key):
        if arr is None or len(arr) == 0:
            return "---"
        return f"{compute_stats(arr)[key]:.2f}"

    def fmtr(arr, key):
        if arr is None or len(arr) == 0:
            return "---"
        return f"{compute_stats(arr)[key]:.3f}"

    lines = [header]
    for cfg, arrays in sorted(records, key=lambda r: tuple(asdict(r[0])[f] for f in key_fields)):
        cells = [asdict(cfg)[f] for f in key_fields]
        t = arrays.get("trans")
        r = arrays.get("rot")
        row = (
            "  " + " & ".join(cells)
            # + f" & {fmtt(t,'rmse')} & {fmtt(t,'mean')} & {fmtt(t,'std')} & {fmtt(t,'median')}"
            # + f" & {fmtr(r,'rmse')} & {fmtr(r,'mean')} & {fmtr(r,'std')} & {fmtr(r,'median')}"
            + f" & {fmtt(t,'mean')}"
            + f" & {fmtr(r,'mean')}"
            + r" \\"
        )
        lines.append(row)

    lines.append(LATEX_FOOTER)

    out_path = out_dir / "eval_rpe_table.tex"
    out_path.write_text("\n".join(lines) + "\n")
    print(f"  Saved: {out_path}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="RPE evaluation for the IILABS3D using the evo Python API."
    )
    parser.add_argument("--dir", required=True, type=Path,
                        help="Directory with ground_truth.tum and *_odom.tum files.")
    parser.add_argument("--filter", nargs="*", metavar="KEY=VALUE", default=[],
                        help="Restrict to files matching all given field values.")

    # parser.add_argument("--group-by", default="sweep",
    #                     choices=["aligner", "formulation", "mode",
    #                              "data_structure", "sweep", "param"],
    #                     help="Config field used to split figures (default: sweep).")

    args = parser.parse_args()

    # Parse --filter arguments
    filters = {}
    for kv in args.filter:
        if "=" not in kv:
            sys.exit(f"[ERROR] --filter arguments must be KEY=VALUE, got: {kv!r}")
        k, v = kv.split("=", 1)
        if k not in Config.__dataclass_fields__:
            sys.exit(f"[ERROR] Unknown filter field: {k!r}. "
                     f"Valid: {list(Config.__dataclass_fields__)}")
        filters[k] = v

    data_dir = args.dir.resolve()
    gt_path  = data_dir / GT_FILE

    if not gt_path.exists():
        sys.exit(f"[ERROR] Ground truth not found: {gt_path}")

    odom_files = sorted(data_dir.glob("*_odom.tum"))
    if not odom_files:
        sys.exit(f"[ERROR] No *_odom.tum files found in {data_dir}")

    print(f"Ground truth : {gt_path}")
    print(f"Trajectories : {len(odom_files)} found")
    # for odom_path in odom_files:
    #     print(f"- {odom_path}")
    if filters:
        print(f"Filters      : {filters}")
    print()

    # -----------------------------------------------------------------------
    # Collect data
    # -----------------------------------------------------------------------
    records = []   # list of (Config, {'trans': array, 'rot': array})
    skipped = 0

    for odom_path in odom_files:
        cfg = Config.parse(odom_path.stem)
        if cfg is None:
            print(f"[SKIP] Unrecognized naming: {odom_path.name}")
            skipped += 1
            continue
        if not cfg.matches(filters):
            print(f"[SKIP/filter]   {odom_path.name}")
            skipped += 1
            continue

        print(f"[{cfg.aligner}/{cfg.formulation}/{cfg.mode}/"
              f"{cfg.data_structure}/{cfg.sweep}/{cfg.param}]")
        try:
            arrays = evaluate(gt_path, odom_path)
        except Exception as e:
            print(f"  [ERROR] {e}")
            continue

        for metric_key, arr in arrays.items():
            s = compute_stats(arr)
            print(f"  {metric_key:5s}: RMSE={s['rmse']:.4f}  mean={s['mean']:.4f}"
                  f"  std={s['std']:.4f}  median={s['median']:.4f}  n={s['n']}")
        records.append((cfg, arrays))

    if not records:
        sys.exit("[ERROR] No data collected — check file naming or filters.")

    print(f"\n{len(records)} trajectories evaluated, {skipped} skipped.\n")

    # -----------------------------------------------------------------------
    # Determine which fields actually vary (for the table key columns)
    # -----------------------------------------------------------------------
    all_field_values = {
        f: set(asdict(cfg)[f] for cfg, _ in records)
        for f in Config.__dataclass_fields__
    }
    varying_fields = [f for f, vals in all_field_values.items() if len(vals) > 1]
    # Always include sweep and param in the key even if constant
    for mandatory in ("sweep", "param"):
        if mandatory not in varying_fields:
            varying_fields.append(mandatory)
    # Preserve canonical field order
    canonical_order = [f.name for f in fields(Config)]
    key_fields = [f for f in canonical_order if f in varying_fields]

    # -----------------------------------------------------------------------
    # Plots: one figure per unique value of --group-by
    # -----------------------------------------------------------------------
    # group_by = args.group_by
    # x_field  = infer_x_field(group_by)

    # # Group records
    # groups: dict = defaultdict(list)
    # for cfg, arrays in records:
    #     groups[cfg.group_key(group_by)].append((cfg, arrays))

    # print("Generating plots ...")
    # for group_key, group_records in sorted(groups.items()):
    #     plot_group(group_key, group_by, x_field, group_records, data_dir)

    # -----------------------------------------------------------------------
    # LaTeX table
    # -----------------------------------------------------------------------
    seq_name = data_dir.name   # e.g. "nav_a_diff"
    print("\nGenerating LaTeX table ...")
    make_latex_table(records, key_fields, data_dir, seq_name)

    print("\nDone.")


if __name__ == "__main__":
    main()
