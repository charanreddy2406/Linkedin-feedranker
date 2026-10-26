import json
import logging

from kafka import KafkaProducer
from kafka.errors import KafkaError

from .config import load_config

log = logging.getLogger("feed-api.producer")
_config = load_config()

_producer = KafkaProducer(
    bootstrap_servers=_config.kafka_bootstrap,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=3,
)


def publish_engagement(event: dict) -> None:
    """Publish synchronously; raise KafkaError if delivery fails."""
    future = _producer.send(_config.engagement_topic, value=event)
    # Block for the broker ack so the route can report success/failure honestly.
    future.get(timeout=5)
    log.info("published event_id=%s type=%s", event["event_id"], event["event_type"])
