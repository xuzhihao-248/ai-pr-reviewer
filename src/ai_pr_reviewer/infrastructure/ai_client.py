"""AI client interface"""

from abc import ABC, abstractmethod


class AIClientInterface(ABC):
    """AI client interface for code analysis"""

    @abstractmethod
    async def analyze_code(
        self,
        file_diff: str,
        file_path: str,
        context_files: list[str] | None = None,
    ) -> dict:
        """
        Analyze code using AI

        Args:
            file_diff: File diff content
            file_path: File path
            context_files: Related file contents (optional)

        Returns:
            Dictionary with analysis results:
            {
                "issues": [
                    {
                        "severity": "high|medium|low|info",
                        "type": "security|logic|style|performance",
                        "line_number": int | null,
                        "description": str,
                        "suggestion": str
                    }
                ],
                "highlights": [
                    {
                        "line_range": [start, end] | null,
                        "description": str
                    }
                ],
                "summary": str
            }

        Raises:
            AIAPIError: AI API call failed
            AnalysisTimeoutError: Analysis timeout
        """
        pass
