#!/bin/bash

cd "$(dirname "$0")"

mkdir -p ./videos

echo "Инициализация базы данных..."
python -m app.init_db

echo "Запуск FastAPI приложения..."
uvicorn app.main:app --reload &
APP_PID=$!

echo "Запуск воркера..."
python -m app.worker &
WORKER_PID=$!

wait $APP_PID $WORKER_PID
