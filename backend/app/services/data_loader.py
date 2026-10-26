"""Load the raw CSV (read-only) and expose the analysis frame.

Policy (see docs/data_audit.md):
- Raw file is never modified.
- Only ALLOWED_FEATURES may be used as model inputs.
- HHaction and Missedbutglove are deterministic functions of Complied (target leakage).
- Opp is a sequential observation id, not a feature.
"""
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["Ward", "Profcat", "Shift", "Opp", "Indication", "HHaction", "Missedbutglove", "Complied"]
ALLOWED_FEATURES = ["Ward", "Profcat", "Shift", "Indication"]
LEAKY_COLUMNS = ["HHaction", "Missedbutglove"]
ID_COLUMNS = ["Opp"]

DEFAULT_PATH = Path(__file__).resolve().parents[3] / "data" / "raw" / "hand_hygiene_data_labeled.csv"


def validate_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    bad = set(df["Complied"].dropna().unique()) - {"Yes", "No"}
    if bad:
        raise ValueError(f"Unexpected Complied values: {sorted(bad)}")


def load_frame(path=None) -> pd.DataFrame:
    path = Path(path or os.getenv("DATA_PATH") or DEFAULT_PATH)
    df = pd.read_csv(path)
    validate_columns(df)
    df = df.copy()
    df["complied"] = (df["Complied"] == "Yes").astype(int)
    return df


@lru_cache(maxsize=1)
def get_frame() -> pd.DataFrame:
    return load_frame()
