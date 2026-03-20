from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://orders_user:orders_pass@orders-db:5432/orders_db"
    DATABASE_URL_SYNC: str = "postgresql://orders_user:orders_pass@orders-db:5432/orders_db"

    # JWT — mesma chave do auth-service para validar tokens
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"

    # Service
    SERVICE_NAME: str = "orders-service"

    class Config:
        env_file = ".env"


settings = Settings()
