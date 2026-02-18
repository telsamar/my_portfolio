# Каталог БПЛА

Веб-приложение-каталог беспилотных летательных аппаратов: бэкенд на Node.js и PostgreSQL, API фильтров и списка/карточки дрона, статический фронтенд.

## Стек

- **Бэкенд:** Node.js, Express
- **БД:** PostgreSQL
- **Фронтенд:** статические HTML/CSS/JS в `public/`

## Структура

- `server.js` — сервер: раздача статики, API фильтров и БПЛА
- `public/` — главная страница с фильтрами и списком, карточка товара
- `setup_db.sh` — создание БД, таблицы `uavs` и начальных записей

## Запуск

### 1. База данных

Установите PostgreSQL. Создайте БД и таблицу (логин/пароль по умолчанию `postgres`):

```bash
chmod +x setup_db.sh
./setup_db.sh
```

При необходимости отредактируйте в начале `setup_db.sh`: `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`.

### 2. Зависимости и сервер

```bash
npm install
node server.js
```

Сервер будет доступен по адресу: http://localhost:3000

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/filters` | Списки для фильтров: производители, типы ЛА, области применения |
| GET | `/uavs` | Список БПЛА. Query: `manufacturer`, `aircraft_type`, `application_area` (значения через `\|`) |
| GET | `/uavs/:id` | Один БПЛА по `id` |

## Таблица БД `uavs`

Поля: `id`, `photo_url`, `name`, `description`, `official_website`, `manufacturer`, `aircraft_type`, `weight_category_kg`, `payload`, `communication_range_km`, `max_takeoff_mass_kg`, `max_flight_time_min`, `max_route_length_km`, `max_speed_km_h`, `max_payload_kg`, `cruise_speed_km_h`, `application_areas`.
