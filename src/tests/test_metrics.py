import pytest
from httpx import ASGITransport, AsyncClient
from src.app import app
from src.utils.db import get_session

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool
from sqlmodel import select, text
from src.controllers.import_sales import ImportSalesController
from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.product import Product


async_engine = create_async_engine(
    "sqlite+aiosqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)

async def get_session_override():
    async with AsyncSession(async_engine) as session:
        yield session

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@pytest.fixture(autouse=True)
async def setup_database():
    await create_tables()
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(async_engine) as session:
        SEED_DATA = [
            text("INSERT INTO products (id, name, price, created_at, updated_at) VALUES (1, 'Test Item', 30, '2024-05-01', '2024-05-01')"),
            text("INSERT INTO orders (id, client_id, sale_id, date, location, discount_percentage, discount_amount, subtotal, tax, total, created_at, updated_at) VALUES (1, 1, 1, '2024-05-01', 'Online Store', 0 , 0, 30, 3, 33, '2024-05-01', '2024-05-01')"),
            text("INSERT INTO orders (id, client_id, sale_id, date, location, discount_percentage, discount_amount, subtotal, tax, total, created_at, updated_at) VALUES (2, 1, 1, '2024-05-02', 'Online Store', 0 , 0, 35, 3.5, 38.5, '2024-05-01', '2024-05-01')"),
            text("INSERT INTO orders (id, client_id, sale_id, date, location, discount_percentage, discount_amount, subtotal, tax, total, created_at, updated_at) VALUES (3, 1, 1, '2024-05-03', 'Online Store', 0 , 0, 40, 4, 44, '2024-05-01', '2024-05-01')"),
            text("INSERT INTO orders (id, client_id, sale_id, date, location, discount_percentage, discount_amount, subtotal, tax, total, created_at, updated_at) VALUES (4, 1, 1, '2024-05-04', 'Online Store', 0 , 0, 45, 4.5, 49.5, '2024-05-01', '2024-05-01')"),
            text("INSERT INTO orders (id, client_id, sale_id, date, location, discount_percentage, discount_amount, subtotal, tax, total, created_at, updated_at) VALUES (5, 1, 1, '2024-05-05', 'Online Store', 0 , 0, 50, 5, 55, '2024-05-01', '2024-05-01')"),
        ]
        for query in SEED_DATA:
            await session.exec(query)
        await session.commit()

@pytest.fixture(name="session")
async def session_fixture():
    async with AsyncSession(async_engine) as session:
        yield session

@pytest.fixture(name="client")
async def client_fixture():
    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_total_revenue(client, session):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        start = "2024-05-01"
        end = "2024-05-30"
        response = await client.get(f"/api/metrics/revenue/?start={start}&end={end}")
        assert response.status_code == 200
        assert response.json() == {
            "total_revenue_sgd": 220,
            "average_order_value_sgd": 44
        }

@pytest.mark.asyncio
async def test_get_total_revenue_daily(client, session):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        start = "2024-05-01"
        end = "2024-05-30"
        response = await client.get(f"/api/metrics/revenue/daily/?start={start}&end={end}&location=Online Store")
        assert response.status_code == 200
        assert response.json() == [
            {
                "date": "2024-05-01",
                "revenue_sgd": 33,
            },
            {
                "date": "2024-05-02",
                "revenue_sgd": 38.5,
            },
            {
                "date": "2024-05-03",
                "revenue_sgd": 44,
            },
            {
                "date": "2024-05-04",
                "revenue_sgd": 49.5,
            },
            {
                "date": "2024-05-05",
                "revenue_sgd": 55,
            }
        ]
