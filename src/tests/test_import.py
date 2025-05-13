import pytest
from httpx import ASGITransport, AsyncClient
from src.app import app

from src.utils.db import get_session

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool  
from sqlalchemy import text

from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.product import Product
from src.controllers.import_sales import ImportSalesController

import pandas as pd

df = pd.read_csv("sales.csv")

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
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

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
async def test_import_sales(client, session):
    response = await client.post("/api/import-sales")
    assert response.status_code == 200
    assert response.json() == {"imported_rows": len(df)}
