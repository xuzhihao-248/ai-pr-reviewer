"""分析结果模型"""

from dataclasses import dataclass, field
from enum import Enum


class IssueSeverity(Enum):
    """问题严重程度"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueType(Enum):
    """问题类型"""

    SECURITY = "security"
    LOGIC = "logic"
    STYLE = "style"
    PERFORMANCE = "performance"


@dataclass
class Issue:
    """分析中发现的代码问题"""

    severity: IssueSeverity
    type: IssueType
    file_path: str
    line_number: int | None
    description: str
    suggestion: str


@dataclass
class Highlight:
    """代码亮点（正向反馈）"""

    file_path: str
    line_range: tuple[int, int] | None
    description: str


@dataclass
class FileAnalysisResult:
    """单个文件的分析结果"""

    file_path: str
    issues: list[Issue] = field(default_factory=list)
    highlights: list[Highlight] = field(default_factory=list)
    summary: str = ""


@dataclass
class AnalysisResult:
    """PR 的完整分析结果"""

    pr_url: str
    pr_title: str
    file_results: list[FileAnalysisResult] = field(default_factory=list)
    total_issues: int = 0
    total_highlights: int = 0
    overall_summary: str = ""

    def calculate_totals(self) -> None:
        """计算问题和亮点总数"""
        self.total_issues = sum(len(f.issues) for f in self.file_results)
        self.total_highlights = sum(len(f.highlights) for f in self.file_results)
