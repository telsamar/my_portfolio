from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from urllib.parse import urlparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Video
import pika
import json
import os

from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'download_you')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '111')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')

app = FastAPI()

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'video_download_queue')

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            connection_attempts=5,
            retry_delay=2
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
except pika.exceptions.AMQPConnectionError as e:
    print(f"Не удалось подключиться к RabbitMQ: {e}")
    exit(1)

class VideoURL(BaseModel):
    url: str

    @validator('url')
    def validate_url(cls, v):
        parsed = urlparse(v)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError('Invalid URL')
        if 'youtube.com/watch' not in v and 'youtu.be/' not in v:
            raise ValueError('URL должно быть ссылкой на YouTube видео')
        return v

@app.post("/videos/add")
def add_video(video: VideoURL):
    """
    Добавляет видео в очередь для обработки.
    """
    session = SessionLocal()
    try:
        # Проверяем, существует ли уже запись с этим URL
        existing_video = session.query(Video).filter_by(url=video.url).first()
        if existing_video:
            if existing_video.status != 'Завершено':
                raise HTTPException(status_code=400, detail="Видео уже добавлено и обрабатывается.")
            else:
                raise HTTPException(status_code=400, detail="Видео уже обработано.")
        
        # Создаём новую запись в базе данных
        new_video = Video(url=video.url, status='В очереди')
        session.add(new_video)
        session.commit()
        session.refresh(new_video)
        
        # Отправляем сообщение в очередь
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=video.url, 
            properties=pika.BasicProperties(
                delivery_mode=2,  
            ))
        
        return {"message": "Видео добавлено в очередь для обработки."}
    except HTTPException as he:
        raise he
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")
    finally:
        session.close()

@app.get("/videos")
def list_videos():
    """
    Получает список всех анализируемых видео.
    """
    session = SessionLocal()
    try:
        videos = session.query(Video).all()
        return [
            {
                "id": video.id,
                "url": video.url,
                "status": video.status,
                "faces_detected": video.faces_detected,
                "created_at": video.created_at
            }
            for video in videos
        ]
    finally:
        session.close()

@app.get("/videos/by_url")
def get_video_info_by_url(url: str):
    """
    Получает информацию о конкретном видео по его URL.
    """
    session = SessionLocal()
    try:
        video = session.query(Video).filter_by(url=url).first()
        if not video:
            raise HTTPException(status_code=404, detail="Видео не найдено.")
        
        return {
            "id": video.id,
            "url": video.url,
            "status": video.status,
            "faces_detected": video.faces_detected,
            "faces": video.faces,
            "created_at": video.created_at,
            "error_message": video.error_message
        }
    finally:
        session.close()
