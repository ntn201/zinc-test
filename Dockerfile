
FROM python:3.12.3-slim-bullseye AS builder

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.1.3 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml /app/
RUN poetry install


FROM python:3.12.3-slim-bullseye AS app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /app
EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
