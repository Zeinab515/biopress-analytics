"""Descriptive analytics. Every rate carries numerator, denominator and a Wilson 95% CI."""
import math

import pandas as pd
from scipy.stats import chi2_contingency

GROUP_COLUMNS = {"ward": "Ward", "shift": "Shift", "profcat": "Profcat", "indication": "Indication"}


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def summary(df: pd.DataFrame) -> dict:
    n = int(len(df))
    k = int(df["complied"].sum())
    lo, hi = wilson_ci(k, n)
    return {"opportunities": n, "actions": k, "compliance_rate": k / n if n else None, "ci_low": lo, "ci_high": hi}


def by_group(df: pd.DataFrame, dimension: str) -> dict:
    if dimension not in GROUP_COLUMNS:
        raise KeyError(dimension)
    col = GROUP_COLUMNS[dimension]
    g = df.groupby(col)["complied"].agg(["sum", "count"]).reset_index()
    rows = []
    for _, r in g.iterrows():
        k, n = int(r["sum"]), int(r["count"])
        lo, hi = wilson_ci(k, n)
        rows.append({"group": r[col], "n": n, "complied": k, "rate": k / n, "ci_low": lo, "ci_high": hi})
    rows.sort(key=lambda x: -x["n"])

    table = pd.crosstab(df[col], df["complied"])
    chi2, p, dof, expected = chi2_contingency(table)
    verdict = ("Overall difference between groups is statistically detectable."
               if p < 0.05 else "No statistically detectable difference between groups; do not rank them.")
    return {
        "dimension": dimension,
        "rows": rows,
        "test": {"name": "chi-square test of independence", "chi2": float(chi2), "dof": int(dof),
                 "p_value": float(p), "min_expected_count": float(expected.min())},
        "note": "Descriptive only; differences are not evidence of a cause. " + verdict,
    }
