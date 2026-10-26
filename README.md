# LinkedIn | Scalable Social Feed Ranking Service

An intermediate capstone — spec the MVP contracts, stand up a Postgres + Redis + Kafka stack with Docker Compose, build a FastAPI feed service that retrieves candidates from multiple sources, scores them with a deterministic ranking model, caches the ranked feed in Redis, ingests engagement events to Kafka, materializes aggregates with a consumer, wires those signals back into ranking with timeouts and fallbacks, tests the core logic, and packages everything for a single cloud deploy.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- FastAPI
- Postgres
- Redis
- Kafka
- Docker
