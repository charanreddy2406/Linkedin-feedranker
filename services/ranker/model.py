"""Pure ranking model. No I/O, no service imports — just math.

Keeping this module dependency-free is what makes ranking deterministic and
unit-testable: same inputs always produce the same score.
"""
import math
from dataclasses import dataclass
from datetime import datetime, timezone

# Tunable weights for the linear scoring function.
W_LIKES = 1.0
W_COMMENTS = 1.5
W_AGE = 0.8


@dataclass(frozen=True)
class Features:
    likes: int
    comments: int
    age_hours: float


def age_hours(created_at: datetime, now: datetime) -> float:
    delta = now.astimezone(timezone.utc) - created_at.astimezone(timezone.utc)
    return max(delta.total_seconds() / 3600.0, 0.0)


def score(f: Features) -> float:
    """Higher is better. Engagement lifts, age decays."""
    return (
        W_LIKES * math.log1p(f.likes)
        + W_COMMENTS * math.log1p(f.comments)
        - W_AGE * f.age_hours
    )
