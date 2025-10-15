from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    openai_api_key: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"
    api_rate_limit: int = 100
    uniprot_api_url: str = "https://rest.uniprot.org"
    pdb_api_url: str = "https://data.rcsb.org/rest/v1"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
