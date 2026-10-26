from datetime import datetime, timezone

from ranker.model import Features, age_hours, score


def test_engagement_lifts_score():
    f_low = Features(likes=0, comments=0, age_hours=1.0)
    f_high = Features(likes=100, comments=20, age_hours=1.0)
    assert score(f_high) > score(f_low)


def test_recency_beats_staleness_when_engagement_equal():
    fresh = Features(likes=10, comments=2, age_hours=0.5)
    stale = Features(likes=10, comments=2, age_hours=48.0)
    assert score(fresh) > score(stale)


def test_age_hours_is_never_negative():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    future = datetime(2026, 1, 1, 13, 0, tzinfo=timezone.utc)
    assert age_hours(future, now) == 0.0


def test_score_is_deterministic():
    f = Features(likes=5, comments=3, age_hours=2.0)
    assert score(f) == score(f)
