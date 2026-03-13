# AISEP 系统指南

> **这是你了解、使用和改进 AISEP 的唯一入口。** 每次迭代后更新此文件。
> 最后更新：2026-03-13 09:21（Backlog 7 方案落地 + L2 知识沉淀协议）

---

## 一、AISEP 是什么

**AI-Integrated Software Engineering Process** — 一个用 Workflow + Skills + Schema 驱动的软件工程系统。

**一句话本质**：给 AI 一套约束（输入→输出→Gate），让它在约束内自由工作，人控制边界。

```
用户想法 → S0 → S1 → S2 → S3 → [S4→S5→S6]×N → S7 → S8 复盘进化
              ↑ Gate ↑ Gate ↑ Gate    ↑ Gate/Slice    ↑ Gate ↑ Gate
                                                              ↓
                                                        知识沉淀 + 系统进化
```

---

## 二、系统心智模型

### 五面体

| 面 | 一句话 | 你关心它的时机 |
|----|--------|--------------|
| **控制面** | 流程怎么走 | 想改 Pipeline 逻辑时 |
| **知识面** | AI 怎么想 | 想加/改方法论或框架知识时 |
| **管理面** | 项目怎么组织 | 想管多项目或想法时 |
| **进化面** | 系统怎么变聪明 | 想回顾和改进系统时 |
| **数据面** | 项目产出了什么 | 想查看具体项目制品时 |

### 三层上下文控制

```
L0 常驻（< 2K tokens）：AISEP.md + constitution + glossary
L1 阶段（< 5K tokens）：当前 Workflow + Skills（Gating 过滤）
L2 按需（< 3K tokens）：历史制品摘要、其他 Slice
```

---

## 三、关注图谱（Concern Map）

**"我想改 X → 该看哪几个文件"**

| 我想… | 看这些文件 | 其他不用管 |
|-------|-----------|-----------|
| 改某个阶段的流程 | `.agents/workflows/s{n}-*.md` | ← 1 file |
| 改/加一个方法论 | `.agents/skills/methodologies/{name}/SKILL.md` | ← 1 file |
| 改制品长什么样 | `.aisep/templates/artifacts/s{n}-*.tmpl.yaml` | ← 1 file |
| 改新项目创建时的内容 | `.aisep/templates/project-scaffold/*` | ← 2-3 files |
| 改框架知识（如 Odoo） | `.agents/skills/frameworks/odoo17/*` | ← pick 1 |
| 改命名/编码规范 | `.aisep/conventions/*.yaml` | ← 1 file |
| 改全局铁律 | `constitution.md` | ← 1 file |
| 改上下文加载规则 | `.aisep/docs/context-loading-protocol.md` | ← 1 file |
| 改上下文排除规则 | `AISEP.md` → `context_fence` 区块 | ← 1 file |
| 查看项目概览 | `projects/{id}/_map.yaml` | ← 1 file |
| 做结构性调整 | `.aisep/docs/architecture.md`（**先改这里**） | ← 然后在 backlog 里记受影响的文件 |
| 记录新想法 | `.aisep/backlog.md` | ← 1 file |

---

## 四、目录结构速览

```
AISEP250311/
├── AISEP.md                 ← AI 入口（导航）
├── constitution.md          ← 全局铁律（12 条）
│
├── .agents/                 ← 「做什么 + 怎么想」
│   ├── workflows/           ← 14 个流程定义
│   │   ├── pipeline.md      ← 主编排器
│   │   ├── idea-mgmt.md     ← 想法管理
│   │   ├── project-mgmt.md  ← 项目管理
│   │   ├── onboard.md       ← 逆向接管
│   │   ├── tidy.md          ← 收尾整理（14 步检查清单）
│   │   └── s0~s8            ← 9 个阶段 workflow（含 S8 复盘进化）
│   │   （全部 14 个 Workflow 均已充实为可执行级）
│   └── skills/              ← 知识面
│       ├── methodologies/   ← 16 个方法论（7 个子目录）
│       └── frameworks/      ← Odoo17 知识库（6 个文件，809 行）
│
├── .aisep/                  ← 「系统配置 + 模板 + 文档」
│   ├── config.yaml          ← Pipeline 配置 + 上下文预算
│   ├── ideas.yaml           ← 想法池
│   ├── registry.yaml        ← 项目注册表
│   ├── conventions/         ← 命名 + 编码标准
│   ├── schemas/             ← 制品 Schema（9 个验证定义）
│   ├── templates/
│   │   ├── project-scaffold/  ← 项目脚手架（复制用）
│   │   └── artifacts/         ← 制品格式模板（引用用）
│   ├── knowledge/           ← 认知知识库（学习笔记）
│   ├── evolution/           ← 自进化引擎数据
│   ├── backlog.md           ← 待做想法
│   └── docs/ (11 份)        ← 设计文档
│
└── projects/                ← 「项目数据」（待创建）
```

