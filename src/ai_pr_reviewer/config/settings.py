"""Application settings"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration"""

    # AI configuration
    ai_base_url: str = "https://api.deepseek.com"
    ai_api_key: str = ""
    ai_model: str = "deepseek-chat"
    ai_max_tokens: int = 4096
    ai_temperature: float = 0.1

    # GitHub configuration
    github_token: str = ""  # Optional, prefer gh CLI

    # Analysis configuration
    max_concurrent_files: int = 5
    max_file_size: int = 10000  # characters
    analysis_timeout: int = 120  # seconds

    # Database configuration
    database_path: str = "data/analysis.db"

    # Web service configuration (reserved)
    web_host: str = "0.0.0.0"
    web_port: int = 8000

    model_config = {"env_file": ".env", "env_prefix": "AI_PR_REVIEWER_"}


# Global settings instance
settings = Settings()
