"""应用程序异常"""


class AppError(Exception):
    """基础应用程序异常"""

    pass


class InvalidPRError(AppError):
    """无效的 PR URL 格式"""

    pass


class PRNotFoundError(AppError):
    """PR 未找到"""

    pass


class GitHubAPIError(AppError):
    """GitHub API 调用失败"""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(AppError):
    """认证失败"""

    pass


class PermissionError(AppError):
    """权限不足"""

    pass


class AIAPIError(AppError):
    """AI API 调用失败"""

    pass


class AnalysisTimeoutError(AppError):
    """分析超时"""

    pass


class RateLimitError(AppError):
    """API 速率限制超出"""

    pass
