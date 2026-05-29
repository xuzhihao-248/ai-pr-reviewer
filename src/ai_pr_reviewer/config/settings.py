"""应用程序配置"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用程序配置"""

    # AI 配置
    ai_base_url: str = "https://api.deepseek.com"
    ai_api_key: str = ""
    ai_model: str = "deepseek-chat"
    ai_max_tokens: int = 4096
    ai_temperature: float = 0.1

    # GitHub 配置
    github_token: str = ""  # 可选，优先使用 gh CLI

    # 分析配置
    max_concurrent_files: int = 5
    max_file_size: int = 10000  # 字符数
    analysis_timeout: int = 120  # 秒

    # 数据库配置
    database_path: str = "data/analysis.db"

    # Web 服务配置（预留）
    web_host: str = "0.0.0.0"
    web_port: int = 8000

    model_config = {"env_file": ".env", "env_prefix": "AI_PR_REVIEWER_"}


# 全局配置实例
settings = Settings()
