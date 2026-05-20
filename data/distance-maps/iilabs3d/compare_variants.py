"""
compare_variants.py
-------------------
Generic comparison of two method variants across SLAM evaluation CSV files.

Each CSV file has the structure:
  col 0 : method  (dmap_p2p | dmap_p2pl | icp_p2p | icp_p2pl)
  col 1 : param   (0.50m … 3.00m | 40% … 90%)
  cols 2+: pairs of (rte, rre) per scenario, in order defined by SCENARIOS

Thresholds (match displayed precision):
  RTE : ±0.05   (2 decimal places)
  RRE : ±0.005  (3 decimal places)

Usage examples:
  # dmap_p2pl M0 vs icp_p2pl M0  (same file, two methods)
  python compare_variants.py \\
      --file-a results_m0.csv --method-a dmap_p2pl \\
      --file-b results_m0.csv --method-b icp_p2pl

  # dmap_p2p M0 vs dmap_p2p M0-1-2  (same method, two files)
  python compare_variants.py \\
      --file-a results_m0.csv     --method-a dmap_p2p \\
      --file-b results_m0-1-2.csv --method-b dmap_p2p

  # Same as above but only for specific scenarios and params
  python compare_variants.py \\
      --file-a results_m0.csv --method-a dmap_p2p \\
      --file-b results_m0.csv --method-b icp_p2p  \\
      --scenarios nav_a_diff loop \\
      --params 1.00m 2.00m 50%

  # Export results
  python compare_variants.py ... --out-csv diff.csv --out-tex summary.tex

By with Claude... Thanks!!! Useful as always!!!
"""

import argparse
import csv
import math
import os
import statistics
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Defaults (overridable via CLI)
# ---------------------------------------------------------------------------

SCENARIOS_ALL = ["nav_a_diff", "nav_a_omni", "loop", "slippage"]

RTE_DECIMALS  = 2
RRE_DECIMALS  = 3
RTE_THRESHOLD = 0.05
# RTE_THRESHOLD = 0.10
RRE_THRESHOLD = 0.005
# RRE_THRESHOLD = 0.010
OUTLIER_REL_THRESH = 5.0   # % relative diff above which a pair is flagged

COL_METHOD         = 0
COL_PARAM          = 1
SCENARIO_COL_START = 2


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Row:
    method: str
    param: str
    values: dict = field(default_factory=dict)  # scenario -> (rte, rre)


@dataclass
class DiffRecord:
    scenario: str
    param: str
    val_a_rte: float | None
    val_b_rte: float | None
    val_a_rre: float | None
    val_b_rre: float | None

    def _abs(self, a, b):
        return None if (a is None or b is None) else abs(a - b)

    def _rel(self, a, b):
        return None if (a is None or b is None or b == 0) else abs(a - b) / b * 100

    def _within(self, a, b, thresh):
        d = self._abs(a, b)
        return None if d is None else d <= thresh

    @property
    def abs_diff_rte(self):  return self._abs(self.val_a_rte, self.val_b_rte)
    @property
    def rel_diff_rte(self):  return self._rel(self.val_a_rte, self.val_b_rte)
    @property
    def within_rte(self):    return self._within(self.val_a_rte, self.val_b_rte, RTE_THRESHOLD)

    @property
    def abs_diff_rre(self):  return self._abs(self.val_a_rre, self.val_b_rre)
    @property
    def rel_diff_rre(self):  return self._rel(self.val_a_rre, self.val_b_rre)
    @property
    def within_rre(self):    return self._within(self.val_a_rre, self.val_b_rre, RRE_THRESHOLD)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_csv(path: str, scenarios: list[str]) -> list[Row]:
    rows = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for i, raw in enumerate(reader):
            if i == 0:
                continue                      # header row
            raw = [c.strip() for c in raw]
            if not any(raw):
                continue
            method = raw[COL_METHOD]
            param  = raw[COL_PARAM]
            values = {}
            for s_idx, scenario in enumerate(scenarios):
                col_rte = SCENARIO_COL_START + s_idx * 2
                col_rre = SCENARIO_COL_START + s_idx * 2 + 1
                try:    rte = float(raw[col_rte])
                except: rte = None
                try:    rre = float(raw[col_rre])
                except: rre = None
                values[scenario] = (rte, rre)
            rows.append(Row(method=method, param=param, values=values))
    return rows


