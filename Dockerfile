FROM python:3.11-slim as requirements
ENV POETRY_CORE_VERSION=1.6.1 POETRY_VERSION=1.5.1 POETRY_NO_INTERACTION=1
RUN pip install --no-cache-dir poetry-core=="${POETRY_CORE_VERSION}" poetry=="${POETRY_VERSION}"
WORKDIR /
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.11-slim as app
WORKDIR /
COPY --from=requirements /requirements.txt .
RUN  pip install --no-cache-dir -r requirements.txt
RUN groupadd -g 999 unprivileged && useradd -m -r -u 999 -g unprivileged unprivileged
USER unprivileged:unprivileged
WORKDIR /app
COPY --chown=unprivileged:unprivileged fastapi_start fastapi_start

FROM app as web
CMD ["uvicorn", "fastapi_start.main:app", "--host", "0.0.0.0"]

FROM app as alembic
COPY --chown=unprivileged:unprivileged alembic.ini alembic.ini
COPY --chown=unprivileged:unprivileged alembic alembic
CMD ["alembic", "upgrade", "head"]
