"""文件过滤工具"""

from ai_pr_reviewer.models.pr_data import PRFile

# 需要排除的文件模式
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

# 需要包含的代码文件扩展名
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
    检查文件是否为需要分析的代码文件

    Args:
        file: PR 文件对象

    Returns:
        如果文件需要分析则返回 True
    """
    path = file.path.lower()

    # 检查排除模式
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if path.endswith(pattern[1:]):
                return False
        elif path.endswith(pattern) or path == pattern:
            return False

    # 检查代码扩展名
    for ext in CODE_EXTENSIONS:
        if path.endswith(ext):
            return True

    return False


def filter_code_files(files: list[PRFile]) -> list[PRFile]:
    """
    过滤 PR 文件，只保留代码文件

    Args:
        files: PR 文件列表

    Returns:
        过滤后的代码文件列表
    """
    return [f for f in files if is_code_file(f)]
