# Wallet API

REST API для работы с кошельками пользователей.

## Стек
- FastAPI (async)
- PostgreSQL
- SQLAlchemy (async)
- Alembic
- Docker / docker-compose
- pytest

## Запуск
```bash
docker-compose up --build
```

## Эндпоинты

- `POST /api/v1/wallets/{wallet_id}/operation` — пополнение/снятие
- `GET /api/v1/wallets/{wallet_id}` — получение баланса

## Тесты
```bash
pytest test_main.py -v
```
