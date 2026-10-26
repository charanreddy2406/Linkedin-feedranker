from typing import TypedDict

from ..db import get_conn


class Candidate(TypedDict):
    post_id: int
    author_id: int
    text: str
    created_at: str


def followed_posts(user_id: int, limit: int) -> list[Candidate]:
    """Recent posts authored by people the user follows."""
    sql = """
        SELECT p.id, p.author_id, p.text, p.created_at
        FROM posts p
        JOIN follows f ON f.followee_id = p.author_id
        WHERE f.follower_id = %s
        ORDER BY p.created_at DESC
        LIMIT %s
    """
    return _run(sql, (user_id, limit))


def global_recent(limit: int) -> list[Candidate]:
    """Recent posts across the whole platform."""
    sql = """
        SELECT p.id, p.author_id, p.text, p.created_at
        FROM posts p
        ORDER BY p.created_at DESC
        LIMIT %s
    """
    return _run(sql, (limit,))


def _run(sql: str, params: tuple) -> list[Candidate]:
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [
        Candidate(
            post_id=r[0], author_id=r[1], text=r[2], created_at=r[3].isoformat()
        )
        for r in rows
    ]
