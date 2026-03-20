from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://orders_user:orders_pass@orders-db:5432/orders_db"
    DATABASE_URL_SYNC: str = "postgresql://orders_user:orders_pass@orders-db:5432/orders_db"

    # JWT (RS256) — only needs the PUBLIC key to verify tokens
    JWT_ALGORITHM: str = "RS256"
    JWT_PUBLIC_KEY: str = ""

    # Service
    SERVICE_NAME: str = "orders-service"

    @property
    def public_key(self) -> str:
        """Decode escaped newlines from env var."""
        return self.JWT_PUBLIC_KEY.replace("\\n", "\n")

    class Config:
        env_file = ".env"


settings = Settings()
