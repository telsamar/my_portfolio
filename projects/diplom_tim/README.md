# Сравнение способов выполнения HTTP-запросов (диплом)

Проект для сравнения производительности четырёх подходов к выполнению множественных HTTP-запросов в Python: синхронный, asyncio, threading, multiprocessing. Используется публичный API списка университетов (Hipo Labs). Для каждого подхода собираются метрики: время выполнения, загрузка CPU, использование памяти, число успешных/неудачных запросов; результаты сохраняются в JSON.

## Стек

- **Python 3**
- **requests** — синхронные и многопоточные запросы
- **aiohttp** — асинхронные запросы
- **psutil** — метрики CPU и памяти
- **concurrent.futures** — ThreadPoolExecutor
- **multiprocessing** — Pool, Manager

## Структура

- **app/sync_implementation.py** — последовательные запросы (один за другим)
- **app/asyncio_implementation.py** — асинхронные запросы (asyncio + aiohttp), ограничение по одновременным запросам
- **app/threading_implementation.py** — многопоточные запросы (ThreadPoolExecutor), повторные попытки при ошибке
- **app/multiprocessing_implementation.py** — многопроцессные запросы (Pool), повторные попытки и итеративные перезапуски неудачных
- **app/*_results.json** — файлы с результатами тестов (создаются при запуске)

API: `http://universities.hipolabs.com/search?country=Russian+Federation`. По умолчанию каждый скрипт делает 100 запросов.

## Запуск

```bash
cd diplom_tim
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Запуск каждого варианта из корня репозитория (чтобы пути к `app/*_results.json` совпадали):

```bash
python app/sync_implementation.py
python app/asyncio_implementation.py
python app/threading_implementation.py
python app/multiprocessing_implementation.py
```

Или из каталога `diplom_tim`:

```bash
python -m app.sync_implementation
python -m app.asyncio_implementation
python -m app.threading_implementation
python -m app.multiprocessing_implementation
```

В конце каждого запуска в консоль выводится сводка метрик, а результат записывается в соответствующий JSON в `app/`.

## Метрики в результатах

- `total_requests` — число запросов
- `successful_requests` / `failed_requests` — успешные и неудачные
- `total_elapsed_time` — общее время (с)
- `average_time_per_request` — среднее время на один запрос (с)
- `cpu_usage_percent` — процент использования CPU
- `memory_usage_mb` — прирост использования памяти (МБ)
