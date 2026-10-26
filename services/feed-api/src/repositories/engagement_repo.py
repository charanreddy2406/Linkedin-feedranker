import logging

from ..db import get_conn, get_conn_with_timeout

log = logging.getLogger("feed-api.engagement")

AGG_TIMEOUT_MS = 150


def aggregates_for(post_ids: list[int]) -> dict[int, tuple[int, int]]:
    """Return {post_id: (like_count, comment_count)}; raise on failure/timeout.

    The caller decides the fallback — this function fails loudly so a slow or
    broken aggregate store can't silently degrade the ranking without a trace.
    """
    if not post_ids:
        return {}
    sql = """
        SELECT post_id, like_count, comment_count
        FROM engagement_aggregates
        WHERE post_id = ANY(%s)
    """
    with get_conn_with_timeout(AGG_TIMEOUT_MS) as conn:
        rows = conn.execute(sql, (post_ids,)).fetchall()
    return {r[0]: (r[1], r[2]) for r in rows}


def record_event(event: dict) -> None:
    sql = """
        INSERT INTO engagement_events (event_id, user_id, post_id, event_type, ts)
        VALUES (%(event_id)s, %(user_id)s, %(post_id)s, %(event_type)s, %(ts)s)
        ON CONFLICT (event_id) DO NOTHING
    """
    with get_conn() as conn:
        conn.execute(sql, event)
        conn.commit()
