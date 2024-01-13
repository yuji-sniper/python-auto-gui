# Docker
up:
	docker-compose up -d

build:
	docker-compose build

down:
	docker-compose down

prune:
	docker system prune -a --volumes


# コンテナ
app:
	docker-compose exec app /bin/bash

mysql:
	docker-compose exec mysql /bin/bash

migrate:
	docker-compose run --rm app poetry run alembic upgrade head

migrate-rollback:
	docker-compose run --rm app poetry run alembic downgrade -1

poetry-install:
	docker-compose run --rm app poetry install

poetry-init:
	docker-compose run --rm app poetry init -n


# ログ
app-log:
	docker-compose logs -f app


# 初回環境構築
init:
	@make build
	@make poetry-install
