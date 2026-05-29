# AI PR Reviewer

AI-powered PR code review tool. Automatically analyze GitHub PRs and generate structured review reports.

## Features

- 🔍 **PR Analysis**: Automatically fetch and analyze GitHub PR diffs
- 🛡️ **Security Detection**: Identify security vulnerabilities (SQL injection, XSS, hardcoded secrets)
- 🐛 **Logic Error Detection**: Find logic errors (boundary conditions, null pointers, race conditions)
- 🎨 **Code Style Check**: Review code style (naming, readability, duplicate code)
- ✨ **Positive Feedback**: Highlight good design and elegant implementations
- 📊 **Risk Assessment**: Automatic risk level calculation (low/medium/high)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-pr-reviewer.git
cd ai-pr-reviewer

# Install with uv (recommended)
uv venv
uv pip install -e .

# Or install with pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Set your DeepSeek API key:
   ```
   AI_PR_REVIEWER_AI_API_KEY=your_api_key_here
   ```

3. Ensure `gh` CLI is installed and authenticated:
   ```bash
   gh auth login
   ```

## Usage

### Analyze a PR

```bash
# Basic usage
ai-pr-reviewer analyze https://github.com/owner/repo/pull/123

# Output as Markdown file
ai-pr-reviewer analyze https://github.com/owner/repo/pull/123 --output markdown

# Post comment to GitHub
ai-pr-reviewer analyze https://github.com/owner/repo/pull/123 --comment
```

### View History

```bash
# List recent analyses
ai-pr-reviewer history

# View specific analysis
ai-pr-reviewer history --id 1
```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .

# Run type checker
mypy src/
```

## License

MIT
