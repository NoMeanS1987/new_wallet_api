# Wallet API

REST API для управления кошельками пользователей с поддержкой конкурентных операций.

## Стек

| Технология | Назначение |
|---|---|
| FastAPI (async) | Web-фреймворк, автодокументация |
| PostgreSQL | Основная БД |
| SQLAlchemy (async) | ORM, асинхронная работа с БД |
| Alembic | Миграции схемы БД |
| Docker / Docker Compose | Контейнеризация и оркестрация |
| pytest | Автоматизированное тестирование |

## Архитектура

```
Client
  │
  ▼
FastAPI (async handlers)
  │
  ▼
SQLAlchemy (async session)
  │
  ▼
PostgreSQL
  │  SELECT FOR UPDATE — защита от race condition
  │  при конкурентных операциях с балансом
```

Ключевое решение: операции с балансом используют `SELECT FOR UPDATE` для предотвращения состояния гонки при параллельных запросах.

## Быстрый старт

### Требования
- Docker
- Docker Compose

### Запуск

```bash
git clone https://github.com/NoMeanS1987/new_wallet_api
cd new_wallet_api
docker-compose up --build
```

API будет доступен по адресу: `http://localhost:8000`

Документация (Swagger): `http://localhost:8000/docs`

## Эндпоинты

### Операция с балансом
```
POST /api/v1/wallets/{wallet_id}/operation
```

**Тело запроса:**
```json
{
  "operationType": "DEPOSIT",
  "amount": 100.00
}
```

**Типы операций:**
- `DEPOSIT` — пополнение
- `WITHDRAW` — снятие

**Пример ответа:**
```json
{
  "wallet_id": "uuid",
  "balance": 100.00
}
```

---

### Получение баланса
```
GET /api/v1/wallets/{wallet_id}
```

**Пример ответа:**
```json
{
  "wallet_id": "uuid",
  "balance": 100.00
}
```

## Тесты

```bash
# Запуск тестов
pytest test_main.py -v

# С покрытием
pytest test_main.py -v --cov=app
```

Тесты покрывают:
- Базовые операции DEPOSIT / WITHDRAW
- Граничные случаи (недостаточно средств, невалидные данные)
- Конкурентные запросы (race condition)

## Миграции

```bash
# Применить миграции
alembic upgrade head

# Создать новую миграцию
alembic revision --autogenerate -m "description"

# Откатить последнюю
alembic downgrade -1
```

## Структура проекта

```
wallet_api/
├── app/
│   ├── main.py          # Точка входа, роутеры
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы
│   ├── crud.py          # Операции с БД
│   └── database.py      # Настройка подключения
├── alembic/             # Миграции
├── tests/
│   └── test_main.py     # Тесты
├── docker-compose.yml
└── Dockerfile
```
