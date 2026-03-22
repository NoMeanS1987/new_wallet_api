import pytest
import time
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from main import app
from database import DATABASE_URL, get_db
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def client():
    engine = create_async_engine(DATABASE_URL)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    await engine.dispose()
    app.dependency_overrides.clear()

async def test_create_wallet(client):
    owner = f"User_{time.time_ns()}"
    response = await client.post(f"/wallets?owner={owner}")
    assert response.status_code == 200
    assert response.json()["balance"] == 0

async def test_get_wallet(client):
    owner = f"User_{time.time_ns()}"
    create = await client.post(f"/wallets?owner={owner}")
    wallet_id = create.json()["wallet_id"]
    response = await client.get(f"/wallets/{wallet_id}")
    assert response.status_code == 200

async def test_deposit(client):
    owner = f"User_{time.time_ns()}"
    create = await client.post(f"/wallets?owner={owner}")
    wallet_id = create.json()["wallet_id"]
    response = await client.post(f"/wallets/{wallet_id}/operation", json={"operation_type": "DEPOSIT", "amount": 500})
    assert response.status_code == 200
    assert response.json()["balance"] == 500

async def test_withdraw(client):
    owner = f"User_{time.time_ns()}"
    create = await client.post(f"/wallets?owner={owner}")
    wallet_id = create.json()["wallet_id"]
    await client.post(f"/wallets/{wallet_id}/operation", json={"operation_type": "DEPOSIT", "amount": 500})
    response = await client.post(f"/wallets/{wallet_id}/operation", json={"operation_type": "WITHDRAW", "amount": 200})
    assert response.status_code == 200
    assert response.json()["balance"] == 300

async def test_invalid_operation(client):
    owner = f"User_{time.time_ns()}"
    create = await client.post(f"/wallets?owner={owner}")
    wallet_id = create.json()["wallet_id"]
    response = await client.post(f"/wallets/{wallet_id}/operation", json={"operation_type": "INVALID", "amount": 100})
    assert response.status_code == 400

async def test_wallet_not_found(client):
    response = await client.get("/wallets/99999")
    assert response.status_code == 404