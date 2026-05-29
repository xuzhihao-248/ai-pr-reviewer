"""GitHub 客户端接口"""

from abc import ABC, abstractmethod


class GitHubClientInterface(ABC):
    """GitHub 客户端接口"""

    @abstractmethod
    async def get_pr(self, repo: str, pr_number: int) -> dict:
        """
        获取 PR 元数据

        Args:
            repo: 仓库名称 (owner/repo)
            pr_number: PR 编号

        Returns:
            PR 元数据字典

        Raises:
            PRNotFoundError: PR 未找到
            GitHubAPIError: API 调用失败
        """
        pass

    @abstractmethod
    async def get_pr_files(self, repo: str, pr_number: int) -> list[dict]:
        """
        获取 PR 文件变更

        Args:
            repo: 仓库名称
            pr_number: PR 编号

        Returns:
            文件变更字典列表

        Raises:
            GitHubAPIError: API 调用失败
        """
        pass

    @abstractmethod
    async def get_pr_diff(self, repo: str, pr_number: int) -> str:
        """
        获取 PR 差异

        Args:
            repo: 仓库名称
            pr_number: PR 编号

        Returns:
            差异内容字符串

        Raises:
            GitHubAPIError: API 调用失败
        """
        pass

    @abstractmethod
    async def get_file_content(
        self, repo: str, file_path: str, ref: str
    ) -> str:
        """
        获取文件内容

        Args:
            repo: 仓库名称
            file_path: 文件路径
            ref: Git 引用

        Returns:
            文件内容字符串

        Raises:
            FileNotFoundError: 文件未找到
            GitHubAPIError: API 调用失败
        """
        pass

    @abstractmethod
    async def post_comment(self, repo: str, pr_number: int, body: str) -> bool:
        """
        发布评论到 PR

        Args:
            repo: 仓库名称
            pr_number: PR 编号
            body: 评论内容 (Markdown)

        Returns:
            如果成功返回 True

        Raises:
            AuthenticationError: 认证失败
            PermissionError: 权限不足
            GitHubAPIError: API 调用失败
        """
        pass
