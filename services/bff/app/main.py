from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.bff import router


app = FastAPI(
    title="BFF Service",
    description="Backend For Frontend do app-host e do mfe-orders",
    version="1.0.0",
    docs_url="/api/bff/docs",
    openapi_url="/api/bff/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.BFF_ALLOWED_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/api/bff/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "bff-service"}
