# Subscription Service

**Subscription Service** — микросервис, отвечающий за управление подписками между пользователями и формирование пользовательской ленты (feed) на основе этих подписок. Он взаимодействует с Auth и Post сервисами через HTTP и кэширует данные для ускорения отклика.

## 🚀 Основные возможности

- Подписка / отписка по `user_id` и `username`
- Получение списка подписок и подписчиков
- Формирование ленты постов от подписок
- Кэширование ленты (например, с Redis)
- Интеграция с Auth и Post Service
- JWT-аутентификация пользователя

## 🧰 Технологии

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Docker / Docker Compose
- Redis (для кэша)
- HTTPX (клиенты для Auth и Post)
- Pytest

## 📁 Структура проекта

```
subscription_service/
├── alembic/                   # Миграции Alembic
├── app/
│   ├── clients/               # HTTP-клиенты для других микросервисов
│   │   ├── auth_client.py
│   │   └── post_client.py
│   ├── core/
│   │   ├── config.py          # Настройки окружения
│   │   └── deps.py            # JWT и Depends
│   ├── database.py            # Подключение к БД
│   ├── models.py              # SQLAlchemy-модели (Subscription)
│   ├── schemas.py             # Pydantic-схемы
│   ├── services/              # Сервисы, логика подписок
│   │   └── subscription_service.py
│   ├── utils/
│   │   └── cache.py           # Кэширование ленты
│   └── routers/
│       └── subscriptions.py   # Роуты подписок
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── main.py                    # Точка входа FastAPI
├── requirements.txt
└── README.md
```

## ▶️ Запуск проекта

```bash
# Клонировать проект
git clone https://github.com/your-org/subscription_service.git
cd subscription_service

# Запуск с помощью Docker Compose
docker-compose up --build
```

После запуска API будет доступен по адресу:  
🔗 `http://localhost:8007`

## 🔐 Авторизация

Для доступа к большинству маршрутов необходим JWT-токен:

```
Authorization: Bearer <ваш_токен>
```

## 📄 Документация

Swagger UI доступен по адресу:
```
http://localhost:8007/docs
```

## 🧪 Тестирование

```bash
pytest
```

Тесты покрывают:
- Подписку / отписку
- Получение фида
- Интеграции с Auth и Post сервисами
- Проверку авторизации

## ⚙️ CI/CD

По push или PR:
- Сборка Docker-образа
- Прогон тестов
- Статическая проверка (линтеры)
- Возможная доставка в staging/production

## 📌 Примечания

- Все ID пользователей получаются из Auth Service
- Посты подгружаются по списку подписок через Post Service
- Кэширование сделано для оптимизации получения фида



# Admin Service

Admin Service — это микросервис, предназначенный для выполнения административных операций в рамках распределённой системы. Он обеспечивает управление пользователями и модерацию контента через REST API, взаимодействуя с другими сервисами (Auth, Post и т.д.).

## 🚀 Основные возможности

- Получение списка пользователей
- Блокировка / разблокировка пользователей
- Изменение ролей (user ↔ admin)
- Удаление постов и комментариев
- Логирование действий администратора (в таблицу и Sentry)
- Проверка прав доступа по JWT
- Интеграция с Auth и Post Service

## 🧰 Технологии

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- Docker / Docker Compose
- PostgreSQL
- REST API
- Pytest

## 📁 Структура проекта

```
admin_service/
├── alembic/                   # Миграции Alembic
├── app/                       # Основная логика сервиса
│   ├── database.py            # Подключение к БД
│   ├── dependencies.py        # Проверка токенов, получение пользователя
│   ├── main.py                # Создание приложения FastAPI
│   ├── models.py              # Модели SQLAlchemy (например, AuditLog)
│   ├── routers/               # Роутеры (users, content, stats)
│   ├── schemas.py             # Pydantic-схемы
│   ├── utils.py               # Логика логирования, Sentry
├── tests/                     # Интеграционные и юнит-тесты
├── alembic.ini                # Конфигурация Alembic
├── app.py                     # Альтернативный запуск сервиса
├── config.py                  # Настройки окружения
├── docker-entrypoint.sh       # Стартовый скрипт Docker-контейнера
├── Dockerfile                 # Инструкция сборки Docker-образа
├── main.py                    # Точка входа FastAPI
├── README.md                  # Документация
└── requirements.txt           # Зависимости
```

## ▶️ Запуск проекта

```bash
# Клонировать проект
git clone https://github.com/your-org/admin_service.git
cd admin_service

# Запуск с помощью Docker Compose
docker-compose up --build
```

После запуска API будет доступен по адресу:  
🔗 `http://localhost:8002`

## 🔐 Авторизация

Все защищённые маршруты требуют передачи JWT-токена администратора:
```
Authorization: Bearer <ваш_токен>
```

Только пользователи с ролью `admin` могут выполнять административные действия.

## 📄 Документация

Swagger UI доступен по адресу:
```
http://localhost:8002/docs
```

## 🧪 Тестирование

```bash
# Запуск тестов
pytest
```

Тесты включают:
- Позитивные и негативные сценарии
- Проверку взаимодействия с Auth и Post сервисами
- Проверку авторизации, валидации и логирования

## ⚙️ CI/CD

При каждом `push` или `pull request` выполняются:
- Сборка Docker-образа
- Прогон тестов через GitHub Actions
- Отчёт об ошибках, если они есть

## 📌 Примечания

- Используются переменные окружения для настройки ссылок на Auth/Post сервисы.
- Логи действий администратора сохраняются в БД и/или отправляются в систему мониторинга (например, Sentry).
 
