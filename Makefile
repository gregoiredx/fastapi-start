install:
	poetry install

test:
	poetry run pytest

up-poetry:
	poetry run uvicorn fastapi_start.main:app --reload

up-docker:
	docker-compose up --build

alembic-upgrade:
	poetry run alembic upgrade head

alembic-autogenerate: alembic-upgrade
	poetry run alembic revision --autogenerate

coverage:
	poetry run pytest --cov=fastapi_start --cov-report html --cov-report term tests/
