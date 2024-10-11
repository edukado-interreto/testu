django := poetry run python manage.py

init:
	poetry install
	$(django) migrate
	$(django) createsuperuser

run:
	@$(django) migrate && gunicorn config.wsgi:application --bind 0.0.0.0:${DJANGO_PORT} --workers 3

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
