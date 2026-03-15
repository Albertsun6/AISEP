# exp-003: Coding Agent 进化机制研究报告

> 方向：Antigravity/Cursor/Aider 等 coding agent 的上下文管理、知识持久化和进化机制，以及与 AISEP/MetaP 体系的整合路径
> 置信度：0.82 | 日期：2026-03-15

---

## 一、核心发现

### Scout-A: 架构原理与上下文工程

**发现 1：上下文工程已从 "Prompt Engineering" 进化为独立学科**

Andrej Karpathy 在 2025 年 6 月提出的范式转换：
- LLM = CPU（计算引擎）
- Context Window = RAM（工作内存）
- User/Agent Framework = Operating System（操作系统，负责加载正确的信息）

这与 AISEP 的分层加载协议（L0→L1→L2→L3）高度同构。

**发现 2：主流 coding agent 的 9 大上下文管理机制**

| # | 机制 | Cursor | Aider | Windsurf | Antigravity | AISEP 当前 |
|---|------|--------|-------|----------|-------------|-----------|
| 1 | Codebase Indexing（全量索引） | ✅ @Codebase | ✅ Repo Map | ✅ 全量 | ✅ Corpus | ⚠️ 手动 |
| 2 | Dynamic Context Discovery（动态发现） | ✅ | ❌ | ✅ | ✅ | ⚠️ Workflow 声明 |
| 3 | User Behavioral Heuristics（行为启发式） | ⚠️ | ❌ | ✅ | ✅ | ❌ |
| 4 | Rules Files（规则文件） | .cursorrules | CONVENTIONS.md | .windsurf | AGENTS.md | ✅ AISEP.md + MetaP.md |
| 5 | Context Compaction（上下文压缩） | ✅ summarizer | ✅ auto | ⚠️ | ✅ auto | ⚠️ /tidy 手动 |
| 6 | Sub-agent Architecture（子代理） | ⚠️ | ❌ | ✅ Cascade | ✅ browser_subagent | ⚠️ /explore Scout |
| 7 | MCP（Model Context Protocol） | ✅ | ❌ | ✅ | ❌ | ❌ |
| 8 | Memory/Notes（持久记忆） | ⚠️ Notepad | ❌ | ⚠️ | ✅ Knowledge Items | ✅ MetaP episodes |
| 9 | Skills/Playbooks（技能手册） | Agent Skills | ❌ | ❌ | Skills | ✅ .agents/skills/ |

**关键洞察**：AISEP 在 Rules Files (4) 和 Skills (9) 上已超越多数 coding agent，但在 Codebase Indexing (1) 和 Context Compaction (5) 上依赖底层 agent 能力而非自有机制。

---

### Scout-B: 知识持久化与跨会话学习

**发现 3：四层记忆架构成为行业共识**

| 记忆类型 | 定义 | 行业实现 | AISEP/MetaP 对应 |
|---------|------|---------|-----------------|
| Working Memory | 当前任务/对话的即时上下文 | Context Window | Working Memory（in-context） |
| Episodic Memory | 具体事件、经验的记录 | PostgreSQL + vector | `.metap/memory/episodes/` ✅ |
| Semantic Memory | 抽象概念、规则、知识 | Knowledge Base / Ontology | `.metap/ontology/concepts/` ✅ |
| Procedural Memory | "如何做"的操作知识 | SKILL.md / Playbooks | `.agents/skills/` ✅ |

**关键洞察**：AISEP 不知不觉中已经实现了完整的四层记忆架构！这不是巧合——因为 AISEP 的设计也是从认知科学出发的。但行业的区别在于——行业用**向量数据库**做自动检索，AISEP 用**YAML 倒排索引**做手动加载。

**发现 4：`.cursorrules` / `AGENTS.md` / `CLAUDE.md` 的演进谱系**

```
2024-Q1: .cursorrules（Cursor 专用，单文件，项目根目录）
         ↓ 开放化
2025-Q1: AGENTS.md（跨平台开源标准，支持层级嵌套）
         ↓ Anthropic 参与
2025-Q2: CLAUDE.md（Anthropic 官方，深度集成 Claude Agent SDK）
         ↓ AISEP 视角
2026-Q1: AISEP.md + MetaP.md（双层入口 + 分层加载 + 本体论驱动）
```

AISEP 的双文件入口架构（AISEP.md 工程层 + MetaP.md 思考层）**超越了行业单文件模式**。行业还停留在"给 agent 一个静态说明"，AISEP 已经实现了"动态加载 + 知识演进 + 自进化"。

---

### Scout-C: 集成模式与 AISEP 整合路径

**发现 5：两种集成模式——"吸收"vs"桥接"**

