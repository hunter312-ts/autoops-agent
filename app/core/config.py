from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration.
    Reads values from the .env file.
    """
    APP_NAME: str = "AutoOps Agent"
    GROQ_API_KEY: str
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = "AutoOps-Agent"
    DATABASE_URL: str = "sqlite:///autoops.db"
    DEBUG: bool = True
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
settings = Settings()