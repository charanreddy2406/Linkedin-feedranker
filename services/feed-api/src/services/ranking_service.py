import logging
from datetime import datetime, timezone

from ranker.model import Features, age_hours, score

from ..repositories.engagement_repo import aggregates_for
from ..repositories.posts_repo import Candidate

log = logging.getLogger("feed-api.ranking")


def _load_aggregates(post_ids: list[int]) -> tuple[dict[int, tuple[int, int]], str]:
    """Return (aggregates, path). On any failure, fall back to empty aggregates."""
    try:
        return aggregates_for(post_ids), "full"
    except Exception as exc:
        log.warning("aggregate read failed, ranking by recency only: %s", exc)
        return {}, "recency_fallback"


def rank(candidates: list[Candidate], now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    post_ids = [c["post_id"] for c in candidates]
    aggs, path = _load_aggregates(post_ids)
    log.info("ranking path=%s candidates=%s", path, len(candidates))

    scored: list[dict] = []
    for c in candidates:
        likes, comments = aggs.get(c["post_id"], (0, 0))
        created = datetime.fromisoformat(c["created_at"])
        feats = Features(
            likes=likes, comments=comments, age_hours=age_hours(created, now)
        )
        scored.append(
            {
                "post_id": c["post_id"],
                "author_id": c["author_id"],
                "text": c["text"],
                "score": round(score(feats), 4),
            }
        )

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored
