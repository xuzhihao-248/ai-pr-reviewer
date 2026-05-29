"""GitHub PR 链接的 URL 解析器"""

import re

from ai_pr_reviewer.exceptions import InvalidPRError

# GitHub PR URL 模式
PR_URL_PATTERN = re.compile(
    r"https?://github\.com/(?P<repo>[^/]+/[^/]+)/pull/(?P<number>\d+)"
)


def parse_pr_url(url: str) -> tuple[str, int]:
    """
    解析 GitHub PR URL

    Args:
        url: PR URL，如 https://github.com/owner/repo/pull/123

    Returns:
        (repo, pr_number) 元组

    Raises:
        InvalidPRError: 如果 URL 格式无效
    """
    match = PR_URL_PATTERN.match(url)
    if not match:
        raise InvalidPRError(
            f"无效的 PR URL 格式: {url}\n"
            "期望格式: https://github.com/owner/repo/pull/123"
        )

    repo = match.group("repo")
    number = int(match.group("number"))

    return repo, number


def validate_pr_url(url: str) -> bool:
    """
    验证 GitHub PR URL 格式

    Args:
        url: 要验证的 PR URL

    Returns:
        如果有效返回 True，否则返回 False
    """
    return bool(PR_URL_PATTERN.match(url))
