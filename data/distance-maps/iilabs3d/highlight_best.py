"""
highlight_best.py
-----------------
Reads 6 CSV files with SLAM evaluation results (RTE / RRE) across 4 scenarios
(nav_a_diff, nav_a_omni, loop, slippage), identifies the best results per
metric and scenario using threshold-based comparison, and outputs one LaTeX
table per CSV file with \bfseries applied to the best-within-threshold cells.

CSV structure (no named header row):
  col 0 : method  (dmap_p2p | dmap_p2pl | icp_p2p | icp_p2pl)
  col 1 : param   (0.50m … 3.00m | 40% … 90%)
  col 2 : nav_a_diff_rte
  col 3 : nav_a_diff_rre
  col 4 : nav_a_omni_rte
  col 5 : nav_a_omni_rre
  col 6 : loop_rte
  col 7 : loop_rre
  col 8 : slippage_rte
  col 9 : slippage_rre

Thresholds (match displayed precision):
  RTE : ±0.05   (2 decimal places)
  RRE : ±0.005  (3 decimal places)

Usage:
  python highlight_best.py               # uses INPUT_FILES list below
  python highlight_best.py --out-dir out # write .tex files to ./out/

Co-developed with Claude... Thanks!!!
"""

import argparse
import csv
import math
import os
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Configuration — edit paths and settings here
# ---------------------------------------------------------------------------

INPUT_FILES = [
    "results_iilabs3d_res-0.03m_dmax-0.50m_rmax-10.0m_m0.csv",
    "results_iilabs3d_res-0.03m_dmax-0.50m_rmax-10.0m_m0-1-2.csv",
    "results_iilabs3d_res-0.03m_dmax-0.50m_rmax-20.0m_m0.csv",
    "results_iilabs3d_res-0.03m_dmax-0.50m_rmax-20.0m_m0-1-2.csv",
    "results_iilabs3d_res-0.03m_dmax-0.50m_rmax-30.0m_m0.csv",
    "results_iilabs3d_res-0.03m_dmax-0.50m_rmax-30.0m_m0-1-2.csv",
]

SCENARIOS = ["nav_a_diff", "nav_a_omni", "loop", "slippage"]

RTE_DECIMALS  = 2
RRE_DECIMALS  = 3
RTE_THRESHOLD = 0.05
RRE_THRESHOLD = 0.005

# Column indices in the CSV (0-based)
COL_METHOD = 0
COL_PARAM  = 1
# Scenario columns start at index 2, in pairs: (rte, rre) per scenario
SCENARIO_COL_START = 2


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Row:
    method: str
    param: str
    # dict: scenario -> (rte, rre) stored as floats (None if missing)
    values: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_csv(path: str) -> list[Row]:
    rows = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for i, raw in enumerate(reader):
            # Skip the header row (first row, starts with empty cell)
            if i == 0:
                continue
            # Strip whitespace from every cell
            raw = [c.strip() for c in raw]
            # Skip completely empty rows
            if not any(raw):
                continue

            method = raw[COL_METHOD]
            param  = raw[COL_PARAM]
            values = {}
            for s_idx, scenario in enumerate(SCENARIOS):
                col_rte = SCENARIO_COL_START + s_idx * 2
                col_rre = SCENARIO_COL_START + s_idx * 2 + 1
                try:
                    rte = float(raw[col_rte])
                except (IndexError, ValueError):
                    rte = None
                try:
                    rre = float(raw[col_rre])
                except (IndexError, ValueError):
                    rre = None
                values[scenario] = (rte, rre)

            rows.append(Row(method=method, param=param, values=values))
    return rows


# ---------------------------------------------------------------------------
# Best-value detection
# ---------------------------------------------------------------------------

def find_best(rows: list[Row], scenario: str, metric: str) -> float | None:
    """Return the minimum finite value for a given scenario and metric."""
    idx = 0 if metric == "rte" else 1
    vals = [r.values[scenario][idx] for r in rows if r.values[scenario][idx] is not None]
    return min(vals) if vals else None


def is_best(value: float, best: float, threshold: float) -> bool:
    return math.isclose(value, best, abs_tol=threshold)


# ---------------------------------------------------------------------------
# LaTeX formatting
# ---------------------------------------------------------------------------

def fmt(value: float | None, decimals: int, bold: bool) -> str:
    if value is None:
        return "--"
    s = f"{value:.{decimals}f}"
    return rf"\bfseries {s}" if bold else s


