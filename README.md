## Разработка

Желательно работать в [виртуальном окружении](https://pythonchik.ru/okruzhenie-i-pakety/virtualnoe-okruzhenie-python-venv)


1. Установка пакетов

Установить [poetry](https://python-poetry.org/docs/#installation)

```bash
poetry install
```




2. Запуск

```bash
poetry run fastapi dev
```

3. Docs

Скорее всего будет в http://localhost:8000/docs


## Docker (development)
### Собрать образ для разработки
```bash
docker build . --tag kvizik:dev --target dev
```
### Запустить (Приложение будет перезапускаться при изменении кода)
```bash
docker run \
-p 8080:8000 \
-v $(pwd)/app:/app/app \
--name kvizik-dev \
--rm \
kvizik:dev
```

## Docker (deployment)
```bash
docker compose up --build
```