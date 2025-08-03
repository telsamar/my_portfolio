from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False) 
    status = Column(String, default='В очереди', nullable=False)  # Статусы: В очереди, Скачивается, Обрабатывается, Завершено, Ошибка
    faces_detected = Column(Integer, default=0, nullable=False)
    faces = Column(JSON, nullable=True)  # Список координат обнаруженных лиц
    error_message = Column(String, nullable=True)  # Сообщение об ошибке, если есть
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
