import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402
from app.services import analytics  # noqa: E402
from app.services.data_loader import ALLOWED_FEATURES, LEAKY_COLUMNS, get_frame, validate_columns  # noqa: E402

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_summary_matches_published_figures():
    s = client.get("/api/v1/analytics/summary").json()
    assert s["opportunities"] == 917
    assert s["actions"] == 202
    assert round(s["compliance_rate"] * 100, 1) == 22.0


@pytest.mark.parametrize("path,dim", [("by-ward", "ward"), ("by-shift", "shift"), ("by-indication", "indication"), ("by-profcat", "profcat")])
def test_group_totals_are_consistent(path, dim):
    r = client.get(f"/api/v1/analytics/{path}").json()
    assert r["dimension"] == dim
    assert sum(x["n"] for x in r["rows"]) == 917
    assert sum(x["complied"] for x in r["rows"]) == 202
    for x in r["rows"]:
        assert x["ci_low"] <= x["rate"] <= x["ci_high"]


def test_indication_is_the_only_significant_dimension():
    p = {d: client.get(f"/api/v1/analytics/by-{d}").json()["test"]["p_value"] for d in ["ward", "shift", "profcat", "indication"]}
    assert p["indication"] < 0.001
    assert p["ward"] > 0.05 and p["shift"] > 0.05 and p["profcat"] > 0.05


def test_leakage_columns_are_deterministic_of_target():
    df = get_frame()
    assert (df["HHaction"].notna() == (df["complied"] == 1)).all()
    assert (df["Missedbutglove"].isna() == (df["complied"] == 1)).all()


def test_leaky_columns_not_in_allowed_features():
    assert not set(LEAKY_COLUMNS) & set(ALLOWED_FEATURES)
    assert "Opp" not in ALLOWED_FEATURES


def test_missing_required_column_is_rejected():
    with pytest.raises(ValueError):
        validate_columns(get_frame().drop(columns=["Shift"]))


def test_wilson_ci_edges():
    assert analytics.wilson_ci(0, 10)[0] == 0.0
    assert analytics.wilson_ci(10, 10)[1] == 1.0
