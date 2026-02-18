@echo off
chcp 65001 >nul 2>&1

set "DB_NAME=university_db"
set "DB_USER=postgres"
set "DB_PASSWORD="
set "HOST=localhost"
set "PORT=5432"

set "PSQL_PATH=psql"

echo Проверка существования базы данных "%DB_NAME%"...
%PSQL_PATH% -h %HOST% -p %PORT% -U %DB_USER% -l | findstr /C:"%DB_NAME%" >nul
if %errorlevel% equ 0 (
    echo База данных "%DB_NAME%" уже существует.
) else (
    echo Создание базы данных "%DB_NAME%"...
    %PSQL_PATH% -h %HOST% -p %PORT% -U %DB_USER% -c "CREATE DATABASE \"%DB_NAME%\" ENCODING 'UTF8';"
    if %errorlevel% neq 0 (
        echo Не удалось создать базу данных.
        exit /b 1
    )
    echo База данных "%DB_NAME%" успешно создана.
)

set "SQL_SCRIPT="
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

echo Проверка и создание таблиц...
echo %SQL_SCRIPT% | %PSQL_PATH% -h %HOST% -p %PORT% -U %DB_USER% -d %DB_NAME%
if %errorlevel% neq 0 (
    echo Ошибка при создании таблиц.
    exit /b 1
)
echo Таблицы успешно проверены и созданы (если их не было).

echo Наполнение таблиц данными...

%PSQL_PATH% -h %HOST% -p %PORT% -U %DB_USER% -d %DB_NAME% -c ^
"INSERT INTO Студенты (имя, фамилия, дата_рождения, email) VALUES
('Иван', 'Иванов', '2000-01-15', 'ivan.ivanov@example.com'),
('Мария', 'Петрова', '1999-05-22', 'maria.petrova@example.com'),
('Сергей', 'Сидоров', '2001-03-10', 'sergey.sidorov@example.com'),
('Анна', 'Кузнецова', '2000-07-30', 'anna.kuznetsova@example.com'),
('Дмитрий', 'Морозов', '1998-11-05', 'dmitry.morozov@example.com')
ON CONFLICT (email) DO NOTHING;"

%PSQL_PATH% -h %HOST% -p %PORT% -U %DB_USER% -d %DB_NAME% -c ^
"INSERT INTO Предметы (название, описание) VALUES
('Математика', 'Основы математического анализа и алгебры'),
('Физика', 'Изучение законов природы и физических явлений'),
('Программирование', 'Основы разработки программного обеспечения'),
('История', 'Изучение истории человечества'),
('Литература', 'Анализ литературных произведений')
ON CONFLICT (название) DO NOTHING;"

%PSQL_PATH% -h %HOST% -p %PORT% -U %DB_USER% -d %DB_NAME% -c ^
"INSERT INTO Преподаватели (имя, фамилия, email, должность) VALUES
('Алексей', 'Новиков', 'alexey.novikov@example.com', 'Доцент'),
('Елена', 'Смирнова', 'elena.smirnova@example.com', 'Профессор'),
('Игорь', 'Ковалев', 'igor.kovalev@example.com', 'Ассистент'),
('Ольга', 'Федорова', 'olga.fedorova@example.com', 'Старший преподаватель'),
('Павел', 'Лебедев', 'pavel.lebedev@example.com', 'Доцент')
ON CONFLICT (email) DO NOTHING;"

%PSQL_PATH% -h %HOST% -p %PORT% -U %DB_USER% -d %DB_NAME% -c ^
"INSERT INTO Экзамены (студент_id, предмет_id, преподаватель_id, оценка, дата_экзамена) VALUES
(1, 1, 1, 85, '2024-06-15'),
(2, 2, 2, 90, '2024-06-16'),
(3, 3, 3, 75, '2024-06-17'),
(4, 4, 4, 88, '2024-06-18'),
(5, 5, 5, 92, '2024-06-19')
ON CONFLICT DO NOTHING;"

if %errorlevel% equ 0 (
    echo Данные успешно добавлены во все таблицы (или уже существовали).
) else (
    echo Ошибка при добавлении данных.
)

set DB_PASSWORD=
set PSQL_PATH=
