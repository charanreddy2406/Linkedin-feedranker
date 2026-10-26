from ..config import load_config
from ..repositories.posts_repo import Candidate, followed_posts, global_recent

_config = load_config()


def gather_candidates(user_id: int) -> list[Candidate]:
    """Compose candidates from multiple sources, then dedupe by post_id."""
    limit = _config.candidate_limit
    sources = [
        followed_posts(user_id, limit),
        global_recent(limit),
    ]

    seen: set[int] = set()
    merged: list[Candidate] = []
    for source in sources:
        for cand in source:
            if cand["post_id"] in seen:
                continue
            seen.add(cand["post_id"])
            merged.append(cand)
    return merged
