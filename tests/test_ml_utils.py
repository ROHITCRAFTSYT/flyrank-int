"""Unit tests for scripts/ml_utils.py.

These cover the pure, dataset-free helpers that the whole pipeline leans on:
normalisation, ranking, precision@k, JSON round-trips, and SVG escaping. They
run without the anonymized data slice, so they stay fast and deterministic and
catch regressions the smoke-test (which only checks the pipeline produces files)
would miss.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ml_utils  # noqa: E402


# --------------------------------------------------------------- normalize
def test_normalize_scales_to_unit_range():
    out = ml_utils.normalize(pd.Series([0, 5, 10]))
    assert out.tolist() == [0.0, 0.5, 1.0]


def test_normalize_constant_series_is_all_zero():
    out = ml_utils.normalize(pd.Series([7, 7, 7]))
    assert out.tolist() == [0.0, 0.0, 0.0]


def test_normalize_handles_nan_and_inf():
    out = ml_utils.normalize(pd.Series([np.nan, np.inf, -np.inf, 2, 4]))
    assert out.min() >= 0.0 and out.max() <= 1.0
    assert out.notna().all()


# --------------------------------------------------------------- ranks
def test_percentile_rank_orders_values():
    out = ml_utils.percentile_rank(pd.Series([10, 20, 30, 40]))
    assert out.iloc[0] < out.iloc[-1]
    assert 0.0 <= out.min() and out.max() <= 1.0


# --------------------------------------------------------------- precision@k
def test_precision_at_k_perfect_ranking():
    y = [1, 1, 0, 0]
    scores = [0.9, 0.8, 0.2, 0.1]
    assert ml_utils.precision_at_k(y, scores, 2) == 1.0


def test_precision_at_k_mixed_ranking():
    y = [0, 1, 1, 0]
    scores = [0.9, 0.8, 0.2, 0.1]
    # top-2 by score are indices 0 (y=0) and 1 (y=1) -> 0.5
    assert ml_utils.precision_at_k(y, scores, 2) == 0.5


def test_precision_at_k_empty_is_zero():
    assert ml_utils.precision_at_k([], [], 5) == 0.0


def test_precision_at_k_k_larger_than_data():
    assert ml_utils.precision_at_k([1, 0], [0.6, 0.4], 10) == 0.5


# --------------------------------------------------------------- safe_float
@pytest.mark.parametrize("value,expected", [
    ("3.5", 3.5), (2, 2.0), (None, 0.0), ("nope", 0.0),
    (float("inf"), 0.0), (float("nan"), 0.0),
])
def test_safe_float(value, expected):
    assert ml_utils.safe_float(value) == expected


def test_safe_float_custom_default():
    assert ml_utils.safe_float("x", default=-1.0) == -1.0


# --------------------------------------------------------------- to_bool
def test_to_bool_series_parses_truthy_strings():
    out = ml_utils.to_bool_series(pd.Series(["true", "1", "yes", "no", "0", ""]))
    assert out.tolist() == [True, True, True, False, False, False]


# --------------------------------------------------------------- json io
def test_json_round_trip(tmp_path):
    path = tmp_path / "nested" / "payload.json"
    payload = {"b": 2, "a": 1}
    ml_utils.write_json(path, payload)
    assert path.exists()
    assert ml_utils.read_json(path) == payload


# --------------------------------------------------------------- xml / svg
def test_escape_xml_escapes_all_specials():
    out = ml_utils.escape_xml("a & b < c > d \" e ' f")
    for ch in "&<>\"'":
        assert ch not in out.replace("&amp;", "").replace("&lt;", "") \
            .replace("&gt;", "").replace("&quot;", "").replace("&apos;", "")


def test_svg_bar_chart_writes_valid_markup(tmp_path):
    path = tmp_path / "chart.svg"
    ml_utils.simple_svg_bar_chart("Top pages", ["a & b", "c<d"], [10, 20], path)
    text = path.read_text()
    assert text.startswith("<svg")
    assert text.strip().endswith("</svg>")
    assert "&amp;" in text and "&lt;" in text  # labels were escaped


def test_svg_bar_chart_handles_empty_values(tmp_path):
    path = tmp_path / "empty.svg"
    ml_utils.simple_svg_bar_chart("Nothing", [], [], path)
    assert path.read_text().startswith("<svg")


# --------------------------------------------------------------- display_path
def test_display_path_relative_inside_repo():
    inside = ml_utils.ROOT / "scripts" / "ml_utils.py"
    shown = ml_utils.display_path(inside)
    # Repo-relative, so the absolute root prefix is stripped off.
    assert shown.endswith("ml_utils.py")
    assert str(ml_utils.ROOT) not in shown


def test_display_path_outside_repo_is_absolute():
    outside = Path(ml_utils.ROOT).parent / "somewhere_else.txt"
    assert ml_utils.display_path(outside).endswith("somewhere_else.txt")
