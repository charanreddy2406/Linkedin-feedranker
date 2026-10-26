import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    database_url: str
    redis_url: str
    kafka_bootstrap: str
    engagement_topic: str
    candidate_limit: int
    log_level: str


def load_config() -> Config:
    return Config(
        database_url=os.environ.get(
            "DATABASE_URL", "postgresql://feed:feed@localhost:5432/feed"
        ),
        redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        kafka_bootstrap=os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092"),
        engagement_topic=os.environ.get("ENGAGEMENT_TOPIC", "engagement.events"),
        candidate_limit=int(os.environ.get("FEED_CANDIDATE_LIMIT", "100")),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
