# AI PR Reviewer — 开发文档

## 1. 技术架构

### 1.1 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      控制层 (Controllers)                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  CLI 控制器 │  │  Web 控制器 │  │  API 控制器 │          │
│  │   (Typer)   │  │  (FastAPI)  │  │  (FastAPI)  │          │
│  └──────┬──────┘  └───────┬─────┘  └────────┬────┘          │
│         │                 │                 │               │
├─────────┼─────────────────┼─────────────────┼───────────────┤
│         ▼                 ▼                 ▼               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    服务层 (Services)                   │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │ │
│  │  │ GitHub 服务 │  │  分析服务   │  │  报告服务   │     │ │
│  │  │             │  │             │  │             │     │ │
│  │  │ - 获取PR    │  │ - 文件分析  │  │ - 生成报告  │     │ │
│  │  │ - 获取Diff  │  │ - 并发控制  │  │ - 风险评级  │     │ │
│  │  │ - 发布评论  │  │ - 上下文获取│  │ - 格式化    │     │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                 │
├───────────────────────────┼─────────────────────────────────┤
│                           ▼                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                基础设施层 (Infrastructure)             │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │ │
│  │  │  AI 客户端  │  │ GitHub客户端│  │ 数据库客户端│     │ │
│  │  │ (DeepSeek)  │  │  (gh CLI)   │  │   (SQLite)  │     │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 设计原则

- **分层架构**：控制层、服务层、基础设施层职责清晰
- **依赖倒置**：服务层依赖接口，不依赖具体实现
- **接口驱动**：服务层提供标准化接口，便于后续 Web UI 调用
- **可测试性**：每层可独立测试，便于单元测试和集成测试

---

## 2. 模块设计

### 2.1 模块划分

```
ai-pr-reviewer/
├── src/
│   ├── __init__.py
│   ├── main.py                    # CLI 入口
│   │
│   ├── controllers/               # 控制层
│   │   ├── __init__.py
│   │   ├── cli.py                 # CLI 控制器
│   │   └── web.py                 # Web 控制器（预留）
│   │
│   ├── services/                  # 服务层（核心业务逻辑）
│   │   ├── __init__.py
│   │   ├── github_service.py      # GitHub 服务
│   │   ├── analysis_service.py    # 分析服务
│   │   └── report_service.py      # 报告服务
│   │
│   ├── models/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── pr_data.py             # PR 数据模型
│   │   ├── analysis_result.py     # 分析结果模型
│   │   └── report.py              # 报告模型
│   │
│   ├── infrastructure/            # 基础设施层
│   │   ├── __init__.py
│   │   ├── ai_client.py           # AI 客户端
│   │   ├── github_client.py       # GitHub 客户端
│   │   └── database.py            # 数据库客户端
│   │
│   ├── utils/                     # 工具函数
│   │   ├── __init__.py
│   │   ├── url_parser.py          # URL 解析
│   │   ├── file_filter.py         # 文件过滤
│   │   └── progress.py            # 进度显示
│   │
│   └── config/                    # 配置管理
│       ├── __init__.py
│       └── settings.py            # 配置文件
│
├── tests/                         # 测试目录
│   ├── unit/
│   └── integration/
│
├── doc/
│   ├── proposal.md
│   └── development.md
│
├── pyproject.toml
└── README.md
```

### 2.2 模块职责

#### 控制层 (Controllers)
- **cli.py**: CLI 命令定义、参数解析、调用服务层
- **web.py**: HTTP 接口定义、请求处理、调用服务层（预留）

#### 服务层 (Services)
- **github_service.py**: GitHub 相关业务逻辑
- **analysis_service.py**: 代码分析业务逻辑、并发控制
- **report_service.py**: 报告生成、风险评级

#### 基础设施层 (Infrastructure)
- **ai_client.py**: AI API 调用封装
- **github_client.py**: GitHub API/CLI 调用封装
- **database.py**: 数据库操作封装

#### 数据模型 (Models)
- **pr_data.py**: PR 元数据、文件列表、Diff 内容
- **analysis_result.py**: 单文件分析结果、问题列表
- **report.py**: 完整报告、风险等级

---

## 3. 接口设计

### 3.1 服务层接口

#### GitHubService 接口

