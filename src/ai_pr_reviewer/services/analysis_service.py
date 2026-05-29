"""分析服务接口"""

from abc import ABC, abstractmethod

from ai_pr_reviewer.models.analysis_result import (
    AnalysisResult,
    FileAnalysisResult,
)
from ai_pr_reviewer.models.pr_data import PRData


class AnalysisServiceInterface(ABC):
    """分析服务接口"""

    @abstractmethod
    async def analyze_pr(self, pr_data: PRData) -> AnalysisResult:
        """
        分析整个 PR

        Args:
            pr_data: PR 数据对象

        Returns:
            包含所有文件分析结果的 AnalysisResult

        Note:
            - 自动过滤非代码文件
            - 支持并发文件分析
            - 包含相关文件上下文
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
        分析单个文件

        Args:
            file_diff: 文件差异内容
            file_path: 文件路径
            context_files: 相关文件内容（可选）

        Returns:
            该文件的 FileAnalysisResult
        """
        pass

    @abstractmethod
    async def get_related_files(
        self, repo: str, file_path: str, ref: str
    ) -> list[str]:
        """
        获取相关文件列表

        Args:
            repo: 仓库名称
            file_path: 当前文件路径
            ref: Git 引用

        Returns:
            相关文件路径列表
        """
        pass