def index_rows(rows: list[Row]) -> dict[tuple[str, str], Row]:
    """Index by (method, param). Last one wins on duplicates."""
    return {(r.method, r.param): r for r in rows}


# ---------------------------------------------------------------------------
# Core comparison
# ---------------------------------------------------------------------------

def build_diffs(
    rows_a: list[Row], method_a: str,
    rows_b: list[Row], method_b: str,
    scenarios: list[str],
    param_filter: list[str] | None,
) -> list[DiffRecord]:
    idx_a = index_rows(rows_a)
    idx_b = index_rows(rows_b)

    # Params present in both, ordered by appearance in file A
    params_a = [r.param for r in rows_a if r.method == method_a]
    params_b = {r.param for r in rows_b if r.method == method_b}
    common   = [p for p in params_a if p in params_b]

    if param_filter:
        common = [p for p in common if p in param_filter]

    if not common:
        raise ValueError(
            f"No common params found between '{method_a}' and '{method_b}'"
            + (f" (filter: {param_filter})" if param_filter else "")
        )

    diffs = []
    for param in common:
        row_a = idx_a.get((method_a, param))
        row_b = idx_b.get((method_b, param))
        if row_a is None or row_b is None:
            continue
        for scenario in scenarios:
            a_rte, a_rre = row_a.values.get(scenario, (None, None))
            b_rte, b_rre = row_b.values.get(scenario, (None, None))
            diffs.append(DiffRecord(
                scenario=scenario, param=param,
                val_a_rte=a_rte, val_b_rte=b_rte,
                val_a_rre=a_rre, val_b_rre=b_rre,
            ))
    return diffs


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def safe_stats(values: list) -> dict:
    v = [x for x in values if x is not None]
    if not v:
        return dict(n=0, mean=None, median=None, max=None, stdev=None)
    return dict(
        n=len(v), mean=statistics.mean(v), median=statistics.median(v),
        max=max(v), stdev=statistics.stdev(v) if len(v) > 1 else 0.0,
    )


def within_pct(records: list[DiffRecord], metric: str) -> float:
    bools = [getattr(r, f"within_{metric}") for r in records]
    bools = [b for b in bools if b is not None]
    return sum(bools) / len(bools) * 100 if bools else float("nan")


# ---------------------------------------------------------------------------
# Console output
# ---------------------------------------------------------------------------

def _stat_line(label: str, s: dict, decimals: int, unit: str = "") -> str:
    if s["mean"] is None:
        return f"    {label}: no data"
    u = f" {unit}" if unit else ""
    return (f"    {label}: "
            f"mean={s['mean']:.{decimals}f}{u}  "
            f"median={s['median']:.{decimals}f}{u}  "
            f"max={s['max']:.{decimals}f}{u}  "
            f"stdev={s['stdev']:.{decimals}f}{u}  "
            f"(n={s['n']})")


