"""GitHub service interface"""

from abc import ABC, abstractmethod

from ai_pr_reviewer.models.pr_data import PRData


class GitHubServiceInterface(ABC):
    """GitHub service interface"""

    @abstractmethod
    async def get_pr_data(self, pr_url: str) -> PRData:
        """
        Get PR data from GitHub

        Args:
            pr_url: PR URL like https://github.com/owner/repo/pull/123

        Returns:
            PRData object with metadata, files, and diff

        Raises:
            InvalidPRError: Invalid PR URL format
            PRNotFoundError: PR not found
            GitHubAPIError: GitHub API call failed
        """
        pass

    @abstractmethod
    async def get_file_content(
        self, repo: str, file_path: str, ref: str
    ) -> str:
        """
        Get file content for context analysis

        Args:
            repo: Repository name (owner/repo)
            file_path: File path
            ref: Git reference (commit sha, branch, etc.)

        Returns:
            File content as string

        Raises:
            FileNotFoundError: File not found
            GitHubAPIError: GitHub API call failed
        """
        pass

    @abstractmethod
    async def post_comment(self, pr_url: str, comment: str) -> bool:
        """
        Post comment to PR

        Args:
            pr_url: PR URL
            comment: Comment content (Markdown format)

        Returns:
            True if successful

        Raises:
            AuthenticationError: Authentication failed
            PermissionError: Permission denied
            GitHubAPIError: GitHub API call failed
        """
        pass
