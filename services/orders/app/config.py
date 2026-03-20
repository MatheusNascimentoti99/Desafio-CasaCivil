from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database (composed from individual env vars)
    ORDERS_DB_USER: str = "orders_user"
    ORDERS_DB_PASSWORD: str = "orders_pass"
    ORDERS_DB_NAME: str = "orders_db"

    # JWT (RS256) — only needs the PUBLIC key to verify tokens
    JWT_ALGORITHM: str = "RS256"
    JWT_PUBLIC_KEY: str = ""

    # Service
    SERVICE_NAME: str = "orders-service"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.ORDERS_DB_USER}:{self.ORDERS_DB_PASSWORD}@orders-db:5432/{self.ORDERS_DB_NAME}"

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return f"postgresql://{self.ORDERS_DB_USER}:{self.ORDERS_DB_PASSWORD}@orders-db:5432/{self.ORDERS_DB_NAME}"

    @property
    def public_key(self) -> str:
        """Decode escaped newlines from env var."""
        return self.JWT_PUBLIC_KEY.replace("\\n", "\n")


settings = Settings()
