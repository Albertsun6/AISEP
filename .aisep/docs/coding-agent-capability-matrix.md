# Coding Agent 能力矩阵

> AISEP 与主流 coding agent 的上下文管理、记忆系统、进化机制对比
> 来源：exp-003 | 上次更新：2026-03-15 | 下次更新：AISEP 系统升级后

## 上下文管理能力

| 机制 | Cursor | Aider | Windsurf | Antigravity | AISEP | 差距方向 |
|------|--------|-------|----------|-------------|-------|---------|
| Codebase Indexing | ✅ @Codebase | ✅ Repo Map | ✅ 全量 | ✅ Corpus | ⚠️ 依赖 agent | 依赖底层 |
| Dynamic Context Discovery | ✅ | ❌ | ✅ | ✅ | ⚠️ Workflow 声明 | 依赖底层 |
| User Behavioral Heuristics | ⚠️ | ❌ | ✅ | ✅ | ❌ | 不需要 |
| Rules Files | .cursorrules | CONVENTIONS | .windsurf | AGENTS.md | ✅ AISEP.md+MetaP.md | **领先** |
| Context Compaction | ✅ auto | ✅ auto | ⚠️ | ✅ auto | ⚠️ /tidy 半自动 | 需增强 |
| Sub-agent Architecture | ⚠️ | ❌ | ✅ Cascade | ✅ subagent | ✅ Scout/角色 | 持平 |
| MCP Integration | ✅ | ❌ | ✅ | ❌ | ❌ | 不适用 |
| Persistent Memory | ⚠️ Notepad | ❌ | ⚠️ | ✅ KI 系统 | ✅ Episodes+Concepts | **领先** |
| Skills/Playbooks | Agent Skills | ❌ | ❌ | Skills | ✅ .agents/skills/ | **领先** |

## 记忆系统能力

| 记忆层 | 行业标准 | AISEP/MetaP |  状态 |
|--------|---------|-------------|------|
| Working Memory | Context Window | In-context | ✅ 等价 |
| Episodic Memory | PostgreSQL + Vector | `.metap/memory/episodes/` (YAML) | ✅ 有，缺自动检索 |
| Semantic Memory | Knowledge Graph / Vector DB | `.metap/ontology/concepts/` (YAML) | ✅ 有，缺向量搜索 |
| Procedural Memory | Playbooks / SKILL.md | `.agents/skills/` | ✅ **领先**（16 skills） |

## 进化机制能力

| 维度 | 行业水平 | AISEP | 状态 |
|------|---------|-------|------|
| 规则文件自动更新 | ❌ 静态文件 | ✅ /evolve + /tidy 反向同步 | **领先** |
| 跨会话学习 | ⚠️ KI/Memory | ✅ 三级记忆 + 结晶路径 | **领先** |
| 多视角讨论 | ❌ | ✅ /deliberate 4角色3轮 | **独有** |
| 知识成熟度追踪 | ❌ | ✅ note→skill + seed→established | **独有** |
| 本体论驱动 | ❌ | ✅ 19 OT / 13 LT / 9 AT | **独有** |
| 分层加载协议 | ⚠️ 简单规则 | ✅ L0→L1→L2→L3 + context_fence | **领先** |

## AISEP 优势总结

1. **深度 > 自动化**：AISEP 在知识管理的深度和系统性上远超行业，但自动化程度不足
2. **独有能力**：多视角辩论 + 本体论驱动 + 知识成熟度追踪 = 行业空白
3. **定位差异**：coding agent 管理单实例上下文，AISEP 管理跨实例知识演进

## 待弥补差距

1. ⚠️ **自动检索**：episodes/concepts 的检索依赖倒排索引（手动），行业用向量搜索（自动）
2. ⚠️ **上下文压缩**：依赖底层 agent 的自动压缩，AISEP 层面缺乏主动压缩
3. ⚠️ **Codebase Indexing**：完全依赖底层 agent，AISEP 层面无独立索引能力
