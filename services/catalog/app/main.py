from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.decorators import close_cache, init_cache
from app.database import create_tables
from app.routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await init_cache()
    yield
    await close_cache()


app = FastAPI(
    title="Catalog Service",
    description="Microsserviço de catálogo de produtos",
    version="1.0.0",
    docs_url="/api/catalog/docs",
    openapi_url="/api/catalog/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)


@app.get("/api/catalog/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "catalog-service"}
