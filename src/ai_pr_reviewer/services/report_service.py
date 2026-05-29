"""Report service interface"""

from abc import ABC, abstractmethod

from ai_pr_reviewer.models.analysis_result import AnalysisResult
from ai_pr_reviewer.models.report import Report, RiskLevel


class ReportServiceInterface(ABC):
    """Report service interface"""

    @abstractmethod
    def generate_report(self, analysis_result: AnalysisResult) -> Report:
        """
        Generate complete report

        Args:
            analysis_result: Analysis result

        Returns:
            Report object with Markdown content and risk level
        """
        pass

    @abstractmethod
    def calculate_risk_level(self, analysis_result: AnalysisResult) -> RiskLevel:
        """
        Calculate risk level

        Args:
            analysis_result: Analysis result

        Returns:
            RiskLevel (low/medium/high)

        Rules:
            - high: Has security issues OR logic issues >= 3
            - medium: Has logic issues OR style issues >= 5
            - low: Otherwise
        """
        pass

    @abstractmethod
    def format_markdown(self, report: Report) -> str:
        """
        Format report as Markdown

        Args:
            report: Report object

        Returns:
            Markdown formatted string
        """
        pass

    @abstractmethod
    def format_terminal(self, report: Report) -> str:
        """
        Format report for terminal output (with colors)

        Args:
            report: Report object

        Returns:
            Terminal formatted string
        """
        pass
