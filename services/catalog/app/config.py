from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    CATALOG_DB_USER: str = "catalog_user"
    CATALOG_DB_PASSWORD: str = "catalog_pass"
    CATALOG_DB_NAME: str = "catalog_db"
    CATALOG_DB_HOST: str = "catalog-db"
    CATALOG_DB_PORT: int = 5432

    SERVICE_NAME: str = "catalog-service"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.CATALOG_DB_USER}:{self.CATALOG_DB_PASSWORD}"
            f"@{self.CATALOG_DB_HOST}:{self.CATALOG_DB_PORT}/{self.CATALOG_DB_NAME}"
        )


settings = Settings()
