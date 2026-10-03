.PHONY: up build down logs shell clean \
        test test-logs test-down test-clean

# ========================================
# Приложение (docker-compose.yml)
# ========================================

up:
	docker compose up

build:
	docker compose up --build

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f fastapi_app

shell:
	docker compose exec fastapi_app bash

clean:
	docker compose down -v --remove-orphans

# ========================================
# Тесты (docker-compose.test.yml)
# ========================================

test:
	docker compose -f docker-compose.test.yml up --build -d --remove-orphans
	docker compose -f docker-compose.test.yml exec -T test_app pytest --maxfail=5 -v
	docker compose -f docker-compose.test.yml down --remove-orphans

test-logs:
	docker compose -f docker-compose.test.yml logs -f test_app

test-down:
	docker compose -f docker-compose.test.yml down --remove-orphans

test-clean:
	docker compose -f docker-compose.test.yml down -v --remove-orphans