"""GitHub 服务接口"""

from abc import ABC, abstractmethod

from ai_pr_reviewer.models.pr_data import PRData


class GitHubServiceInterface(ABC):
    """GitHub 服务接口"""

    @abstractmethod
    async def get_pr_data(self, pr_url: str) -> PRData:
        """
        从 GitHub 获取 PR 数据

        Args:
            pr_url: PR URL，如 https://github.com/owner/repo/pull/123

        Returns:
            包含元数据、文件和差异的 PRData 对象

        Raises:
            InvalidPRError: 无效的 PR URL 格式
            PRNotFoundError: PR 未找到
            GitHubAPIError: GitHub API 调用失败
        """
        pass

    @abstractmethod
    async def get_file_content(
        self, repo: str, file_path: str, ref: str
    ) -> str:
        """
        获取文件内容用于上下文分析

        Args:
            repo: 仓库名称 (owner/repo)
            file_path: 文件路径
            ref: Git 引用（提交 sha、分支等）

        Returns:
            文件内容字符串

        Raises:
            FileNotFoundError: 文件未找到
            GitHubAPIError: GitHub API 调用失败
        """
        pass

    @abstractmethod
    async def post_comment(self, pr_url: str, comment: str) -> bool:
        """
        发布评论到 PR

        Args:
            pr_url: PR URL
            comment: 评论内容 (Markdown 格式)

        Returns:
            如果成功返回 True

        Raises:
            AuthenticationError: 认证失败
            PermissionError: 权限不足
            GitHubAPIError: GitHub API 调用失败
        """
        pass
