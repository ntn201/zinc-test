from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.controllers.import_sales import ImportSalesController
from src.utils.db import get_session

router = APIRouter(prefix="/import-sales")

# THIS ENDPOINT SHOULD BE A POST ENDPOINT TO RETURN 201 CREATED
# RETURN 201 FOR A GET API IS BAD PRACTICE IN RESTFUL API
@router.post("")
async def import_sales(truncate_table: bool = False, session: AsyncSession = Depends(get_session)):
    imported_rows = await ImportSalesController(session=session).import_sales(truncate_table)
    return {
        "imported_rows": imported_rows
    }