```python
from abc import ABC, abstractmethod
from models.pr_data import PRData

class GitHubServiceInterface(ABC):
    """GitHub 服务接口"""

    @abstractmethod
    async def get_pr_data(self, pr_url: str) -> PRData:
        """
        获取 PR 数据

        Args:
            pr_url: PR 链接，如 https://github.com/owner/repo/pull/123

        Returns:
            PRData: PR 数据对象，包含元数据、文件列表、Diff

        Raises:
            InvalidPRError: PR 链接格式错误
            PRNotFoundError: PR 不存在
            GitHubAPIError: GitHub API 调用失败
        """
        pass

    @abstractmethod
    async def get_file_content(self, repo: str, file_path: str, ref: str) -> str:
        """
        获取文件内容（用于上下文分析）

        Args:
            repo: 仓库名，如 owner/repo
            file_path: 文件路径
            ref: Git 引用（commit sha、branch 等）

        Returns:
            str: 文件内容

        Raises:
            FileNotFoundError: 文件不存在
            GitHubAPIError: GitHub API 调用失败
        """
        pass

    @abstractmethod
    async def post_comment(self, pr_url: str, comment: str) -> bool:
        """
        发布评论到 PR

        Args:
            pr_url: PR 链接
            comment: 评论内容（Markdown 格式）

        Returns:
            bool: 是否成功

        Raises:
            AuthenticationError: 认证失败
            PermissionError: 无权限
            GitHubAPIError: GitHub API 调用失败
        """
        pass
```

#### AnalysisService 接口

```python
from abc import ABC, abstractmethod
from models.pr_data import PRData
from models.analysis_result import AnalysisResult, FileAnalysisResult

class AnalysisServiceInterface(ABC):
    """分析服务接口"""

    @abstractmethod
    async def analyze_pr(self, pr_data: PRData) -> AnalysisResult:
        """
        分析整个 PR

        Args:
            pr_data: PR 数据对象

        Returns:
            AnalysisResult: 分析结果，包含所有文件的分析结果

        Note:
            - 自动过滤非代码文件
            - 支持并发分析多个文件
            - 分析时包含相关文件上下文
        """
        pass

    @abstractmethod
    async def analyze_file(
        self,
        file_diff: str,
        file_path: str,
        context_files: list[str] | None = None
    ) -> FileAnalysisResult:
        """
        分析单个文件

        Args:
            file_diff: 文件的 Diff 内容
            file_path: 文件路径
            context_files: 相关文件内容列表（可选）

        Returns:
            FileAnalysisResult: 单文件分析结果
        """
        pass

    @abstractmethod
    async def get_related_files(
        self,
        repo: str,
        file_path: str,
        ref: str
    ) -> list[str]:
        """
        获取相关文件列表

        Args:
            repo: 仓库名
            file_path: 当前文件路径
            ref: Git 引用

        Returns:
            list[str]: 相关文件路径列表
        """
        pass
```

#### ReportService 接口

```python
from abc import ABC, abstractmethod
from models.analysis_result import AnalysisResult
from models.report import Report, RiskLevel

class ReportServiceInterface(ABC):
    """报告服务接口"""

    @abstractmethod
    def generate_report(self, analysis_result: AnalysisResult) -> Report:
        """
        生成完整报告

        Args:
            analysis_result: 分析结果

        Returns:
            Report: 报告对象，包含 Markdown 内容和风险等级
        """
        pass

    @abstractmethod
    def calculate_risk_level(self, analysis_result: AnalysisResult) -> RiskLevel:
        """
        计算风险等级

        Args:
            analysis_result: 分析结果

        Returns:
            RiskLevel: 风险等级（low/medium/high）

        规则:
            - high: 存在安全漏洞 或 逻辑错误 >= 3
            - medium: 逻辑错误 >= 1 或 代码风格问题 >= 5
            - low: 其他情况
        """
        pass

    @abstractmethod
    def format_markdown(self, report: Report) -> str:
        """
        格式化为 Markdown

        Args:
            report: 报告对象

        Returns:
            str: Markdown 格式的报告内容
        """
        pass

    @abstractmethod
    def format_terminal(self, report: Report) -> str:
        """
        格式化为终端输出（带颜色）

        Args:
            report: 报告对象

        Returns:
            str: 终端格式的报告内容
        """
        pass
```

### 3.2 数据模型

