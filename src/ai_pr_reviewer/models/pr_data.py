"""PR data models"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PRFile:
    """PR file change"""

    path: str
    status: str  # added, modified, removed
    additions: int
    deletions: int
    diff: str
    language: str | None = None


@dataclass
class PRData:
    """PR data from GitHub"""

    url: str
    repo: str  # owner/repo
    number: int
    title: str
    description: str
    author: str
    created_at: datetime
    base_branch: str
    head_branch: str
    files: list[PRFile]
    diff: str
