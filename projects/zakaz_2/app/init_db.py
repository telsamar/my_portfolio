import psycopg2
from sqlalchemy import create_engine
from .models import Base
import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'download_you')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '111')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')

def create_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (DB_NAME,))
        exists = cursor.fetchone()
        if not exists:
            print(f"База данных {DB_NAME} не существует. Создаём...")
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
        else:
            print(f"База данных {DB_NAME} уже существует.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        exit(1)

def create_tables():
    try:
        DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        engine = create_engine(DATABASE_URL)

        Base.metadata.create_all(engine)
        print("Таблицы созданы успешно.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        exit(1)

if __name__ == '__main__':
    create_database()
    create_tables()
    print("Инициализация базы данных завершена успешно.")