#### PRData 模型

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PRData:
    """PR 数据"""
    url: str                          # PR 链接
    repo: str                         # 仓库名 (owner/repo)
    number: int                       # PR 编号
    title: str                        # PR 标题
    description: str                  # PR 描述
    author: str                       # 作者
    created_at: datetime              # 创建时间
    base_branch: str                  # 目标分支
    head_branch: str                  # 源分支
    files: list[PRFile]              # 变更文件列表
    diff: str                         # 完整 Diff

@dataclass
class PRFile:
    """PR 变更文件"""
    path: str                         # 文件路径
    status: str                       # 状态 (added/modified/removed)
    additions: int                    # 新增行数
    deletions: int                    # 删除行数
    diff: str                         # 文件 Diff
    language: str | None              # 编程语言
```

#### AnalysisResult 模型

```python
from dataclasses import dataclass
from enum import Enum

class IssueSeverity(Enum):
    """问题严重程度"""
    HIGH = "high"           # 高风险（安全漏洞、严重逻辑错误）
    MEDIUM = "medium"       # 中风险（逻辑错误）
    LOW = "low"             # 低风险（代码风格）
    INFO = "info"           # 信息（建议）

class IssueType(Enum):
    """问题类型"""
    SECURITY = "security"           # 安全漏洞
    LOGIC = "logic"                 # 逻辑错误
    STYLE = "style"                 # 代码风格
    PERFORMANCE = "performance"     # 性能问题

@dataclass
class Issue:
    """问题"""
    severity: IssueSeverity          # 严重程度
    type: IssueType                  # 问题类型
    file_path: str                   # 文件路径
    line_number: int | None          # 行号
    description: str                 # 问题描述
    suggestion: str                  # 修复建议

@dataclass
class Highlight:
    """亮点"""
    file_path: str                   # 文件路径
    line_range: tuple[int, int] | None  # 行范围
    description: str                 # 亮点描述

@dataclass
class FileAnalysisResult:
    """单文件分析结果"""
    file_path: str                   # 文件路径
    issues: list[Issue]              # 问题列表
    highlights: list[Highlight]      # 亮点列表
    summary: str                     # 文件变更总结

@dataclass
class AnalysisResult:
    """完整分析结果"""
    pr_url: str                      # PR 链接
    pr_title: str                    # PR 标题
    file_results: list[FileAnalysisResult]  # 各文件分析结果
    total_issues: int                # 问题总数
    total_highlights: int            # 亮点总数
    overall_summary: str             # 整体总结
```

#### Report 模型

```python
from dataclasses import dataclass
from enum import Enum
from models.analysis_result import AnalysisResult

class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Report:
    """报告"""
    pr_url: str                      # PR 链接
    pr_title: str                    # PR 标题
    risk_level: RiskLevel            # 风险等级
    markdown_content: str            # Markdown 内容
    analysis_result: AnalysisResult  # 分析结果
    generated_at: datetime           # 生成时间
```

---

## 4. 核心流程

### 4.1 PR 分析流程

```
用户输入 PR 链接
       │
       ▼
┌──────────────────┐
│  解析 PR 链接    │  url_parser.py
│  验证格式        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  获取 PR 数据    │  github_service.py
│  - 元数据        │
│  - 文件列表      │
│  - Diff 内容     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  过滤文件        │  file_filter.py
│- 只保留代码文件  │
│- 排除 lock 文件  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  获取上下文      │  github_service.py
│ - 相关文件内容   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  并发分析文件    │  analysis_service.py
│  - 调用 AI 分析  │
│  - 收集问题      │
│  - 收集亮点      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  生成报告        │  report_service.py
│  - 汇总结果      │
│  - 计算风险等级  │
│  - 格式化输出    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  输出结果        │
│  - 终端输出      │
│  - 存入数据库    │
│  - 发布评论(可选)│
└──────────────────┘
```

### 4.2 风险等级计算规则

```python
def calculate_risk_level(analysis_result: AnalysisResult) -> RiskLevel:
    """
    计算风险等级

    规则:
        - HIGH: 存在安全漏洞 或 逻辑错误 >= 3
        - MEDIUM: 逻辑错误 >= 1 或 代码风格问题 >= 5
        - LOW: 其他情况
    """
    security_issues = [i for i in all_issues if i.type == IssueType.SECURITY]
    logic_issues = [i for i in all_issues if i.type == IssueType.LOGIC]
    style_issues = [i for i in all_issues if i.type == IssueType.STYLE]

    if security_issues or len(logic_issues) >= 3:
        return RiskLevel.HIGH
    elif logic_issues or len(style_issues) >= 5:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.LOW
