# Анализ лиц в YouTube-видео

Сервис для добавления YouTube-видео в очередь, скачивания, детекции лиц (OpenCV) и сохранения результатов в БД. Бэкенд на FastAPI, воркер потребляет задачи из RabbitMQ, данные хранятся в PostgreSQL.

## Стек

- **API:** FastAPI, uvicorn
- **БД:** PostgreSQL, SQLAlchemy
- **Очередь:** RabbitMQ (pika)
- **Обработка:** yt-dlp (скачивание), OpenCV (детекция лиц)
- **Запуск:** Docker Compose

## Структура

- `app/main.py` — FastAPI: эндпоинты добавления видео, списка и информации по URL
- `app/worker.py` — воркер: потребление очереди, скачивание видео, детекция лиц, обновление статуса в БД
- `app/models.py` — модель SQLAlchemy `Video`
- `app/init_db.py` — создание БД и таблиц при старте
- `docker-compose.yml` — сервисы app, worker, db, rabbitmq
- `Dockerfile` — образ для приложения и воркера
- `run_app.sh` — локальный запуск без Docker (БД и RabbitMQ должны быть подняты отдельно)

## Запуск (Docker Compose)

```bash
docker compose up --build
```

- API: http://localhost:8001 (порт 8001 → 8000 в контейнере)
- RabbitMQ Management: http://localhost:15673 (логин/пароль guest/guest)
- PostgreSQL: порт 5433 (внутри сети — 5432)

Переменные окружения заданы в `docker-compose.yml` (DB_*, RABBITMQ_*). При необходимости их можно вынести в `.env`.

## API

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/videos/add` | Добавить видео в очередь. Body: `{"url": "https://www.youtube.com/watch?v=..."}`. URL должен быть YouTube. |
| GET | `/videos` | Список всех видео (id, url, status, faces_detected, created_at). |
| GET | `/videos/by_url?url=...` | Информация о видео по URL (включая faces — координаты лиц). |

Статусы записи: «В очереди», «Скачивается», «Обрабатывается», «Завершено», «Ошибка».

## Локальный запуск (без Docker)

1. Поднять PostgreSQL и RabbitMQ с теми же параметрами (БД `download_you`, пользователь `postgres`, пароль `111`, очередь `video_download_queue`).
2. Создать `.env` при необходимости (DB_HOST=localhost, RABBITMQ_HOST=localhost и т.д.).
3. Выполнить:

```bash
pip install -r requirements.txt
./run_app.sh
```

Либо по отдельности: `python -m app.init_db`, затем `uvicorn app.main:app --reload` и в другом терминале `python -m app.worker`.

## Примеры запросов

Добавить видео:

```bash
curl -X POST "http://127.0.0.1:8001/videos/add" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=HaNaKPAQpa0"}'
```

Список видео:

```bash
curl -X GET "http://127.0.0.1:8001/videos"
```

Информация по URL:

```bash
curl -X GET "http://127.0.0.1:8001/videos/by_url?url=https://www.youtube.com/watch?v=HaNaKPAQpa0"
```
