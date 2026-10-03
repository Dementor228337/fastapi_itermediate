FROM python:3.14-slim

RUN pip install poetry==2.5.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY src ./src