from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_NAME: str = "FastAPI App"
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    SECRET_KEY: str = "change-this-in-production"

    # sync psycopg2 URL — no +asyncpg prefix
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mydb"

    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


settings = Settings()
