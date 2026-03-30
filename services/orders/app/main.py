from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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


def _translate_validation_message(error: dict) -> str:
    error_type = error.get("type")
    ctx = error.get("ctx", {}) or {}

    if error_type == "missing":
        return "Campo obrigatório"
    if error_type == "string_too_short":
        return f"Texto deve ter no mínimo {ctx.get('min_length', 0)} caracteres"
    if error_type == "string_too_long":
        return f"Texto deve ter no máximo {ctx.get('max_length', 0)} caracteres"
    if error_type == "string_pattern_mismatch":
        return "Formato inválido"
    if error_type == "greater_than":
        return f"Valor deve ser maior que {ctx.get('gt')}"
    if error_type == "greater_than_equal":
        return f"Valor deve ser maior ou igual a {ctx.get('ge')}"
    if error_type == "float_parsing" or error_type == "int_parsing":
        return "Valor numérico inválido"

    return "Valor inválido"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc: RequestValidationError):
    translated_errors: list[dict] = []

    for error in exc.errors():
        translated = dict(error)
        translated["msg"] = _translate_validation_message(error)
        translated_errors.append(translated)

    return JSONResponse(status_code=422, content={"detail": translated_errors})


@app.get("/api/orders/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "orders-service"}
