install:
	poetry install

test:
	poetry run pytest

up-poetry:
	poetry run uvicorn fastapi_start.main:app --reload

up-docker:
	docker-compose up --build
