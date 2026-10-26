from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg_pool import ConnectionPool

from .config import load_config

_config = load_config()
_pool = ConnectionPool(_config.database_url, min_size=1, max_size=10, open=True)


@contextmanager
def get_conn() -> Iterator[psycopg.Connection]:
    with _pool.connection() as conn:
        yield conn


@contextmanager
def get_conn_with_timeout(ms: int) -> Iterator[psycopg.Connection]:
    """A connection whose statements abort after `ms` milliseconds."""
    with _pool.connection() as conn:
        conn.execute("SET LOCAL statement_timeout = %s", (ms,))
        yield conn
