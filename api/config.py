from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ALLOWED_ORIGINS: list = ["http://localhost", "http://localhost:3000", "http://localhost:9200"]
    DATABASE_URL: PostgresDsn

    SECRET_KEY: str = "root"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "api.log"

    SEARCH_API_KEY: str
    CUSTOM_SEARCH_ENGINE_ID: str

    SEARCH_API_KEY: str
    CUSTOM_SEARCH_ENGINE_ID: str

    class Config:
        env_file = ".env"

settings = Settings()

# Debug print (remember to remove this in production)
print(f"Loaded DATABASE_URL: {settings.DATABASE_URL}")