from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    ORDERS_SERVICE_URL: str = "http://orders-service:8002"
    CATALOG_SERVICE_URL: str = "http://catalog-service:8004"

    BFF_COOKIE_NAME: str = "bff_session"
    BFF_COOKIE_SECURE: bool = False
    BFF_COOKIE_SAMESITE: str = "lax"
    BFF_COOKIE_MAX_AGE: int = 3600

    BFF_ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://localhost:5173,http://localhost:5174"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
