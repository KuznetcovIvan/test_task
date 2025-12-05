MANAGE := uv run manage.py
CELERY := uv run -m celery -A config.celery
DC := docker compose

.PHONY: run migrate makemigrations superuser worker test up down restart logs build

run:
	$(MANAGE) runserver 0.0.0.0:8000

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

collectstatic:
	$(MANAGE) collectstatic --noinput

worker:
	$(CELERY) worker -l info

test:
	uv run -m pytest

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) down
	$(DC) up -d

logs:
	$(DC) logs -f

build:
	$(DC) build
