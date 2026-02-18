# Банковский проект (Django)

Веб-приложение на Django: регистрация и авторизация, каталог товаров/услуг, оформление заказов, отзывы. БД MySQL.

## Стек

- **Backend:** Django 5.1
- **БД:** MySQL (mysqlclient)
- **Шаблоны:** Django templates

## Структура

- **bankproject/** — проект Django (настройки, urls)
- **bankproject/accounts/** — приложение: модели User/Profile, Review, CatalogItem, Order; регистрация, логин, каталог, заказы, отзывы
- **bankproject/templates/** — HTML-шаблоны (главная, каталог, контакты, отзывы, форма заказа, регистрация/логин)
- **bankproject/static/** — статика (CSS, изображения)
- **test_dump.sql** — дамп БД для развёртывания
- **Описание.txt** — краткая инструкция по запуску

## Запуск

### 1. База данных

Установите MySQL. Создайте пустую базу (например, `test`) и загрузите дамп:

```bash
mysql -u root -p test < test_dump.sql
```

### 2. Проект

```bash
cd bankproject
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Задайте переменные окружения (или создайте `.env` и подгружайте через python-dotenv):

- `DJANGO_SECRET_KEY` — секретный ключ Django (обязательно)
- `DB_NAME` — имя БД (по умолчанию `test`)
- `DB_USER` — пользователь MySQL (по умолчанию `root`)
- `DB_PASSWORD` — пароль
- при необходимости: `DB_HOST`, `DB_PORT`

### 3. Запуск сервера

```bash
python manage.py runserver
```

Откройте в браузере: http://127.0.0.1:8000/

По умолчанию редирект на страницу входа. Админка: http://127.0.0.1:8000/admin/ (создайте суперпользователя: `python manage.py createsuperuser`).

## Основные страницы

| Путь | Описание |
|------|----------|
| `/accounts/login/` | Вход |
| `/accounts/register/` | Регистрация (логин, email, ФИО, телефон, согласие на обработку данных) |
| `/home/` | Главная (после входа) |
| `/catalog/` | Каталог товаров/услуг |
| `/catalog/order/<id>/` | Оформление заказа (ФИО, телефон, email, адрес, способ оплаты) |
| `/contacts/` | Контакты |
| `/reviews/` | Отзывы (добавление и просмотр) |

Модели: профиль пользователя (ФИО, телефон, согласие), отзывы, позиции каталога, заказы.
