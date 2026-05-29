"""报告模型"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ai_pr_reviewer.models.analysis_result import AnalysisResult


class RiskLevel(Enum):
    """风险等级"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Report:
    """分析报告"""

    pr_url: str
    pr_title: str
    risk_level: RiskLevel
    markdown_content: str
    analysis_result: AnalysisResult
    generated_at: datetime
