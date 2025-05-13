from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.utils.db import get_session
from src.controllers.health import HealthController

router = APIRouter(prefix="/health")

@router.get("")
async def get_health(session: AsyncSession = Depends(get_session)):
    if await HealthController(session).get_health():
        return {
            "status": "ok",
            "database": "reachable"
        }
    else:
        return {
            "status": "error",
            "database": "unreachable"
        }
