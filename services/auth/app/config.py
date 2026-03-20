from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database (composed from individual env vars)
    AUTH_DB_USER: str = "auth_user"
    AUTH_DB_PASSWORD: str = "auth_pass"
    AUTH_DB_NAME: str = "auth_db"

    # JWT (RS256)
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_PRIVATE_KEY: str = ""
    JWT_PUBLIC_KEY: str = ""

    # Service
    SERVICE_NAME: str = "auth-service"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.AUTH_DB_USER}:{self.AUTH_DB_PASSWORD}@auth-db:5432/{self.AUTH_DB_NAME}"

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return f"postgresql://{self.AUTH_DB_USER}:{self.AUTH_DB_PASSWORD}@auth-db:5432/{self.AUTH_DB_NAME}"

    @property
    def private_key(self) -> str:
        """Decode escaped newlines from env var."""
        return self.JWT_PRIVATE_KEY.replace("\\n", "\n")

    @property
    def public_key(self) -> str:
        """Decode escaped newlines from env var."""
        return self.JWT_PUBLIC_KEY.replace("\\n", "\n")


settings = Settings()
