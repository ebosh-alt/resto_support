FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.0.1 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

WORKDIR /app
COPY . /app

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-root

EXPOSE 6379

CMD ["python", "main.py"]
