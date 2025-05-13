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


async def test_health_check():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "database": "reachable"}
