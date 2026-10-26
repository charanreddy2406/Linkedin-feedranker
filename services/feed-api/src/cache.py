import json
import logging

import redis

from .config import load_config

log = logging.getLogger("feed-api.cache")
_config = load_config()
_client = redis.from_url(_config.redis_url, decode_responses=True)

CACHE_VERSION = "v1"
TTL_SECONDS = 60


def feed_key(user_id: int, limit: int) -> str:
    return f"feed:{CACHE_VERSION}:user:{user_id}:limit:{limit}"


def get_feed(user_id: int, limit: int) -> list[dict] | None:
    try:
        raw = _client.get(feed_key(user_id, limit))
        return json.loads(raw) if raw else None
    except redis.RedisError as exc:
        log.warning("cache get failed, serving from source: %s", exc)
        return None


def set_feed(user_id: int, limit: int, items: list[dict]) -> None:
    try:
        _client.setex(feed_key(user_id, limit), TTL_SECONDS, json.dumps(items))
    except redis.RedisError as exc:
        log.warning("cache set failed, ignoring: %s", exc)
