from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.decorators import close_cache, init_cache
from app.database import create_tables
from app.routers import orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await init_cache()
    yield
    await close_cache()


app = FastAPI(
    title="Orders Service",
    description="Microsserviço de gestão de pedidos",
    version="1.0.0",
    docs_url="/api/orders/docs",
    openapi_url="/api/orders/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router)


@app.get("/api/orders/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "orders-service"}
