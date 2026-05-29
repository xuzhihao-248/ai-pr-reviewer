"""PR 数据模型"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PRFile:
    """PR 文件变更"""

    path: str
    status: str  # added, modified, removed（新增、修改、删除）
    additions: int
    deletions: int
    diff: str
    language: str | None = None


@dataclass
class PRData:
    """来自 GitHub 的 PR 数据"""

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
