from datetime import date
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.controllers.metrics import MetricsController
from src.utils.db import get_session

router = APIRouter(prefix="/metrics")

@router.get("/revenue/")
async def get_total_revenue(
    start: date,
    end: date,
    session: AsyncSession = Depends(get_session)
):
    total_revenue, average_order_value = await MetricsController(session).get_revenue_metrics(start, end)
    return {
        "total_revenue_sgd": total_revenue,
        "average_order_value_sgd": average_order_value
    }

@router.get("/revenue/daily/")
async def get_daily_revenue(
    start: date,
    end: date,
    session: AsyncSession = Depends(get_session)
):
    daily_revenue = await MetricsController(session).get_daily_revenue(start, end)
    return daily_revenue
