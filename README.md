## Разработка

Желательно работать в [виртуальном окружении](https://pythonchik.ru/okruzhenie-i-pakety/virtualnoe-okruzhenie-python-venv)


1. Установка пакетов

`
pip install -r requirements.txt
`

2. Запуск

`
fastapi dev
`

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
docker-compose up --build
```