def print_comparison(
    diffs: list[DiffRecord],
    label_a: str, label_b: str,
    scenarios: list[str],
    outlier_thresh: float,
) -> None:
    sep = "=" * 70
    print(f"\n{sep}")
    print(f"COMPARISON:  {label_a}  vs  {label_b}")
    print(sep)

    for scenario in scenarios:
        recs = [d for d in diffs if d.scenario == scenario]
        print(f"\n  [{scenario}]  ({len(recs)} param configs)")
        for metric, decimals in [("rte", RTE_DECIMALS), ("rre", RRE_DECIMALS)]:
            abs_s = safe_stats([getattr(r, f"abs_diff_{metric}") for r in recs])
            rel_s = safe_stats([getattr(r, f"rel_diff_{metric}") for r in recs])
            pct   = within_pct(recs, metric)
            print(f"    {metric.upper()}  within-threshold: {pct:.1f}%")
            print(_stat_line("     abs diff", abs_s, decimals))
            print(_stat_line("     rel diff", rel_s, 1, "%"))

    # Global across all scenarios
    print(f"\n  [ALL SCENARIOS]")
    for metric, decimals in [("rte", RTE_DECIMALS), ("rre", RRE_DECIMALS)]:
        abs_s = safe_stats([getattr(r, f"abs_diff_{metric}") for r in diffs])
        rel_s = safe_stats([getattr(r, f"rel_diff_{metric}") for r in diffs])
        pct   = within_pct(diffs, metric)
        print(f"    {metric.upper()}  within-threshold: {pct:.1f}%")
        print(_stat_line("     abs diff", abs_s, decimals))
        print(_stat_line("     rel diff", rel_s, 1, "%"))

    # Outliers
    print(f"\n  OUTLIERS  (rel diff > {outlier_thresh}% in any metric):")
    outliers = [
        d for d in diffs
        if (d.rel_diff_rte is not None and d.rel_diff_rte > outlier_thresh)
        or (d.rel_diff_rre is not None and d.rel_diff_rre > outlier_thresh)
    ]
    if not outliers:
        print(f"    None — variants agree within {outlier_thresh}% everywhere.")
    else:
        for o in outliers:
            rte_s = f"RTE Δ={o.rel_diff_rte:.1f}%" if o.rel_diff_rte is not None else ""
            rre_s = f"RRE Δ={o.rel_diff_rre:.1f}%" if o.rel_diff_rre is not None else ""
            print(f"    {o.scenario}  |  {o.param}  |  {rte_s}  {rre_s}")


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def export_csv(diffs: list[DiffRecord], label_a: str, label_b: str, path: str) -> None:
    fields = [
        "scenario", "param",
        f"rte_{label_a}", f"rte_{label_b}", "abs_diff_rte", "rel_diff_rte_%", "within_thresh_rte",
        f"rre_{label_a}", f"rre_{label_b}", "abs_diff_rre", "rel_diff_rre_%", "within_thresh_rre",
    ]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for d in diffs:
            def _f(v, dec): return f"{v:.{dec}f}" if v is not None else ""
            def _b(v):      return "" if v is None else str(v)
            w.writerow({
                "scenario":              d.scenario,
                "param":                 d.param,
                f"rte_{label_a}":        _f(d.val_a_rte, RTE_DECIMALS),
                f"rte_{label_b}":        _f(d.val_b_rte, RTE_DECIMALS),
                "abs_diff_rte":          _f(d.abs_diff_rte, RTE_DECIMALS),
                "rel_diff_rte_%":        _f(d.rel_diff_rte, 1),
                "within_thresh_rte":     _b(d.within_rte),
                f"rre_{label_a}":        _f(d.val_a_rre, RRE_DECIMALS),
                f"rre_{label_b}":        _f(d.val_b_rre, RRE_DECIMALS),
                "abs_diff_rre":          _f(d.abs_diff_rre, RRE_DECIMALS),
                "rel_diff_rre_%":        _f(d.rel_diff_rre, 1),
                "within_thresh_rre":     _b(d.within_rre),
            })
    print(f"\nFull diff table → {path}")


# ---------------------------------------------------------------------------
# LaTeX summary table
# ---------------------------------------------------------------------------

