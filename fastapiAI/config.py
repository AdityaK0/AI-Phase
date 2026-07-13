from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    API_KEY: str
    TMDB_API_KEY: str
    DATABASE_URL: str


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


settings = Settings()