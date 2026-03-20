from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables
from app.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if they don't exist
    await create_tables()
    yield


app = FastAPI(
    title="Auth Service",
    description="Microsserviço de autenticação e gestão de usuários",
    version="1.0.0",
    docs_url="/api/auth/docs",
    openapi_url="/api/auth/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)


@app.get("/api/auth/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "auth-service"}
