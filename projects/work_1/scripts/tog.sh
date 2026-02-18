#!/bin/bash

DB_NAME="university_db"
DB_USER="postgres"
DB_PASSWORD="${DB_PASSWORD:-}"
HOST="localhost"
PORT="5432"

export PGPASSWORD="$DB_PASSWORD"

echo "Проверка существования базы данных '$DB_NAME'..."
DB_EXISTS=$(psql -h "$HOST" -p "$PORT" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -w "$DB_NAME" | wc -l)

if [ "$DB_EXISTS" -eq 0 ]; then
    echo "База данных '$DB_NAME' не существует. Создаем..."
    createdb -h "$HOST" -p "$PORT" -U "$DB_USER" "$DB_NAME"

    if [ $? -ne 0 ]; then
        echo "Не удалось создать базу данных."
        exit 1
    fi
    echo "База данных '$DB_NAME' успешно создана."
else
    echo "База данных '$DB_NAME' уже существует."
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

echo "Проверка и создание таблиц..."
psql -h "$HOST" -p "$PORT" -U "$DB_USER" -d "$DB_NAME" -c "$SQL_SCRIPT"

if [ $? -eq 0 ]; then
    echo "Таблицы успешно проверены и созданы (если их не было)."
else
    echo "Произошла ошибка при создании таблиц."
    exit 1
fi

execute_sql() {
    local sql="$1"
    psql -h "$HOST" -p "$PORT" -U "$DB_USER" -d "$DB_NAME" -c "$sql"
}

echo "Наполнение таблиц данными..."

echo "Наполнение таблицы Студенты..."
execute_sql "
INSERT INTO Студенты (имя, фамилия, дата_рождения, email) VALUES
('Иван', 'Иванов', '2000-01-15', 'ivan.ivanov@example.com'),
('Мария', 'Петрова', '1999-05-22', 'maria.petrova@example.com'),
('Сергей', 'Сидоров', '2001-03-10', 'sergey.sidorov@example.com'),
('Анна', 'Кузнецова', '2000-07-30', 'anna.kuznetsova@example.com'),
('Дмитрий', 'Морозов', '1998-11-05', 'dmitry.morozov@example.com')
ON CONFLICT (email) DO NOTHING;
"

echo "Наполнение таблицы Предметы..."
execute_sql "
INSERT INTO Предметы (название, описание) VALUES
('Математика', 'Основы математического анализа и алгебры'),
('Физика', 'Изучение законов природы и физических явлений'),
('Программирование', 'Основы разработки программного обеспечения'),
('История', 'Изучение истории человечества'),
('Литература', 'Анализ литературных произведений')
ON CONFLICT (название) DO NOTHING;
"

echo "Наполнение таблицы Преподаватели..."
execute_sql "
INSERT INTO Преподаватели (имя, фамилия, email, должность) VALUES
('Алексей', 'Новиков', 'alexey.novikov@example.com', 'Доцент'),
('Елена', 'Смирнова', 'elena.smirnova@example.com', 'Профессор'),
('Игорь', 'Ковалев', 'igor.kovalev@example.com', 'Ассистент'),
('Ольга', 'Федорова', 'olga.fedorova@example.com', 'Старший преподаватель'),
('Павел', 'Лебедев', 'pavel.lebedev@example.com', 'Доцент')
ON CONFLICT (email) DO NOTHING;
"

echo "Наполнение таблицы Экзамены..."
execute_sql "
INSERT INTO Экзамены (студент_id, предмет_id, преподаватель_id, оценка, дата_экзамена) VALUES
(1, 1, 1, 85, '2024-06-15'),
(2, 2, 2, 90, '2024-06-16'),
(3, 3, 3, 75, '2024-06-17'),
(4, 4, 4, 88, '2024-06-18'),
(5, 5, 5, 92, '2024-06-19')
ON CONFLICT DO NOTHING;
"

if [ $? -eq 0 ]; then
    echo "Данные успешно добавлены во все таблицы (или уже существовали)."
else
    echo "Произошла ошибка при добавлении данных."
fi

unset PGPASSWORD
