"""Database client interface"""

from abc import ABC, abstractmethod
from datetime import datetime


class DatabaseClientInterface(ABC):
    """Database client interface"""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize database tables"""
        pass

    @abstractmethod
    async def save_analysis(
        self,
        pr_url: str,
        repo: str,
        pr_number: int,
        pr_title: str,
        risk_level: str,
        report_markdown: str,
        issues_count: int,
        highlights_count: int,
    ) -> int:
        """
        Save analysis record

        Args:
            pr_url: PR URL
            repo: Repository name
            pr_number: PR number
            pr_title: PR title
            risk_level: Risk level (low/medium/high)
            report_markdown: Report content
            issues_count: Number of issues
            highlights_count: Number of highlights

        Returns:
            Record ID
        """
        pass

    @abstractmethod
    async def get_analysis(self, analysis_id: int) -> dict | None:
        """
        Get analysis record by ID

        Args:
            analysis_id: Analysis record ID

        Returns:
            Analysis record or None
        """
        pass

    @abstractmethod
    async def list_analyses(
        self, limit: int = 20, offset: int = 0
    ) -> list[dict]:
        """
        List analysis records

        Args:
            limit: Max records to return
            offset: Records to skip

        Returns:
            List of analysis records
        """
        pass

    @abstractmethod
    async def delete_analysis(self, analysis_id: int) -> bool:
        """
        Delete analysis record

        Args:
            analysis_id: Analysis record ID

        Returns:
            True if deleted
        """
        pass

    @abstractmethod
    async def cleanup_old_records(self, days: int = 30) -> int:
        """
        Cleanup old records

        Args:
            days: Delete records older than this many days

        Returns:
            Number of deleted records
        """
        pass
