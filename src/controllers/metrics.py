import asyncio
from datetime import date

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select, text, func
from src.utils.db import get_session

from src.models.order import Order

from src.helpers.datetime import get_date_range

class MetricsController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_total_revenue(
        self,
        start: date,
        end: date
    ) -> float:
        query = select(func.sum(Order.total)).where(Order.date >= start, Order.date <= end)
        total_revenue = await self.session.exec(query)
        return total_revenue.scalar()

    async def get_number_of_orders(
        self,
        start: date,
        end: date
    ) -> int:
        query = select(func.count(Order.id)).where(Order.date >= start, Order.date <= end)
        total_orders = await self.session.exec(query)
        return total_orders.scalar()

    async def get_revenue_metrics(
        self,
        start: date,
        end: date,
    ) -> tuple[float, float]:
        total_revenue = await self.get_total_revenue(start, end)
        number_of_orders = await self.get_number_of_orders(start, end)
        if number_of_orders > 0:
            return total_revenue, total_revenue / number_of_orders
        return total_revenue, 0

    async def get_daily_revenue(
        self,
        start: date,
        end: date,
    ) -> list[dict]:
        query = select(
            Order.date,
            func.sum(Order.total).label('revenue')
        ).where(
            Order.date >= start,
            Order.date <= end
        ).group_by(Order.date).order_by(Order.date)

        result = await self.session.exec(query)
        daily_revenues = result.all()
        return [
            {
                "date": revenue.date.strftime("%Y-%m-%d"),
                "revenue_sgd": revenue.revenue
            }
            for revenue in daily_revenues
        ]
