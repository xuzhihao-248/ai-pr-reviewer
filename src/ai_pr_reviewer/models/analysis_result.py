"""Analysis result models"""

from dataclasses import dataclass, field
from enum import Enum


class IssueSeverity(Enum):
    """Issue severity level"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueType(Enum):
    """Issue type"""

    SECURITY = "security"
    LOGIC = "logic"
    STYLE = "style"
    PERFORMANCE = "performance"


@dataclass
class Issue:
    """Code issue found in analysis"""

    severity: IssueSeverity
    type: IssueType
    file_path: str
    line_number: int | None
    description: str
    suggestion: str


@dataclass
class Highlight:
    """Code highlight (positive feedback)"""

    file_path: str
    line_range: tuple[int, int] | None
    description: str


@dataclass
class FileAnalysisResult:
    """Analysis result for a single file"""

    file_path: str
    issues: list[Issue] = field(default_factory=list)
    highlights: list[Highlight] = field(default_factory=list)
    summary: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result for a PR"""

    pr_url: str
    pr_title: str
    file_results: list[FileAnalysisResult] = field(default_factory=list)
    total_issues: int = 0
    total_highlights: int = 0
    overall_summary: str = ""

    def calculate_totals(self) -> None:
        """Calculate total issues and highlights"""
        self.total_issues = sum(len(f.issues) for f in self.file_results)
        self.total_highlights = sum(len(f.highlights) for f in self.file_results)
