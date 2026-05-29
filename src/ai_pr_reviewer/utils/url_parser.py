"""URL parser for GitHub PR links"""

import re

from ai_pr_reviewer.exceptions import InvalidPRError

# GitHub PR URL pattern
PR_URL_PATTERN = re.compile(
    r"https?://github\.com/(?P<repo>[^/]+/[^/]+)/pull/(?P<number>\d+)"
)


def parse_pr_url(url: str) -> tuple[str, int]:
    """
    Parse GitHub PR URL

    Args:
        url: PR URL like https://github.com/owner/repo/pull/123

    Returns:
        Tuple of (repo, pr_number)

    Raises:
        InvalidPRError: If URL format is invalid
    """
    match = PR_URL_PATTERN.match(url)
    if not match:
        raise InvalidPRError(
            f"Invalid PR URL format: {url}\n"
            "Expected: https://github.com/owner/repo/pull/123"
        )

    repo = match.group("repo")
    number = int(match.group("number"))

    return repo, number


def validate_pr_url(url: str) -> bool:
    """
    Validate GitHub PR URL format

    Args:
        url: PR URL to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(PR_URL_PATTERN.match(url))
