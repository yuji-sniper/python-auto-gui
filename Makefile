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

poetry-install:
	docker-compose run --rm app poetry install --no-root

poetry-init:
	docker-compose run --rm app poetry init -n


# ログ
app-log:
	docker-compose logs -f app


# 初回環境構築
init:
	@make build
	@make poetry-install