def build_latex_summary(
    diffs: list[DiffRecord],
    scenarios: list[str],
    label_a: str, label_b: str,
) -> str:
    lines = [
        rf"% Equivalence: {label_a} vs {label_b}",
        r"\begin{tabular}{lcccccccc}",
        r"\toprule",
        r"& \multicolumn{4}{c}{\textbf{RTE}} & \multicolumn{4}{c}{\textbf{RRE}} \\",
        r"\cmidrule(lr){2-5}\cmidrule(lr){6-9}",
        r"Scenario"
        r" & $\bar{\Delta}$ & $\Delta_{\max}$"
        r" & $\bar{\Delta}_{\mathrm{rel}}$\,[\%] & $\leq\varepsilon$\,[\%]"
        r" & $\bar{\Delta}$ & $\Delta_{\max}$"
        r" & $\bar{\Delta}_{\mathrm{rel}}$\,[\%] & $\leq\varepsilon$\,[\%] \\",
        r"\midrule",
    ]

    def _row(recs, row_label):
        cells = [row_label.replace("_", r"\_")]
        for metric, decimals in [("rte", RTE_DECIMALS), ("rre", RRE_DECIMALS)]:
            s_abs = safe_stats([getattr(r, f"abs_diff_{metric}") for r in recs])
            s_rel = safe_stats([getattr(r, f"rel_diff_{metric}") for r in recs])
            pct   = within_pct(recs, metric)
            cells += [
                f"{s_abs['mean']:.{decimals}f}" if s_abs["mean"] is not None else "--",
                f"{s_abs['max']:.{decimals}f}"  if s_abs["max"]  is not None else "--",
                f"{s_rel['mean']:.1f}"           if s_rel["mean"] is not None else "--",
                f"{pct:.1f}"                     if not math.isnan(pct)        else "--",
            ]
        return " & ".join(cells) + r" \\"

    for scenario in scenarios:
        recs = [d for d in diffs if d.scenario == scenario]
        lines.append(_row(recs, scenario))

    lines.append(r"\midrule")
    lines.append(_row(diffs, r"\textbf{All}"))
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Compare two method variants from SLAM evaluation CSVs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    # Variant A
    p.add_argument("--file-a",   required=True, help="CSV file for variant A")
    p.add_argument("--method-a", required=True, help="Method name in file A (e.g. dmap_p2pl)")
    # Variant B
    p.add_argument("--file-b",   required=True, help="CSV file for variant B (can be same as A)")
    p.add_argument("--method-b", required=True, help="Method name in file B (e.g. icp_p2pl)")
    # Filters
    p.add_argument("--scenarios", nargs="+", default=None,
                   help=f"Scenarios to include (default: all {SCENARIOS_ALL})")
    p.add_argument("--params", nargs="+", default=None,
                   help="Param values to include, e.g. 1.00m 2.00m 50%% (default: all common)")
    # Output
    p.add_argument("--out-csv",  default=None, help="Export full diff table as CSV")
    p.add_argument("--out-tex",  default=None, help="Export summary as LaTeX table")
    p.add_argument("--outlier-thresh", type=float, default=OUTLIER_REL_THRESH,
                   help=f"Rel diff %% threshold for outlier flag (default: {OUTLIER_REL_THRESH})")
    return p.parse_args()


def main():
    args = parse_args()

    scenarios = args.scenarios if args.scenarios else SCENARIOS_ALL

    # Human-readable labels for output headers
    label_a = f"{args.method_a}@{os.path.basename(args.file_a)}"
    label_b = f"{args.method_b}@{os.path.basename(args.file_b)}"
    # Shorten if same file
    if args.file_a == args.file_b:
        fname   = os.path.basename(args.file_a)
        label_a = f"{args.method_a}@{fname}"
        label_b = f"{args.method_b}@{fname}"

    rows_a = parse_csv(args.file_a, scenarios)
    rows_b = parse_csv(args.file_b, scenarios)

    diffs = build_diffs(
        rows_a, args.method_a,
        rows_b, args.method_b,
        scenarios,
        param_filter=args.params,
    )

    print_comparison(diffs, label_a, label_b, scenarios, args.outlier_thresh)

    if args.out_csv:
        export_csv(diffs, args.method_a, args.method_b, args.out_csv)

    if args.out_tex:
        latex = build_latex_summary(diffs, scenarios, label_a, label_b)
        with open(args.out_tex, "w") as f:
            f.write(latex + "\n")
        print(f"LaTeX summary table → {args.out_tex}")


if __name__ == "__main__":
    main()
