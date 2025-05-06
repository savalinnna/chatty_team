# Структура проекта

```
Chatty5/
├── auth_service/           # Сервис авторизации
├── admin_service/          # Админ-сервис
├── post_service/           # Управление постами
├── subscription_service/   # Подписки
├── tests/                  # Тесты (e2e, интеграционные)
├── docker-compose.yml      # Docker Compose для объединённого запуска
├── nginx.conf              # Конфиг nginx
├── .env, .env.test         # Переменные окружения
└── workflows/              # GitHub Actions
```

## Описание сервисов

### auth\_service

* Отвечает за регистрацию, вход, JWT и управление пользователями.
* `routers/auth.py`, `routers/users.py`, `utils/security.py`
* Alembic для миграций БД.

### admin\_service

* Обработка активности, логирование, статистика.
* `routers/activity.py`, `logs.py`, `stats.py`, `users.py`
* Набор тестов (юнит и интеграционные).

### post\_service

* Создание, обновление и удаление постов.
* `crud.py`, `routers/posts.py`, `uploads/`

### subscription\_service

* Обработка подписок.
* `clients/` общается с auth и post сервисами.
* `services/subscription_service.py`, `routers/subscriptions.py`, `utils/cache.py`

## Тестирование

* Полный набор `pytest`-test:

  * для каждого сервиса.
  * `tests/test_full_flow.py` — e2e.
  * `tests/test_integration.py`, `conftest.py` для конфигурации.

## DevOps и инфраструктура

* `docker-compose.yml` запускает все сервисы с nginx.
* `nginx.conf` проксирует запросы.
* `workflows/admin_service_tests.yml` — CI для GitHub Actions.

---

Пошаговая инструкция создания проекта:

1 Инициализация репозитория

Создайте папку Chatty5/ и инициализируйте git-репозиторий.

Настройте .gitignore для Python, Docker, IDE и т.д.

2 Создание Docker-инфраструктуры

Напишите docker-compose.yml, описывающий сервисы, БД и nginx.

Добавьте nginx.conf с маршрутизацией запросов к сервисам.

3 Создание auth_service

Настройте FastAPI-приложение.

Реализуйте регистрацию, логин, JWT-токены и эндпоинты управления пользователями.

Добавьте Alembic и напишите миграции.

4 Создание post_service

Реализуйте CRUD-подход для постов.

Добавьте модели, схемы, роутеры и загрузку файлов (uploads).

5 Создание subscription_service

Добавьте подписки на пользователей.

Реализуйте API для подписки/отписки, получения списка подписок.

Настройте обращения к другим сервисам через HTTP (клиенты).

6 Создание admin_service

Реализуйте сбор и отображение пользовательской активности.

Добавьте простую статистику и логирование действий.

Настройка переменных окружения

7 Создайте .env файлы для dev и test окружений.

Убедитесь, что все сервисы используют переменные из них.

8 Настройка тестирования

Используйте pytest.

Напишите юнит и интеграционные тесты для каждого сервиса.

Добавьте e2e тест test_full_flow.py.

9 Интеграция CI/CD

Настройте GitHub Actions (.github/workflows/...) для автоматической проверки коммитов.

10 Запуск проекта

Запустите docker-compose up --build.

Убедитесь, что все сервисы работают корректно через nginx.

11 Мониторинг и отладка

Используйте логи (docker logs) и localhost:{порт} для проверки работы каждого сервиса.


# Auth Service

Auth Service — это микросервис, отвечающий за аутентификацию, авторизацию и управление пользователями в проекте Chatty.

## 🔐 Основной функционал

- Регистрация и вход пользователя
- Подтверждение email
- Восстановление пароля
- Генерация и проверка JWT-токенов
- Получение информации о текущем пользователе
- Проверка ролей (user/admin)

## 🧰 Технологии

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic 2.x
- Docker, Docker Compose
- JWT (JSON Web Tokens)

## 📁 Структура проекта

```
auth_service/
├── alembic/                # миграции Alembic
├── routers/                # маршруты API (auth, users)
├── utils/                  # вспомогательные функции (jwt, hash и т.д.)
├── models.py               # модели SQLAlchemy
├── schemas.py              # Pydantic-схемы
├── config.py               # переменные окружения и настройки
├── database.py             # подключение к БД
├── main.py                 # точка входа приложения
├── Dockerfile              # сборка контейнера
├── docker-entrypoint.sh    # запуск миграций и сервера
├── alembic.ini             # конфигурация Alembic
└── requirements.txt        # зависимости
```

## 🚀 Как запустить

```bash
# Клонировать проект и перейти в директорию
git clone https://github.com/your-org/chatty-auth-service.git
cd auth_service

# Запуск в Docker
docker-compose up --build
```

Сервис будет доступен по адресу:  
`http://localhost:<порт>` (обычно 8000 или другой)

## 📄 Документация

Swagger UI доступен по адресу:  
```
http://localhost:<порт>/docs
```

## 📦 Авторизация

Каждый защищённый маршрут требует JWT-токен:

```
Authorization: Bearer <ваш_токен>
```

Токен содержит ID и роль пользователя. Используется для проверки прав.

## 🧪 Тестирование

```bash
pytest
```

В проекте реализованы юнит- и интеграционные тесты (если есть `tests/`).

## 🔄 Миграции

```bash
# создание новой миграции
alembic revision --autogenerate -m "описание"

# применение миграций
alembic upgrade head
```

## 👤 Роли пользователей

- `user` — обычный пользователь
- `admin` — имеет расширенные права, например, на управление другими пользователями

## 🧾 Переменные окружения (пример .env)

```env
POSTGRES_URL=postgresql://user:password@db:5432/auth_db
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```


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
 