| 模式 | 描述 | 优势 | 风险 | AISEP 适用性 |
|------|------|------|------|-------------|
| **吸收** | 把 agent 的 Knowledge Items / conversation logs 直接导入 AISEP 知识库 | 单一真相源 | 数据量过大、格式不兼容 | ⚠️ 需选择性吸收 |
| **桥接** | AISEP 读取 agent 的输出，提炼后写入自己的体系 | 保持独立性、质量可控 | 需要手动触发 | ✅ 推荐（与 bridge 策略一致） |

**发现 6：Antigravity 的 Knowledge Items 系统**

Antigravity（本 agent）自带 Knowledge Items 系统：
- 存储在 `~/.gemini/antigravity/knowledge/` 中
- 自动从对话中提炼结构化知识
- 包含 `metadata.json` + `artifacts/` 目录
- 由独立的 KNOWLEDGE SUBAGENT 维护

这与 AISEP 的 `.aisep/knowledge/` + `.metap/ontology/concepts/` **高度同构**！但目前两者完全独立运行。

---

## 二、核心洞见

### 洞见 1：AISEP 已经是一个"元 coding agent 框架"

大多数 coding agent（Cursor/Aider/Windsurf）只管理**单个 agent 实例**的上下文和记忆。AISEP 管理的是**跨 agent、跨项目、跨对话**的知识演进——这是一个更高维度的问题。AISEP 的定位不是替代 Cursor/Aider，而是**管理它们的上下文和进化**。

### 洞见 2：从"被动文件"到"知识 API"的演进方向

当前 `.cursorrules` / `AGENTS.md` 还是静态文件——agent 读它，但不改它。AISEP 的 `/evolve` 机制已经走在了前面——agent 可以提议修改自己的规则。下一步是让 AISEP 的知识产出**反向写入** agent 的上下文文件（如自动更新 `.cursorrules` 或 AISEP.md）。

### 洞见 3：Antigravity Knowledge Items 是天然的桥接点

Antigravity 的 KI 系统已经在做"对话知识提炼"——这正是 AISEP `/tidy` Step 10 做的事情。两者的唯一区别是格式（KI 用 markdown/JSON，AISEP 用 YAML）和管理范围（KI 是 per-agent，AISEP 是 per-project + per-system）。

---

## 三、行动建议

### prop-007: AISEP → Agent 反向同步机制

**建议**：当 AISEP 的知识库发生关键变更（新 skill 沉淀、新 evolution rule）时，自动更新 `AISEP.md` 和 `MetaP.md` 中的索引和加载协议。

**工作量**：~20m · 3 files · low
**优先级**：P1
**风险**：低——只改描述性文件

---

### prop-008: Antigravity KI ↔ AISEP Knowledge 桥接

**建议**：在 `/tidy` 中增加一步——扫描 `~/.gemini/antigravity/knowledge/` 目录，识别与当前项目相关的 KI，提示用户是否将其提炼到 `.aisep/knowledge/` 或 `.metap/ontology/concepts/`。

**工作量**：~30m · 2 files · mid
**优先级**：P1
**风险**：中——依赖 Antigravity KI 的目录结构稳定性

---

### prop-009: Context Engineering Audit（上下文工程审计）

**建议**：在 AISEP 体系中引入"上下文工程审计"概念——不只是审计文件使用情况（当前 /tidy Step 13），而是审计**上下文效率**：
- 投入的 token 数 vs 产出价值
- 哪些知识被重复加载但从未使用
- 哪些知识应该在 L0 层但被放在了 L2

**工作量**：~1h · 5 files · mid
**优先级**：P2
**风险**：低

---

### prop-010: Coding Agent 能力矩阵追踪

**建议**：维护一份"coding agent 能力矩阵"——追踪 AISEP 与主流 coding agent 在上下文管理、记忆系统、进化机制上的对比。每次 AISEP 升级后更新，用于指导演进方向。

**工作量**：~15m · 1 file · low
**优先级**：P2
**风险**：极低——纯文档

---

## 四、结论

> **AISEP 在知识管理的深度和系统性上已超越主流 coding agent 工具**——它不仅有四层记忆架构（Working → Episodic → Semantic → Procedural），还有本体论驱动的知识关联、结构化辩论、分层加载协议和自进化机制。
>
> 行业的差距主要在**自动化程度**上——coding agent 的上下文发现和记忆检索是自动的（向量搜索 + codebase indexing），而 AISEP 依赖 workflow 驱动的手动/半自动流程。
>
> **最有价值的整合方向**不是让 AISEP "模仿" coding agent，而是让 AISEP 成为 coding agent 的**知识中枢**——管理它们的上下文、提炼它们的产出、驱动它们的进化。
