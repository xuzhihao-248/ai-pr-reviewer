"""报告服务接口"""

from abc import ABC, abstractmethod

from ai_pr_reviewer.models.analysis_result import AnalysisResult
from ai_pr_reviewer.models.report import Report, RiskLevel


class ReportServiceInterface(ABC):
    """报告服务接口"""

    @abstractmethod
    def generate_report(self, analysis_result: AnalysisResult) -> Report:
        """
        生成完整报告

        Args:
            analysis_result: 分析结果

        Returns:
            包含 Markdown 内容和风险等级的 Report 对象
        """
        pass

    @abstractmethod
    def calculate_risk_level(self, analysis_result: AnalysisResult) -> RiskLevel:
        """
        计算风险等级

        Args:
            analysis_result: 分析结果

        Returns:
            RiskLevel (low/medium/high)

        规则:
            - high: 存在安全问题 或 逻辑问题 >= 3
            - medium: 存在逻辑问题 或 代码风格问题 >= 5
            - low: 其他情况
        """
        pass

    @abstractmethod
    def format_markdown(self, report: Report) -> str:
        """
        将报告格式化为 Markdown

        Args:
            report: Report 对象

        Returns:
            Markdown 格式的字符串
        """
        pass

    @abstractmethod
    def format_terminal(self, report: Report) -> str:
        """
        将报告格式化为终端输出（带颜色）

        Args:
            report: Report 对象

        Returns:
            终端格式化的字符串
        """
        pass
