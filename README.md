# AI PR Reviewer

AI 驱动的 PR 代码审查工具。自动分析 GitHub PR 并生成结构化审查报告。

## 功能特性

- 🔍 **PR 分析**：自动获取并分析 GitHub PR 差异
- 🛡️ **安全检测**：识别安全漏洞（SQL 注入、XSS、硬编码密钥）
- 🐛 **逻辑错误检测**：查找逻辑错误（边界条件、空指针、竞态条件）
- 🎨 **代码风格检查**：审查代码风格（命名、可读性、重复代码）
- ✨ **正向反馈**：突出优秀设计和优雅实现
- 📊 **风险评估**：自动计算风险等级（低/中/高）

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/ai-pr-reviewer.git
cd ai-pr-reviewer

# 使用 uv 安装（推荐）
uv venv
uv pip install -e .

# 或使用 pip 安装
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## 配置

1. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 设置 DeepSeek API 密钥：
   ```
   AI_PR_REVIEWER_AI_API_KEY=your_api_key_here
   ```

3. 确保 `gh` CLI 已安装并认证：
   ```bash
   gh auth login
   ```

## 使用方法

### 分析 PR

```bash
# 基本用法
ai-pr-reviewer analyze https://github.com/owner/repo/pull/123

# 输出为 Markdown 文件
ai-pr-reviewer analyze https://github.com/owner/repo/pull/123 --output markdown

# 发布评论到 GitHub
ai-pr-reviewer analyze https://github.com/owner/repo/pull/123 --comment
```

### 查看历史

```bash
# 列出最近的分析
ai-pr-reviewer history

# 查看特定分析
ai-pr-reviewer history --id 1
```

## 开发

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 运行代码检查
ruff check .

# 运行类型检查
mypy src/
```
