FROM python:3.9-buster

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false

# Install poetry and python deps
COPY ./poetry.lock ./pyproject.toml /app/
RUN curl -sSL https://install.python-poetry.org | python3 - && /root/.local/bin/poetry install
ENV PATH "/root/.local/bin:$PATH"