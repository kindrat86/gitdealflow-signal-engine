"""Unit tests for the pure computation functions in signal_engine_core.

Run:  pip install pytest && pytest -q
No network access or GitHub token required.
"""

import signal_engine_core as se


def _engine():
    return se.SignalEngine(se.GitHubClient(token="test-token"))


def test_gini_uniform_is_zero():
    assert abs(se.gini([1, 1, 1, 1])) < 1e-9


def test_gini_fully_concentrated():
    # max Gini for n values is (n-1)/n, not 1.0
    assert abs(se.gini([10, 0, 0, 0]) - 0.75) < 1e-9


def test_gini_no_activity_is_max_penalty():
    # Documented design choice: no activity -> maximally concentrated (1.0),
    # so dead repos never earn the diversity bonus.
    assert se.gini([]) == 1.0
    assert se.gini([0, 0, 0]) == 1.0


def test_composite_score_bounds():
    e = _engine()
    assert 0.0 <= e.composite_score(0.0, 0.0, 0, 1.0) <= 100.0
    assert 0.0 <= e.composite_score(10.0, 10.0, 50, 0.0) <= 100.0


def test_composite_score_readme_example():
    # The exact numbers shown in the README example output
    e = _engine()
    assert round(e.composite_score(1.524, 0.68, 4, 0.212), 1) == 76.6


def test_classify_signal_priority():
    e = _engine()
    # Contributor growth >= +50% dominates
    assert e.classify_signal(1.524, 0.68, 4) == "Engineering Hiring Burst"
    # >= 3 new repos without hiring burst
    assert e.classify_signal(0.2, 0.1, 3) == "Infrastructure Buildout"
    # Velocity spike >= +150%
    assert e.classify_signal(1.6, 0.1, 0) == "Deploy Frequency Spike"
    # Fallback
    assert e.classify_signal(0.5, 0.1, 0) == "Framework Migration"


def test_estimate_stage():
    e = _engine()
    assert e.estimate_stage(5) == "pre-seed"
    assert e.estimate_stage(12) == "seed"
    assert e.estimate_stage(34) == "series-a-b"
    assert e.estimate_stage(80) == "growth"


def test_change_pct_zero_prior_is_bounded():
    # Prior window of 0 must return a bounded finite value, never inf.
    # Design: "activity started from nothing" == +100% (fractional 1.0).
    import math

    val = se._change_pct(10, 0)
    assert math.isfinite(val)
    assert val == 1.0
    assert se._change_pct(0, 0) == 0.0
