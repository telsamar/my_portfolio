import pika
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Video
import os
import cv2
import json
import logging
import traceback
import yt_dlp
import time
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'download_you')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '111')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'video_download_queue')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("worker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def download_video(url):
    """
    Скачивает видео с YouTube по заданному URL.

    :param url: URL видео на YouTube.
    :return: Путь к скачанному файлу.
    """
    try:
        if not os.path.exists('./videos'):
            os.makedirs('./videos')

        ydl_opts = {
            'outtmpl': './videos/%(id)s.%(ext)s',
            'format': 'best',
            'noplaylist': True,
            'ignoreerrors': False,
            'retries': 3,
            'quiet': True,
            'no_warnings': True,
            'logger': logger,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if info_dict is None:
                raise Exception("Не удалось извлечь информацию о видео.")
            file_path = ydl.prepare_filename(info_dict)
        logger.info(f"Видео скачано по пути: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Ошибка при скачивании видео {url}: {e}")
        logger.error(traceback.format_exc())
        raise


def detect_faces_in_video(video_path, frame_interval=30):
    """
    Обнаруживает все лица в видео и сохраняет их координаты.
    """
    try:
        logger.info(f"Начало анализа видео: {video_path}")

        if not os.path.exists(video_path):
            logger.error(f"Видео не найдено: {video_path}")
            return 0, []

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            logger.error(f"Не удалось открыть видеофайл: {video_path}")
            return 0, []

        total_faces_detected = 0
        faces_info = []
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                logger.info(
                    f"Конец видео. Проанализировано {frame_count} кадров.")
                break

            frame_count += 1
            if frame_count % frame_interval != 0:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            logger.info(
                f"Кадр {frame_count}: обнаружено {len(detected_faces)} лиц.")
            for (x, y, w, h) in detected_faces:
                faces_info.append({
                    'bounding_box': {
                        'x': int(x),
                        'y': int(y),
                        'width': int(w),
                        'height': int(h)
                    }
                })
                total_faces_detected += 1

        cap.release()
        logger.info(
            f"Обнаружено лиц в видео {video_path}: {total_faces_detected}")
        return total_faces_detected, faces_info

    except Exception as e:
        logger.error(f"Ошибка при анализе видео {video_path}: {e}")
        logger.error(traceback.format_exc())
        raise


def callback(ch, method, properties, body):
    logger.info(f"Получено сообщение из очереди: {body.decode()}")
    """
    Обработчик сообщений из очереди RabbitMQ.
    """
    url = body.decode()
    logger.info(f"Получен URL: {url}")
    session = Session()
    video = None
    try:
        video = session.query(Video).filter_by(url=url).first()
        if not video:
            logger.error(f"Видео с URL {url} не найдено в базе данных.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if video.status == 'Завершено':
            logger.info("Обработка видео уже завершена.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        video.status = 'Скачивается'
        session.commit()

        file_path = download_video(url)
        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не существует после скачивания.")
            video.status = 'Ошибка'
            session.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        video.status = 'Обрабатывается'
        session.commit()

        total_faces_detected, faces_info = detect_faces_in_video(file_path)

        video.status = 'Завершено'
        video.faces_detected = total_faces_detected
        video.faces = faces_info
        session.commit()

        logger.info(
            f"Видео '{url}' обработано. Найдено лиц: {total_faces_detected}.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Не удалось обработать видео {url}: {e}")
        logger.error(traceback.format_exc())
        if video:
            video.status = 'Ошибка'
            session.commit()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    finally:
        session.close()


def main():
    """
    Основная функция воркера, устанавливающая соединение с RabbitMQ и начинающая потребление сообщений.
    """
    while True:
        try:
            logger.info("Подключение к RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST))
            logger.info("Соединение установлено с RabbitMQ.")

            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
            logger.info(f"Очередь {RABBITMQ_QUEUE} создана/существует.")

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=RABBITMQ_QUEUE,
                                on_message_callback=callback)
            logger.info("Начало потребления сообщений из очереди.")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(
                f"Ошибка подключения к RabbitMQ: {e}. Повтор через 5 секунд.")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Необработанная ошибка: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main()
