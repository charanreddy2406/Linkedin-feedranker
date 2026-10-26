-- Materialized per-post engagement counters the ranker reads at request time.
CREATE TABLE IF NOT EXISTS engagement_aggregates (
    post_id       BIGINT PRIMARY KEY REFERENCES posts(id),
    like_count    INTEGER NOT NULL DEFAULT 0,
    comment_count INTEGER NOT NULL DEFAULT 0,
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Raw event log used for optional durability and dedupe by event_id.
CREATE TABLE IF NOT EXISTS engagement_events (
    event_id   UUID PRIMARY KEY,
    user_id    BIGINT NOT NULL,
    post_id    BIGINT NOT NULL,
    event_type TEXT NOT NULL,
    ts         TIMESTAMPTZ NOT NULL
);
