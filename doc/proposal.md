# AI PR Reviewer — 需求文档

## 1. 项目概述

### 1.1 项目名称
AI PR Reviewer

### 1.2 项目背景
在软件开发过程中，Pull Request（PR）的代码评审是保证代码质量的关键环节。然而，人工评审耗时长、容易遗漏问题，尤其对于安全漏洞和逻辑缺陷的识别存在盲区。本项目旨在构建一个 AI 驱动的 PR 评审助手，自动分析 GitHub PR 中的代码变更，生成结构化的评审报告，辅助开发者提升评审效率与质量。

### 1.3 项目目标
- 构建一个可用的 AI PR Review 工具，支持 CLI 和 Web 两种使用方式
- 实现 PR 变更总结、风险代码识别、Review 建议生成等核心功能
- 作为个人作品集项目，展示 AI 应用开发、前后端工程化能力

### 1.4 目标用户
- 个人开发者
- 开源项目维护者
- 小型开发团队

---

## 2. 功能需求

### 2.1 核心功能

#### 2.1.1 PR 分析（P0 — 必须实现）
- 用户输入 GitHub PR 链接（如 `https://github.com/owner/repo/pull/123`）
- 系统自动获取 PR 的 diff、文件列表、元数据（标题、描述、作者等）
- AI 对每个变更文件进行分析，识别问题并生成建议

#### 2.1.2 分析维度（P0）
| 维度 | 说明 |
|------|------|
| 安全漏洞检测 | SQL注入、XSS、硬编码密钥、权限问题等 |
| 逻辑错误检测 | 边界条件、空指针、竞态条件、类型错误等 |
| 代码风格检查 | 命名规范、可读性、重复代码、过长函数等 |

#### 2.1.3 正面反馈（P0）
- 识别代码中的亮点（好的设计、优雅的实现、合理的抽象）
- 在报告中给出正面评价，而非仅指出问题

#### 2.1.4 本地报告输出（P0）
- 在终端输出格式化的 Markdown 报告
- 报告包含：变更总结、问题列表（按严重程度排序）、亮点、整体评价

#### 2.1.5 自动评论到 GitHub（P0）
- 分析完成后，可选择将评审报告作为评论发布到对应 PR
- 使用 gh CLI 进行认证和评论发布

#### 2.1.6 历史记录（P1）
- 将每次分析的结果存入 SQLite 数据库
- 支持查看历史分析记录列表
- 支持查看单次分析的详细报告

### 2.2 CLI 功能

```
# 基本用法
ai-pr-review analyze https://github.com/owner/repo/pull/123

# 指定输出格式
ai-pr-review analyze https://github.com/owner/repo/pull/123 --output markdown

# 自动发布评论到 GitHub
ai-pr-review analyze https://github.com/owner/repo/pull/123 --comment

# 查看历史记录
ai-pr-review history

# 查看某次分析详情
ai-pr-review history --id <analysis_id>

# 启动 Web 服务
ai-pr-review serve
```

### 2.3 Web 功能

#### 2.3.1 发起分析
- 用户在 Web 页面输入 PR 链接
- 点击"分析"按钮发起分析
- 展示分析进度（加载状态）
- 分析完成后展示报告

#### 2.3.2 查看报告
- 以美观的 Markdown 渲染方式展示分析报告
- 支持按严重程度筛选问题
- 支持将报告导出为 Markdown 文件

#### 2.3.3 历史记录浏览
- 展示历史分析记录列表（PR链接、分析时间、风险等级）
- 点击可查看详细报告

---

## 3. 技术需求

### 3.1 技术栈

| 层 | 技术 | 说明 |
|---|------|------|
| 编程语言 | Python 3.11+ | 主要开发语言 |
| 后端框架 | FastAPI | 异步、自带API文档 |
| 前端框架 | Vue 3 + Vite | 响应式、快速开发 |
| GitHub集成 | gh CLI | 已安装，用于认证和API调用 |
| AI模型 | DeepSeek API（OpenAI兼容格式） | 代码分析能力 |
| 数据库 | SQLite | 轻量、无需额外安装 |
| CLI框架 | Typer | 快速构建命令行工具 |

### 3.2 AI 模型接入

使用 OpenAI 兼容格式接入 DeepSeek API：
- Base URL: `https://api.deepseek.com`（或用户配置的地址）
- API Key: 通过环境变量 `DEEPSEEK_API_KEY` 配置
- 模型: 可配置，默认 `deepseek-chat`
- 支持 OpenAI 兼容的其他模型（如 Mimo 等）

### 3.3 GitHub 集成

- 使用 `gh` CLI 进行身份认证
- 通过 `gh api` 调用 GitHub REST API 获取 PR 信息
- 通过 `gh pr comment` 发布评审评论

### 3.4 数据库设计

**表：analysis_records**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| pr_url | TEXT | PR链接 |
| repo | TEXT | 仓库名（owner/repo） |
| pr_number | INTEGER | PR编号 |
| pr_title | TEXT | PR标题 |
| analysis_time | DATETIME | 分析时间 |
| risk_level | TEXT | 风险等级（low/medium/high） |
| report_markdown | TEXT | 完整报告内容 |
| issues_count | INTEGER | 问题数量 |
| highlights_count | INTEGER | 亮点数量 |

---

## 4. 非功能需求

### 4.1 性能
- 中小型 PR（50 个文件以内）分析时间控制在 2 分钟以内
- 支持并发分析多个文件以提升速度

### 4.2 易用性
- CLI 命令简洁明了，帮助文档清晰
- Web 界面操作直观，无需额外学习成本
- 分析过程中有进度反馈

### 4.3 可扩展性
- AI 模型可配置，支持切换不同模型
- 分析维度可扩展，便于后续添加新的检查规则
- 前后端分离，便于独立演进

### 4.4 本地化
- 仅本地运行，不涉及云端部署
- 所有数据存储在本地 SQLite

---

## 5. 项目约束

- 仅支持中小型 PR（50 个文件以内），暂不处理超大 PR
- 依赖 gh CLI 进行 GitHub 认证，需用户预先安装并登录
- 依赖外部 AI API（DeepSeek），需用户自行配置 API Key
- 仅本地运行，不考虑多用户并发场景

---

## 6. 验收标准

### 6.1 CLI
- [ ] 能通过 PR 链接获取 diff 并完成分析
- [ ] 能在终端输出格式化的 Markdown 报告
- [ ] 能将报告自动评论到 GitHub PR
- [ ] 能查看历史分析记录

### 6.2 Web
- [ ] 能在 Web 页面输入 PR 链接发起分析
- [ ] 能在 Web 页面查看格式化的分析报告
- [ ] 能在 Web 页面浏览历史记录

### 6.3 通用
- [ ] 分析维度覆盖安全、逻辑、风格三个方面
- [ ] 报告包含正面反馈/亮点
- [ ] 分析结果存入 SQLite 并可查询

---

## 7. 项目目录结构（预设）

```
ai-pr-reviewer/
├── Document/              # 项目文档
├── doc/                   # 需求文档
│   └── proposal.md
├── src/                   # 源代码（后续实现）
├── pyproject.toml         # 项目配置（后续创建）
└── README.md              # 项目说明（后续创建）
```
