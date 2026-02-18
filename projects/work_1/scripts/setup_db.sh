#!/bin/bash

DB_NAME="university_db"
DB_USER="postgres"
DB_PASSWORD="${DB_PASSWORD:-}"
HOST="localhost"
PORT="5432"

export PGPASSWORD="$DB_PASSWORD"

echo "Создание базы данных '$DB_NAME'..."
createdb -h "$HOST" -p "$PORT" -U "$DB_USER" "$DB_NAME"

if [ $? -ne 0 ]; then
    echo "Не удалось создать базу данных. Возможно, она уже существует."
else
    echo "База данных '$DB_NAME' успешно создана."
fi

SQL_SCRIPT="
CREATE TABLE IF NOT EXISTS Студенты (
    id SERIAL PRIMARY KEY,
    имя VARCHAR(100) NOT NULL,
    фамилия VARCHAR(100) NOT NULL,
    дата_рождения DATE,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS Предметы (
    id SERIAL PRIMARY KEY,
    название VARCHAR(100) NOT NULL UNIQUE,
    описание TEXT
);

CREATE TABLE IF NOT EXISTS Преподаватели (
    id SERIAL PRIMARY KEY,
    имя VARCHAR(100) NOT NULL,
    фамилия VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    должность VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Экзамены (
    id SERIAL PRIMARY KEY,
    студент_id INTEGER NOT NULL REFERENCES Студенты(id) ON DELETE CASCADE,
    предмет_id INTEGER NOT NULL REFERENCES Предметы(id) ON DELETE CASCADE,
    преподаватель_id INTEGER NOT NULL REFERENCES Преподаватели(id) ON DELETE CASCADE,
    оценка INTEGER CHECK (оценка >= 0 AND оценка <= 100),
    дата_экзамена DATE NOT NULL
);
"

echo "Создание таблиц..."
psql -h "$HOST" -p "$PORT" -U "$DB_USER" -d "$DB_NAME" -c "$SQL_SCRIPT"

if [ $? -eq 0 ]; then
    echo "Таблицы успешно созданы."
else
    echo "Произошла ошибка при создании таблиц."
fi

unset PGPASSWORD
