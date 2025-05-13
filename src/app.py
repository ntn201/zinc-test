from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


from src.views.import_sales import router as import_sales_router
from src.views.metrics import router as metrics_router
from src.views.health import router as health_router

from src.utils.db import init_db, close_db
from src.utils.sentry import init_sentry
app = FastAPI(
    title="FastAPI",
    description="A FastAPI project",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    init_sentry()
    yield
    await close_db()


# Include routers
api_router = APIRouter(prefix="/api")
api_router.include_router(import_sales_router)
api_router.include_router(metrics_router)
app.include_router(api_router)
app.include_router(health_router)

@app.get("/")
async def root():
    return {"message": "Zinc Test API"}