---

## 五、常用操作

| 场景 | 做法 |
|------|------|
| **有新想法** | 写到 `.aisep/backlog.md`，或 `/idea add` |
| **开始新项目** | `/idea promote <id>` → 自动复制脚手架 → 进入 S0 |
| **推进项目** | `/pipeline` → 执行当前阶段 |
| **做结构改进** | 先改 `architecture.md` → 记 backlog → 逐个同步 |
| **加新方法论** | 在 `skills/methodologies/` 下建目录，写 `SKILL.md` |
| **改制品格式** | 改 `templates/artifacts/s{n}-*.tmpl.yaml` |
| **快速定位** | 说"状态" → 展示已建/待建/backlog 统计 |
| **对话收尾** | `/tidy` → 同步变更 + Git checkpoint（AI 判断 + 人工审核） |
| **版本管理** | `/tidy` 步骤 15 自动检测变更，人工确认后 commit + push |

### 完整命令速查

#### 想法管理

| 命令 | 说明 |
|------|------|
| `/idea add <描述>` | 记录想法到 ideas.yaml |
| `/idea list` | 列出所有未归档想法 |
| `/idea refine <id>` | AI 辅助分析可行性和范围 |
| `/idea promote <id>` | 提升为项目 → 复制脚手架 → 进入 S0 |
| `/idea archive <id>` | 归档想法 |

#### 项目管理

| 命令 | 说明 |
|------|------|
| `/project list` | 列出所有项目 |
| `/project switch <id>` | 切换活跃项目 |
| `/project status` | 简要进度（当前阶段 + 最近 Gate） |
| `/project status --full` | 聚合视图（从所有制品合成概览） |
| `/project archive <id>` | 归档项目 |

#### Pipeline 执行

| 命令 | 说明 |
|------|------|
| `/pipeline` | 推进当前活跃项目的 pipeline |
| `/s0-init` | 直接进入 S0 项目初始化 |
| `/s1-domain` | 直接进入 S1 业务领域分析 |
| `/s2-requirements` | 直接进入 S2 需求规格 + Slice 规划 |
| `/s3-architecture` | 直接进入 S3 架构设计 |
| `/s4-design` | 直接进入 S4 Slice 详细设计 |
| `/s5-implementation` | 直接进入 S5 代码实现 |
| `/s6-testing` | 直接进入 S6 测试验证 |
| `/s7-deployment` | 直接进入 S7 部署配置 |

#### 系统维护

| 命令 | 说明 |
|------|------|
| `/onboard --source <path>` | 逆向接管现有系统模块 |
| `/tidy` | 对话窗口结束前收尾整理 |

#### 交互快捷命令

| 命令 | 说明 |
|------|------|
| `状态` | 快速展示已建/待建/backlog 统计 |
| `进化` | 触发交互规则自进化协议 |
| `深挖` | 对当前话题垂直深入 |
| `拉远` | 缩放到更高抽象层 |
| `总结` | 压缩当前讨论为结构化要点 |
| `转向` | 切换话题方向 |
| `验收` | 触发截图 + 录屏 + 功能清单验证 |
| `全做` | 执行所有推荐选项，静默完成后报告 |

---

## 六、执行流程

### 正向路径（新项目）

