from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://auth_user:auth_pass@auth-db:5432/auth_db"
    DATABASE_URL_SYNC: str = "postgresql://auth_user:auth_pass@auth-db:5432/auth_db"

    # JWT (RS256)
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_PRIVATE_KEY: str = ""
    JWT_PUBLIC_KEY: str = ""

    # Service
    SERVICE_NAME: str = "auth-service"

    @property
    def private_key(self) -> str:
        """Decode escaped newlines from env var."""
        return self.JWT_PRIVATE_KEY.replace("\\n", "\n")

    @property
    def public_key(self) -> str:
        """Decode escaped newlines from env var."""
        return self.JWT_PUBLIC_KEY.replace("\\n", "\n")

    class Config:
        env_file = ".env"


settings = Settings()