```

### 4.3 文件过滤规则

```python
# 需要排除的文件模式
EXCLUDE_PATTERNS = [
    "*.lock",           # 依赖锁定文件
    "*.min.js",         # 压缩文件
    "*.min.css",
    "*.map",            # Source Map
    "*.svg",            # 图片
    "*.png",
    "*.jpg",
    "*.gif",
    "*.ico",
    "*.woff",           # 字体
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
CODE_EXTENSIONS = [
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".kt", ".scala",
    ".c", ".cpp", ".h", ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".swift",
    ".m", ".mm",
    ".r", ".R",
    ".sql",
    ".sh", ".bash",
    ".yaml", ".yml",
    ".json",
    ".xml",
    ".html", ".css", ".scss", ".less",
    ".md",
    ".txt",
]
```

---

## 5. 错误处理

### 5.1 错误类型定义

```python
class AppError(Exception):
    """应用基础异常"""
    pass

class InvalidPRError(AppError):
    """PR 链接格式错误"""
    pass

class PRNotFoundError(AppError):
    """PR 不存在"""
    pass

class GitHubAPIError(AppError):
    """GitHub API 调用失败"""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class AuthenticationError(AppError):
    """认证失败"""
    pass

class PermissionError(AppError):
    """权限不足"""
    pass

class AIAPIError(AppError):
    """AI API 调用失败"""
    pass

class AnalysisTimeoutError(AppError):
    """分析超时"""
    pass

class RateLimitError(AppError):
    """API 限流"""
    pass
```

### 5.2 错误处理策略

| 错误类型 | 处理方式 |
|---------|---------|
| InvalidPRError | 提示用户检查链接格式 |
| PRNotFoundError | 提示 PR 不存在或无权访问 |
| GitHubAPIError | 显示错误码，建议稍后重试 |
| AuthenticationError | 提示用户运行 `gh auth login` |
| PermissionError | 提示用户检查仓库权限 |
| AIAPIError | 显示错误信息，检查 API Key |
| AnalysisTimeoutError | 提示 PR 过大，建议分批分析 |
| RateLimitError | 显示等待时间，自动重试 |

---

## 6. 配置管理

### 6.1 配置项

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    """应用配置"""

    # AI 配置
    ai_base_url: str = "https://api.deepseek.com"
    ai_api_key: str = ""
    ai_model: str = "deepseek-chat"
    ai_max_tokens: int = 4096
    ai_temperature: float = 0.1

    # GitHub 配置
    github_token: str = ""  # 可选，优先使用 gh CLI

    # 分析配置
    max_concurrent_files: int = 5        # 最大并发分析文件数
    max_file_size: int = 10000           # 最大文件大小（字符数）
    analysis_timeout: int = 120          # 分析超时时间（秒）

    # 数据库配置
    database_path: str = "data/analysis.db"

    # Web 服务配置（预留）
    web_host: str = "0.0.0.0"
    web_port: int = 8000

    class Config:
        env_file = ".env"
        env_prefix = "AI_PR_REVIEWER_"
```

### 6.2 环境变量

```bash
# AI 配置
AI_PR_REVIEWER_AI_BASE_URL=https://api.deepseek.com
AI_PR_REVIEWER_AI_API_KEY=your_api_key_here
AI_PR_REVIEWER_AI_MODEL=deepseek-chat

# GitHub 配置（可选）
AI_PR_REVIEWER_GITHUB_TOKEN=your_github_token

# 分析配置
AI_PR_REVIEWER_MAX_CONCURRENT_FILES=5
AI_PR_REVIEWER_ANALYSIS_TIMEOUT=120

# 数据库配置
AI_PR_REVIEWER_DATABASE_PATH=data/analysis.db
```

---

## 7. 报告模板

### 7.1 Markdown 报告格式

```markdown
# PR Review Report

## 基本信息
- **PR**: [标题](链接)
- **作者**: 作者名
- **风险等级**: 🟢 Low / 🟡 Medium / 🔴 High

## 变更总结
简要描述本次 PR 的主要变更内容。

## 问题列表

### 🔴 高风险问题
| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| src/main.py | 42 | SQL 注入风险 | 使用参数化查询 |

### 🟡 中风险问题
| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| src/utils.py | 15 | 空指针风险 | 添加空值检查 |

### 🟢 低风险问题
| 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|
| src/config.py | 8 | 命名不规范 | 使用 snake_case |

## 亮点
- ✅ `src/auth.py`: 良好的错误处理设计
- ✅ `src/models.py`: 清晰的数据模型定义

## 统计
- 分析文件数: 10
- 问题总数: 5 (高: 1, 中: 2, 低: 2)
- 亮点总数: 2
```

---

## 8. 开发规范

### 8.1 代码风格

- 遵循 PEP 8 规范
- 使用类型注解
- 使用 async/await 进行异步编程
- 函数和类必须有文档字符串

### 8.2 命名规范

- 文件名：snake_case
- 类名：PascalCase
- 函数名：snake_case
- 常量：UPPER_SNAKE_CASE

### 8.3 提交规范

```
<type>(<scope>): <subject>

类型:
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

示例:
feat(github): 添加 PR 数据获取功能
fix(analysis): 修复并发分析时的竞态条件
docs(readme): 更新安装说明
```

---

## 9. 开发计划（3天冲刺）

> **截止日期**: 2026年5月31日 23:59
> **策略**: 核心功能优先，非核心功能延后

### Day 1（5月29日）— 基础框架 + 核心链路

**目标**: 跑通最小可用链路（输入 URL → 获取 PR → AI 分析 → 输出报告）

- [ ] **上午**: 项目初始化
  - 创建目录结构
  - pyproject.toml 配置
  - 数据模型定义（PRData, AnalysisResult, Report）
  - 基础异常类

- [ ] **下午**: 基础设施层
  - GitHub 客户端（基于 gh CLI，只实现 get_pr_data）
  - AI 客户端（DeepSeek API，只实现 analyze_file）
  - 配置管理（.env 文件）

- [ ] **晚上**: 服务层骨架
  - GitHub 服务（获取 PR 数据）
  - 分析服务（单文件分析，先不做并发）
  - 报告服务（基础 Markdown 输出）

### Day 2（5月30日）— CLI + 并发 + 完善

**目标**: CLI 可用，支持并发分析，报告格式完善

- [ ] **上午**: CLI 控制层
  - Typer 命令实现（analyze）
  - 进度显示（rich 进度条）
  - 终端输出美化

- [ ] **下午**: 并发分析
  - asyncio 并发分析多个文件
  - 文件过滤（排除非代码文件）
  - 上下文获取（相关文件）

- [ ] **晚上**: 报告完善
  - 风险等级计算
  - 报告模板优化
  - 错误处理（基础）

### Day 3（5月31日）— 收尾 + 测试 + 打磨

**目标**: 功能完整，可演示，基本可用

- [ ] **上午**: 功能补全
  - 历史记录功能（SQLite）
  - 评论发布到 GitHub（可选）
  - CLI help 文档

- [ ] **下午**: 测试与修复
  - 端到端测试（真实 PR）
  - Bug 修复
  - 边界情况处理

- [ ] **晚上**: 打磨与交付
  - README 编写
  - 使用示例
  - 最终检查

---

### 功能优先级

| 优先级 | 功能 | 状态 |
|--------|------|------|
| P0 | PR 数据获取 | Day 1 |
| P0 | AI 代码分析 | Day 1 |
| P0 | 终端报告输出 | Day 1 |
| P0 | CLI 命令 | Day 2 |
| P0 | 并发分析 | Day 2 |
| P0 | 风险等级计算 | Day 2 |
| P1 | 历史记录 | Day 3 |
| P1 | GitHub 评论 | Day 3 |
| P2 | Web 界面 | 延后 |

### 技术债务（可接受）

- 测试覆盖率：核心路径测试即可，不追求 100%
- 错误处理：覆盖主要场景，边缘情况可忽略
- 代码注释：关键逻辑注释，不追求全覆盖
- 性能优化：能用即可，不追求极致

---

## 10. 依赖清单

```toml
[project]
dependencies = [
    "typer>=0.9.0",           # CLI 框架
    "fastapi>=0.100.0",       # Web 框架（预留）
    "uvicorn>=0.23.0",        # ASGI 服务器（预留）
    "httpx>=0.24.0",          # HTTP 客户端
    "openai>=1.0.0",          # OpenAI 兼容客户端
    "pydantic>=2.0.0",        # 数据验证
    "rich>=13.0.0",           # 终端美化
    "aiosqlite>=0.19.0",      # 异步 SQLite
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```
