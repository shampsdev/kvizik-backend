FROM python:3.11-alpine AS base

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


FROM base AS dev
CMD [ "uvicorn", "app.app:app", "--host", "0.0.0.0", "--reload" ]


FROM base AS prod
CMD [ "uvicorn", "app.app:app", "--host", "0.0.0.0" ]

