import logging
import uuid
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from kafka.errors import KafkaError
from pydantic import BaseModel, Field

from ..kafka_producer import publish_engagement

log = logging.getLogger("feed-api.events")
router = APIRouter()


class EngagementIn(BaseModel):
    user_id: int
    post_id: int
    event_type: Literal["like", "comment", "follow"]


@router.post("/events/engagement")
def ingest(body: EngagementIn):
    event = {
        "schema_version": 1,
        "event_id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "post_id": body.post_id,
        "event_type": body.event_type,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    try:
        publish_engagement(event)
    except KafkaError as exc:
        log.error("kafka publish failed: %s", exc)
        return JSONResponse(status_code=503, content={"error": "event bus unavailable"})
    return JSONResponse(status_code=202, content={"accepted": event["event_id"]})
