install:
	poetry install

test:
	poetry run pytest

alembic-upgrade-poetry:
	poetry run alembic upgrade head

alembic-autogenerate-poetry: alembic-upgrade-poetry
	poetry run alembic revision --autogenerate

up-poetry: alembic-upgrade-poetry
	poetry run uvicorn fastapi_start.main:app --reload

up-docker:
	docker-compose up --build

coverage:
	poetry run pytest --cov=fastapi_start --cov-report html --cov-report term tests/
