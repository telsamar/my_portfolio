# Университетское приложение

Веб-приложение для учёта студентов, предметов, преподавателей и экзаменов. Бэкенд на Node.js и Express, БД PostgreSQL, загрузка предметов из Excel (.xlsx, .xls).

## Стек

- **Бэкенд:** Node.js, Express
- **БД:** PostgreSQL
- **Фронтенд:** статические HTML/CSS/JS в `public/`
- **Загрузка файлов:** Multer, xlsx

## Структура

- **university_app/** — приложение (сервер + фронт в `public/`).
- **scripts/** — скрипты для создания БД и наполнения данными:
  - `setup_db.sh` / `setup_db.ps1` — создание БД и таблиц
  - `populate_db.sh` — вставка тестовых данных (Bash)
  - `tog.sh` — создание БД, таблиц и наполнение одним скриптом (Bash)
  - `setup.bat` — создание БД, таблиц и наполнение (Windows)
  - `insert_data.ps1` — вставка тестовых данных (PowerShell)

Таблицы: Студенты, Предметы, Преподаватели, Экзамены (связи по id).

## Запуск

### 1. База данных

Установите PostgreSQL. Пароль и пользователь задаются через переменные окружения (см. ниже).

**Linux/macOS (Bash):**
```bash
cd scripts
export DB_PASSWORD='ваш_пароль'
chmod +x setup_db.sh
./setup_db.sh
./populate_db.sh
```
Или одним скриптом: `./tog.sh`

**Windows (PowerShell):**
```powershell
$env:DB_PASSWORD = "ваш_пароль"
.\scripts\setup_db.ps1
.\scripts\insert_data.ps1
```

**Windows (cmd):** в `setup.bat` задайте `set "DB_PASSWORD=ваш_пароль"` и при необходимости путь к `psql` в `PSQL_PATH`, затем запустите `setup.bat`.

### 2. Приложение

```bash
cd university_app
cp ../.env.example .env
# Отредактируйте .env: DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
npm install
node server.js
```

Приложение будет доступно по адресу: http://localhost:3000

Переменные окружения (или файл `.env` в папке с `server.js`): `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `PORT`.

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/students` | Список студентов |
| POST | `/api/students` | Добавить студента (имя, фамилия, дата_рождения, email) |
| DELETE | `/api/students/:id` | Удалить студента |
| GET | `/api/subjects` | Список предметов |
| POST | `/api/subjects/upload` | Загрузить предметы из Excel (multipart, поле `file`) |
| GET | `/api/teachers` | Список преподавателей |
| GET | `/api/exams` | Список экзаменов (с именами студента, предмета, преподавателя) |
| POST | `/api/exams` | Назначить экзамен (студент_id, предмет_id, преподаватель_id, оценка 0–100, дата_экзамена) |

Файл для импорта предметов: два столбца (название, описание), без обязательного заголовка. Максимальный размер файла — 5 MB.
