"""数据库客户端接口"""

from abc import ABC, abstractmethod
from datetime import datetime


class DatabaseClientInterface(ABC):
    """数据库客户端接口"""

    @abstractmethod
    async def initialize(self) -> None:
        """初始化数据库表"""
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
        保存分析记录

        Args:
            pr_url: PR URL
            repo: 仓库名称
            pr_number: PR 编号
            pr_title: PR 标题
            risk_level: 风险等级 (low/medium/high)
            report_markdown: 报告内容
            issues_count: 问题数量
            highlights_count: 亮点数量

        Returns:
            记录 ID
        """
        pass

    @abstractmethod
    async def get_analysis(self, analysis_id: int) -> dict | None:
        """
        根据 ID 获取分析记录

        Args:
            analysis_id: 分析记录 ID

        Returns:
            分析记录或 None
        """
        pass

    @abstractmethod
    async def list_analyses(
        self, limit: int = 20, offset: int = 0
    ) -> list[dict]:
        """
        列出分析记录

        Args:
            limit: 返回的最大记录数
            offset: 跳过的记录数

        Returns:
            分析记录列表
        """
        pass

    @abstractmethod
    async def delete_analysis(self, analysis_id: int) -> bool:
        """
        删除分析记录

        Args:
            analysis_id: 分析记录 ID

        Returns:
            如果删除成功返回 True
        """
        pass

    @abstractmethod
    async def cleanup_old_records(self, days: int = 30) -> int:
        """
        清理旧记录

        Args:
            days: 删除超过此天数的记录

        Returns:
            删除的记录数
        """
        pass
