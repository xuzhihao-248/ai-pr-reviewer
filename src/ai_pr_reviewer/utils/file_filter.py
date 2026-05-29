"""File filtering utilities"""

from ai_pr_reviewer.models.pr_data import PRFile

# File patterns to exclude from analysis
EXCLUDE_PATTERNS = [
    "*.lock",
    "*.min.js",
    "*.min.css",
    "*.map",
    "*.svg",
    "*.png",
    "*.jpg",
    "*.gif",
    "*.ico",
    "*.woff",
    "*.woff2",
    "*.ttf",
    "*.eot",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Cargo.lock",
    "go.sum",
]

# Code file extensions to include
CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".kt",
    ".scala",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".swift",
    ".m",
    ".mm",
    ".r",
    ".sql",
    ".sh",
    ".bash",
    ".yaml",
    ".yml",
    ".json",
    ".xml",
    ".html",
    ".css",
    ".scss",
    ".less",
    ".md",
    ".txt",
}


def is_code_file(file: PRFile) -> bool:
    """
    Check if file is a code file that should be analyzed

    Args:
        file: PR file object

    Returns:
        True if file should be analyzed
    """
    path = file.path.lower()

    # Check exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if path.endswith(pattern[1:]):
                return False
        elif path.endswith(pattern) or path == pattern:
            return False

    # Check code extensions
    for ext in CODE_EXTENSIONS:
        if path.endswith(ext):
            return True

    return False


def filter_code_files(files: list[PRFile]) -> list[PRFile]:
    """
    Filter PR files to only include code files

    Args:
        files: List of PR files

    Returns:
        Filtered list of code files
    """
    return [f for f in files if is_code_file(f)]
