.PHONY: up down build migrate test seed shell logs clean

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

migrate:
	docker compose exec web python manage.py makemigrations
	docker compose exec web python manage.py migrate

test:
	docker compose exec web pytest

seed:
	docker compose exec web python manage.py seed_data

shell:
	docker compose exec web python manage.py shell

logs:
	docker compose logs -f

clean:
	docker compose down -v
	docker system prune -f