def build_latex_table(rows: list[Row], caption_hint: str = "") -> str:
    """
    Builds a LaTeX tabular block.

    Layout:
      Method | Param | nav_a_diff (RTE RRE) | nav_a_omni (RTE RRE) | loop (RTE RRE) | slippage (RTE RRE)
    """
    # Pre-compute best values for every scenario x metric
    bests: dict[tuple[str, str], float | None] = {}
    for scenario in SCENARIOS:
        bests[(scenario, "rte")] = find_best(rows, scenario, "rte")
        bests[(scenario, "rre")] = find_best(rows, scenario, "rre")

    n_scenarios = len(SCENARIOS)

    # --- column spec & headers ---
    col_spec = "ll" + "".join(["cc"] * n_scenarios)
    scenario_headers = " & ".join(
        rf"\multicolumn{{2}}{{c}}{{\texttt{{{s.replace('_', r'\_')}}}}}"
        for s in SCENARIOS
    )
    metric_headers = " & ".join(
        [r"\multicolumn{1}{c}{RTE} & \multicolumn{1}{c}{RRE}"] * n_scenarios
    )

    lines = []
    if caption_hint:
        lines.append(f"% {caption_hint}")
    lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
    lines.append(r"\toprule")
    lines.append(rf"Method & Param & {scenario_headers} \\")

    # cmidrule under each scenario pair (1-based; cols 1=Method, 2=Param)
    cmidrules = []
    for i in range(n_scenarios):
        start = 3 + i * 2
        end   = start + 1
        cmidrules.append(rf"\cmidrule(lr){{{start}-{end}}}")
    lines.append("".join(cmidrules))
    lines.append(rf"& & {metric_headers} \\")
    lines.append(r"\midrule")

    # --- data rows ---
    prev_method = None
    for row in rows:
        # Thin separator between method groups
        if prev_method is not None and row.method != prev_method:
            lines.append(r"\midrule")
        prev_method = row.method

        cells = [row.method.replace("_", r"\_"), row.param]
        for scenario in SCENARIOS:
            rte, rre = row.values[scenario]
            best_rte = bests[(scenario, "rte")]
            best_rre = bests[(scenario, "rre")]

            bold_rte = (rte is not None and best_rte is not None
                        and is_best(rte, best_rte, RTE_THRESHOLD))
            bold_rre = (rre is not None and best_rre is not None
                        and is_best(rre, best_rre, RRE_THRESHOLD))

            cells.append(fmt(rte, RTE_DECIMALS, bold_rte))
            cells.append(fmt(rre, RRE_DECIMALS, bold_rre))

        lines.append(" & ".join(cells) + r" \\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Summary (human-readable, for quick sanity check)
# ---------------------------------------------------------------------------

def print_summary(rows: list[Row], label: str) -> None:
    print(f"\n{'='*60}")
    print(f"FILE: {label}")
    print(f"{'='*60}")
    for scenario in SCENARIOS:
        print(f"\n  Scenario: {scenario}")
        for metric, threshold, decimals in [
            ("rte", RTE_THRESHOLD, RTE_DECIMALS),
            ("rre", RRE_THRESHOLD, RRE_DECIMALS),
        ]:
            best = find_best(rows, scenario, metric)
            if best is None:
                continue
            idx = 0 if metric == "rte" else 1
            winners = [
                f"{r.method}/{r.param}"
                for r in rows
                if r.values[scenario][idx] is not None
                and is_best(r.values[scenario][idx], best, threshold)
            ]
            print(f"    {metric.upper()}  best={best:.{decimals}f}  ±{threshold}  →  {', '.join(winners)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Highlight best RTE/RRE across 4 scenarios in 6 CSV files."
    )
    p.add_argument("--inputs", "-i", nargs="+", default=None,
                   help="CSV files to process (default: INPUT_FILES in script)")
    p.add_argument("--out-dir", "-o", default=None,
                   help="Directory for .tex output files (default: print to stdout)")
    p.add_argument("--no-summary", action="store_true",
                   help="Suppress human-readable summary")
    return p.parse_args()


def main():
    args = parse_args()
    files = args.inputs if args.inputs else INPUT_FILES

    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)

    for path in files:
        label = os.path.basename(path)
        rows  = parse_csv(path)

        if not args.no_summary:
            print_summary(rows, label)

        latex = build_latex_table(rows, caption_hint=label)

        if args.out_dir:
            stem    = os.path.splitext(label)[0]
            outpath = os.path.join(args.out_dir, stem + ".tex")
            with open(outpath, "w") as f:
                f.write(latex + "\n")
            print(f"\n  → Written: {outpath}")
        else:
            print(f"\n{'='*60}")
            print(f"LaTeX — {label}")
            print(f"{'='*60}")
            print(latex)


if __name__ == "__main__":
    main()
