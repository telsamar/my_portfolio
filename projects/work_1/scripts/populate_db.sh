#!/bin/bash

DB_NAME="university_db"
DB_USER="postgres"
DB_PASSWORD="${DB_PASSWORD:-}"
HOST="localhost"
PORT="5432"

export PGPASSWORD="$DB_PASSWORD"

execute_sql() {
    local sql="$1"
    psql -h "$HOST" -p "$PORT" -U "$DB_USER" -d "$DB_NAME" -c "$sql"
}

echo "Наполнение таблицы Студенты..."
execute_sql "
INSERT INTO Студенты (имя, фамилия, дата_рождения, email) VALUES
('Иван', 'Иванов', '2000-01-15', 'ivan.ivanov@example.com'),
('Мария', 'Петрова', '1999-05-22', 'maria.petrova@example.com'),
('Сергей', 'Сидоров', '2001-03-10', 'sergey.sidorov@example.com'),
('Анна', 'Кузнецова', '2000-07-30', 'anna.kuznetsova@example.com'),
('Дмитрий', 'Морозов', '1998-11-05', 'dmitry.morozov@example.com');
"

echo "Наполнение таблицы Предметы..."
execute_sql "
INSERT INTO Предметы (название, описание) VALUES
('Математика', 'Основы математического анализа и алгебры'),
('Физика', 'Изучение законов природы и физических явлений'),
('Программирование', 'Основы разработки программного обеспечения'),
('История', 'Изучение истории человечества'),
('Литература', 'Анализ литературных произведений');
"

echo "Наполнение таблицы Преподаватели..."
execute_sql "
INSERT INTO Преподаватели (имя, фамилия, email, должность) VALUES
('Алексей', 'Новиков', 'alexey.novikov@example.com', 'Доцент'),
('Елена', 'Смирнова', 'elena.smirnova@example.com', 'Профессор'),
('Игорь', 'Ковалев', 'igor.kovalev@example.com', 'Ассистент'),
('Ольга', 'Федорова', 'olga.fedorova@example.com', 'Старший преподаватель'),
('Павел', 'Лебедев', 'pavel.lebedev@example.com', 'Доцент');
"

echo "Наполнение таблицы Экзамены..."
execute_sql "
INSERT INTO Экзамены (студент_id, предмет_id, преподаватель_id, оценка, дата_экзамена) VALUES
(1, 1, 1, 85, '2024-06-15'),
(2, 2, 2, 90, '2024-06-16'),
(3, 3, 3, 75, '2024-06-17'),
(4, 4, 4, 88, '2024-06-18'),
(5, 5, 5, 92, '2024-06-19');
"

if [ $? -eq 0 ]; then
    echo "Данные успешно добавлены во все таблицы."
else
    echo "Произошла ошибка при добавлении данных."
fi

unset PGPASSWORD
