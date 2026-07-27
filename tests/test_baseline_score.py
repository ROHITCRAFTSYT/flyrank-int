"""Unit tests for the baseline scorer's decision rules.

reason_codes and suggested_action are the transparent, deterministic heuristics
behind every "refresh this page" recommendation. Their thresholds are the model,
so a silent change here changes the output queue — worth pinning. Pure per-row
logic; no dataset needed. The module name starts with a digit, so it's loaded by
path.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

_spec = importlib.util.spec_from_file_location("baseline_score", SCRIPTS / "02_baseline_score.py")
baseline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(baseline)


def _row(**over) -> pd.Series:
    base = dict(
        days_since_last_update=0, impressions_90d=0, trend_direction="flat",
        word_count=2000, avg_position=0, content_age_days=0, ctr=5.0,
        sessions_90d=0, engagement_rate=50.0, scroll_rate=50.0,
    )
    base.update(over)
    return pd.Series(base)


# --------------------------------------------------------------- reason_codes
def test_healthy_page_gets_general_review_only():
    assert baseline.reason_codes(_row()) == ["general_refresh_review"]


def test_stale_visible_page_flagged():
    r = _row(days_since_last_update=200, impressions_90d=800)
    assert "stale_visible_page" in baseline.reason_codes(r)


def test_declining_with_demand_flagged():
    r = _row(trend_direction="Down", impressions_90d=150)
    assert "declining_with_demand" in baseline.reason_codes(r)


def test_thin_visible_page_flagged():
    r = _row(word_count=800, impressions_90d=300)
    assert "thin_visible_page" in baseline.reason_codes(r)


def test_low_ctr_visible_page_flagged():
    r = _row(impressions_90d=600, avg_position=8, ctr=0.3)
    assert "low_ctr_visible_page" in baseline.reason_codes(r)


def test_low_engagement_visible_page_flagged():
    r = _row(sessions_90d=50, engagement_rate=15)
    assert "low_engagement_visible_page" in baseline.reason_codes(r)


def test_thresholds_are_exclusive_at_the_boundary():
    # word_count exactly 1200 is NOT thin (rule is < 1200)
    r = _row(word_count=1200, impressions_90d=300)
    assert "thin_visible_page" not in baseline.reason_codes(r)


# --------------------------------------------------------------- action
def test_suggested_action_priority_order():
    assert baseline.suggested_action(_row(reason_codes="thin_visible_page")) == "expand_and_refresh"
    assert baseline.suggested_action(_row(reason_codes="low_ctr_visible_page")) == "refresh_and_review_ctr"
    assert baseline.suggested_action(_row(reason_codes="stale_visible_page")) == "refresh"
    assert baseline.suggested_action(_row(reason_codes="general_refresh_review")) == "monitor"


def test_suggested_action_thin_beats_stale():
    # both present -> the higher-priority "expand_and_refresh" wins
    r = _row(reason_codes="stale_visible_page|thin_visible_page")
    assert baseline.suggested_action(r) == "expand_and_refresh"
