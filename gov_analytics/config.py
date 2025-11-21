from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    DATA_GOV_API_KEY: Optional[str] = None
    ETL_TRIGGER_SECRET: Optional[str] = None
    DVC_REMOTE: Optional[str] = None
    DEFAULT_TIMEOUT: int = Field(30, description="HTTP timeout seconds")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
