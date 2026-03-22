from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database (composed from individual env vars)
    ORDERS_DB_USER: str = "orders_user"
    ORDERS_DB_PASSWORD: str = "orders_pass"
    ORDERS_DB_NAME: str = "orders_db"
    ORDERS_DB_HOST: str = "orders-db"
    ORDERS_DB_PORT: int = 5432

    # JWT (RS256) — only needs the PUBLIC key to verify tokens
    JWT_ALGORITHM: str = "RS256"
    JWT_PUBLIC_KEY: str = ""

    # Redis / Cache
    REDIS_URL: str = "redis://redis:6379/0"
    CACHE_ENABLED: bool = True
    CACHE_TTL_ORDER: int = 600

    # Service
    SERVICE_NAME: str = "orders-service"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.ORDERS_DB_USER}:{self.ORDERS_DB_PASSWORD}@{self.ORDERS_DB_HOST}:{self.ORDERS_DB_PORT}/{self.ORDERS_DB_NAME}"

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return f"postgresql://{self.ORDERS_DB_USER}:{self.ORDERS_DB_PASSWORD}@{self.ORDERS_DB_HOST}:{self.ORDERS_DB_PORT}/{self.ORDERS_DB_NAME}"
    @property
    def public_key(self) -> str:
        """Decode escaped newlines from env var."""
        return self.JWT_PUBLIC_KEY.replace("\\n", "\n")


settings = Settings()
