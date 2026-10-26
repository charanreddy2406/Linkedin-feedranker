# Event contracts

All events are JSON published to Kafka topic **`engagement.events`**.

## EngagementEvent (schema_version 1)

| field          | type     | notes                                  |
|----------------|----------|----------------------------------------|
| schema_version | int      | bump on any breaking field change      |
| event_id       | uuid     | producer-generated; consumers dedupe   |
| user_id        | int      | who acted                              |
| post_id        | int      | the post acted on                      |
| event_type     | enum     | `like` \| `comment` \| `follow`        |
| ts             | ISO-8601 | event time, UTC                        |

## Why version from day one
Adding `schema_version` now means a consumer can branch on the version instead
of guessing. New optional fields are backward-compatible; a breaking change
bumps the version and the consumer keeps reading old events.
