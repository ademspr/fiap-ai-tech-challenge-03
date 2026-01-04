FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

ENV PATH=/opt/poetry/bin:$PATH
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root

COPY . .
