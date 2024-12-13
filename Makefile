django := docker compose exec django

all: run

run:
	docker compose up --build

migrate:
	$(django) make migrate

migrations:
	$(django) make migrations
	isort backend/apps
	black backend/apps

test:
	$(django) poetry run pytest -Wi --reuse-db --cov-report=xml --cov-report=term:skip-covered --cov=apps

superuser:
	$(django) make superuser

urls:
	$(django) make urls

shell:
	$(django) make shell

pdb-shell:
	docker attach testu-django-1

vue:
	docker compose run --rm vue yarn build
