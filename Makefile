.PHONY: up down seed demo logs

up:
	docker compose up -d
	@echo "waiting for services to report healthy..."
	@docker compose ps

down:
	docker compose down -v

seed:
	bash scripts/init_db.sh

demo:
	bash scripts/demo_e2e.sh

logs:
	docker compose logs -f
