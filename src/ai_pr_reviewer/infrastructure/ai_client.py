"""AI 客户端接口"""

from abc import ABC, abstractmethod


class AIClientInterface(ABC):
    """用于代码分析的 AI 客户端接口"""

    @abstractmethod
    async def analyze_code(
        self,
        file_diff: str,
        file_path: str,
        context_files: list[str] | None = None,
    ) -> dict:
        """
        使用 AI 分析代码

        Args:
            file_diff: 文件差异内容
            file_path: 文件路径
            context_files: 相关文件内容（可选）

        Returns:
            分析结果字典：
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
            AIAPIError: AI API 调用失败
            AnalysisTimeoutError: 分析超时
        """
        pass
