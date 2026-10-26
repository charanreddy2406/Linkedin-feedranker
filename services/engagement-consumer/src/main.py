import json
import logging
import os

import psycopg
from kafka import KafkaConsumer

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
log = logging.getLogger("engagement-consumer")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://feed:feed@localhost:5432/feed")
KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.environ.get("ENGAGEMENT_TOPIC", "engagement.events")

# event_type -> which counter to increment
COUNTER_FOR = {"like": "like_count", "comment": "comment_count"}


def apply_event(conn: psycopg.Connection, event: dict) -> None:
    column = COUNTER_FOR.get(event["event_type"])
    if column is None:
        return  # follows don't affect post aggregates
    sql = f"""
        INSERT INTO engagement_aggregates (post_id, {column})
        VALUES (%(post_id)s, 1)
        ON CONFLICT (post_id)
        DO UPDATE SET {column} = engagement_aggregates.{column} + 1,
                      updated_at = now()
    """
    conn.execute(sql, {"post_id": event["post_id"]})


def main() -> None:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="engagement-aggregator",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
    )
    log.info("consuming %s ...", TOPIC)
    with psycopg.connect(DATABASE_URL) as conn:
        for msg in consumer:
            event = msg.value
            try:
                apply_event(conn, event)
                conn.commit()
                consumer.commit()  # commit offset only after the DB write succeeds
                log.info("applied %s post=%s", event["event_type"], event["post_id"])
            except Exception:
                conn.rollback()
                log.exception("failed to apply event, will retry on redelivery")


if __name__ == "__main__":
    main()
