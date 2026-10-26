from .candidate_service import gather_candidates
from .ranking_service import rank
from ..cache import get_feed, set_feed


def build_feed(user_id: int, limit: int) -> tuple[list[dict], bool]:
    """Return (items, cache_hit). Cache-aside: try cache, else compute + store."""
    cached = get_feed(user_id, limit)
    if cached is not None:
        return cached, True

    candidates = gather_candidates(user_id)
    ranked = rank(candidates)
    items = ranked[:limit]
    set_feed(user_id, limit, items)
    return items, False
