"""Analysis service interface"""

from abc import ABC, abstractmethod

from ai_pr_reviewer.models.analysis_result import (
    AnalysisResult,
    FileAnalysisResult,
)
from ai_pr_reviewer.models.pr_data import PRData


class AnalysisServiceInterface(ABC):
    """Analysis service interface"""

    @abstractmethod
    async def analyze_pr(self, pr_data: PRData) -> AnalysisResult:
        """
        Analyze entire PR

        Args:
            pr_data: PR data object

        Returns:
            AnalysisResult with all file analysis results

        Note:
            - Automatically filters non-code files
            - Supports concurrent file analysis
            - Includes related file context
        """
        pass

    @abstractmethod
    async def analyze_file(
        self,
        file_diff: str,
        file_path: str,
        context_files: list[str] | None = None,
    ) -> FileAnalysisResult:
        """
        Analyze single file

        Args:
            file_diff: File diff content
            file_path: File path
            context_files: Related file contents (optional)

        Returns:
            FileAnalysisResult for the file
        """
        pass

    @abstractmethod
    async def get_related_files(
        self, repo: str, file_path: str, ref: str
    ) -> list[str]:
        """
        Get related file list

        Args:
            repo: Repository name
            file_path: Current file path
            ref: Git reference

        Returns:
            List of related file paths
        """
        pass
