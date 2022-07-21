django := poetry run python manage.py

init:
	poetry install
	$(django) migrate
	$(django) createsuperuser

run:
	@$(django) runserver 0.0.0.0:${DJANGO_PORT}

shell:
	@$(django) shell_plus

migrate:
	@$(django) migrate

migrations:
	@$(django) makemigrations

superuser:
	@$(django) createsuperuser

urls:
	@$(django) show_urls