```
/idea add "做一个制造业 ERP"          ← 记录想法
    ↓
/idea promote idea-001                ← 复制脚手架 → 创建项目
    ↓
S0 项目初始化                         ← 对话提取范围 → project.yaml
    ↓ Gate: 确认范围
S1 业务领域分析                       ← DDD + Blueprint → domain-model.yaml
    ↓ Gate: 确认领域模型
S2 需求规格                           ← INVEST + Story Map → functional.yaml + slice-plan.yaml
    ↓ Gate: 确认需求 + Slice 划分
S3 架构设计                           ← 确认技术栈 → 加载框架 Skill → architecture.yaml
    ↓ Gate: 确认架构
循环 ×N（每个 Slice）:
  S4 详细设计 → Gate → S5 代码实现 → Gate → S6 测试 → Gate
    ↓
S7 部署配置                           ← deployment.yaml
    ↓ Gate: 最终确认
```

### 逆向路径（接管现有系统）

```
/onboard --source <path>              ← 扫描现有代码
    ↓
逆向提取 + 准确度评估                  ← 代码 → 制品（标注置信度）
    ↓
人工补全                               ← 确认低置信度制品
    ↓
进入增量模式                           ← 新需求走 changes/ → S4-S6
```

### 关键机制

- 每个 Gate 都是**人工确认**（constitution 第 1 条）
- Gate 通过时自动：记录 gate-log + 生成制品摘要（Compaction）
- S3 确认技术栈后才加载框架 Skill（Gating）
- S4-S6 **一次一个 Slice**，其他 Slice 上下文被排除
- `/tidy` 收尾时自动：上下文审计 + 话题偏移评估 + 生成交接清单（`_next_session.yaml`）
- 新对话开场：读取交接清单 → 推荐加载文件 → 用户确认 → 精准加载
- Context Fence：`AISEP.md` 声明排除目录，多项目时硬排除非活跃项目的上下文
- Project Map：`_map.yaml` Gate 通过时自动生成，低 token 项目全貌（< 500 tokens）
- Registry 冷热分区：活跃项目留主注册表，归档项目迁移到 `registry-archive.yaml`
- Git 版本同步：`/tidy` 收尾时 AI 判断是否需要 commit，人工确认后自动 commit + push（GitHub: [Albertsun6/AISEP](https://github.com/Albertsun6/AISEP)）

---

## 八、设计中使用的方法论

以下方法论在 AISEP 设计过程中被实际运用，也内化为系统的一部分：

| 方法论 | 用在何处 | 核心要点 |
|--------|---------|---------|
| **对标分析 (Benchmarking)** | 研究 OpenClaw / SpecKit / OpenSpec | 不重新发明轮子，提取已验证的模式 |
| **渐进披露 (Progressive Disclosure)** | 上下文三层加载 L0→L1→L2 | 按需下钻，不一次性全量加载 |
| **Context Engineering** | 上下文加载协议（5 大机制） | Compaction + Just-in-Time + Gating |
| **YAGNI** | 延迟项目类型 Profile | 不提前实现不确定的功能 |
| **关注点分离 (SoC)** | 五面体分层 + Concern Map | 改一个面不影响其他面 |
| **Prototype vs Factory** | 项目脚手架模板设计 | 模板复制 + 版本追踪 vs 动态生成 |
| **三文件入口** | 借鉴 OpenClaw AGENTS/SOUL/TOOLS | 导航、铁律、能力各司其职 |
| **三层优先级** | 借鉴 OpenClaw Bundled/Managed/Workspace | 内置→全局→项目，就近覆盖 |
| **变更隔离** | 借鉴 OpenSpec changes/ | Brownfield 增量演进独立管理 |
| **ADR** | S3 架构决策记录 | 记录决策背景和理由，防止遗忘 |
| **DDD** | S1 领域建模 | 限界上下文 + 统一语言 + 聚合根 |
| **INVEST** | S2 Story 质量检查 | 独立/可协商/有价值/可估算/小/可测试 |
| **User Story Mapping** | S2 Slice 划分 | 横向切分 Story Map → Slice 边界 |
| **Test Pyramid** | S6 测试策略 | 单元 > 集成 > E2E 的金字塔比例 |
| **Twelve-Factor App** | S7 部署 | 环境变量、无状态、日志流 |

---

## 九、新对话开场模板

```
继续 AISEP 系统。上一轮覆盖了：
- [关键成果 1]
- [关键成果 2]

本轮目标：[具体目标]

需要延续的上下文：
- 系统指南：.aisep/docs/system-guide.md
- 设计文档：.aisep/docs/
- 构建计划：.aisep/docs/implementation_plan.md
```
