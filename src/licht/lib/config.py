from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # Email Settings
    resend_api_key: str
    email_from: str = "onboarding@resend.dev"

    # LLM Settings
    llm_model: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None

@lru_cache()
def get_settings() -> Settings:
    return Settings()