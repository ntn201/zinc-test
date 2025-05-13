from src.utils.db import Database
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession
import logging
logger = logging.getLogger(__name__)

class HealthController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_health(self) -> bool:
        try:
            await self.session.exec(text("SELECT 1"))
            return True
        except Exception as e:
            logger.exception(e)
            return False
