# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    ffmpeg \
    libsm6 \
    libxext6 \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Указываем порт для FastAPI
EXPOSE 8000

# Добавляем сценарий запуска
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Запуск FastAPI-приложения с ожиданием доступности базы данных
CMD ["sh", "-c", "./wait-for-it.sh db:5432 -- python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
