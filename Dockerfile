FROM python:3.11-alpine AS base

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

WORKDIR /app

RUN pip install poetry

COPY ./pyproject.toml .

RUN poetry install

COPY . .


FROM base AS dev
CMD ["poetry", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]


FROM base AS prod
CMD ["poetry", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000" ]
