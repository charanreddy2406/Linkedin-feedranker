from fastapi import APIRouter, Response

from ..services.feed_service import build_feed

router = APIRouter()


@router.get("/feed")
def feed(user_id: int, response: Response, limit: int = 20):
    items, cache_hit = build_feed(user_id, limit)
    response.headers["x-cache"] = "HIT" if cache_hit else "MISS"
    return {"user_id": user_id, "items": items, "limit": limit}
