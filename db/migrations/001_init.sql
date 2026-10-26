CREATE TABLE IF NOT EXISTS users (
    id   BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id         BIGSERIAL PRIMARY KEY,
    author_id  BIGINT NOT NULL REFERENCES users(id),
    text       TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS follows (
    follower_id BIGINT NOT NULL REFERENCES users(id),
    followee_id BIGINT NOT NULL REFERENCES users(id),
    PRIMARY KEY (follower_id, followee_id)
);

-- Feed candidate queries fetch a user's followees' recent posts, and recent
-- global posts. Index for both access patterns.
CREATE INDEX IF NOT EXISTS idx_posts_author_created
    ON posts (author_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_posts_created
    ON posts (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_follows_follower
    ON follows (follower_id);
