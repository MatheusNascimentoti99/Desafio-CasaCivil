from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://auth_user:auth_pass@auth-db:5432/auth_db"
    DATABASE_URL_SYNC: str = "postgresql://auth_user:auth_pass@auth-db:5432/auth_db"

    # JWT
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Service
    SERVICE_NAME: str = "auth-service"

    class Config:
        env_file = ".env"


settings = Settings()
