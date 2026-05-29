"""GitHub client interface"""

from abc import ABC, abstractmethod


class GitHubClientInterface(ABC):
    """GitHub client interface"""

    @abstractmethod
    async def get_pr(self, repo: str, pr_number: int) -> dict:
        """
        Get PR metadata

        Args:
            repo: Repository name (owner/repo)
            pr_number: PR number

        Returns:
            PR metadata dictionary

        Raises:
            PRNotFoundError: PR not found
            GitHubAPIError: API call failed
        """
        pass

    @abstractmethod
    async def get_pr_files(self, repo: str, pr_number: int) -> list[dict]:
        """
        Get PR file changes

        Args:
            repo: Repository name
            pr_number: PR number

        Returns:
            List of file change dictionaries

        Raises:
            GitHubAPIError: API call failed
        """
        pass

    @abstractmethod
    async def get_pr_diff(self, repo: str, pr_number: int) -> str:
        """
        Get PR diff

        Args:
            repo: Repository name
            pr_number: PR number

        Returns:
            Diff content as string

        Raises:
            GitHubAPIError: API call failed
        """
        pass

    @abstractmethod
    async def get_file_content(
        self, repo: str, file_path: str, ref: str
    ) -> str:
        """
        Get file content

        Args:
            repo: Repository name
            file_path: File path
            ref: Git reference

        Returns:
            File content as string

        Raises:
            FileNotFoundError: File not found
            GitHubAPIError: API call failed
        """
        pass

    @abstractmethod
    async def post_comment(self, repo: str, pr_number: int, body: str) -> bool:
        """
        Post comment to PR

        Args:
            repo: Repository name
            pr_number: PR number
            body: Comment body (Markdown)

        Returns:
            True if successful

        Raises:
            AuthenticationError: Auth failed
            PermissionError: Permission denied
            GitHubAPIError: API call failed
        """
        pass
