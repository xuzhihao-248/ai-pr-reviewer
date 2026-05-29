"""Application exceptions"""


class AppError(Exception):
    """Base application exception"""

    pass


class InvalidPRError(AppError):
    """Invalid PR URL format"""

    pass


class PRNotFoundError(AppError):
    """PR not found"""

    pass


class GitHubAPIError(AppError):
    """GitHub API call failed"""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(AppError):
    """Authentication failed"""

    pass


class PermissionError(AppError):
    """Permission denied"""

    pass


class AIAPIError(AppError):
    """AI API call failed"""

    pass


class AnalysisTimeoutError(AppError):
    """Analysis timeout"""

    pass


class RateLimitError(AppError):
    """API rate limit exceeded"""

    pass
