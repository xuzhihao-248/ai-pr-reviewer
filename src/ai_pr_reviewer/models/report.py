"""Report models"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ai_pr_reviewer.models.analysis_result import AnalysisResult


class RiskLevel(Enum):
    """Risk level"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Report:
    """Analysis report"""

    pr_url: str
    pr_title: str
    risk_level: RiskLevel
    markdown_content: str
    analysis_result: AnalysisResult
    generated_at: datetime
