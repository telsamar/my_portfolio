FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    ffmpeg \
    libsm6 \
    libxext6 \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh db:5432 -- python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
