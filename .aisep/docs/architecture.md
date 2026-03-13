# AISEP 系统架构

## 五面体分层设计

```
┌─────────────────────────────────────────────────────────┐
│  控制面（Control Plane）                                    │
│  .agents/workflows/        工作流定义                      │
│  .aisep/schemas/             制品 Schema                     │
├─────────────────────────────────────────────────────────┤
│  知识面（Knowledge Plane）— 三层优先级 Skills 机制          │
│  内置层: AISEP 默认方法论（随系统分发，最低优先级）          │
│  全局层: ~/.aisep/skills/（跨项目共享，中等优先级）          │
│  项目层: .agents/skills/（项目级覆盖，最高优先级）          │
│  .aisep/conventions/             工程规范 (WHAT rules)     │
├─────────────────────────────────────────────────────────┤
│  管理面（Management Plane）                                 │
│  .aisep/config.yaml          全局配置                      │
│  .aisep/ideas.yaml           想法池                          │
│  .aisep/registry.yaml        项目注册表                    │
├─────────────────────────────────────────────────────────┤
│  进化面（Evolution Plane）                                 │
│  .aisep/evolution/            自进化引擎数据                │
├─────────────────────────────────────────────────────────┤
│  数据面（Data Plane）— 每项目隔离                         │
│  projects/{project-id}/     项目工作空间                   │
└─────────────────────────────────────────────────────────┘
```

---

## 目录结构

```
# ── 三文件入口（借鉴 OpenClaw AGENTS/SOUL/TOOLS 模式）──
AISEP.md                             ← 🔑 系统导航层（AI 第一个读的）
                                       目录索引 + 当前活跃项目 + 加载指引
constitution.md                     ← 🔑 全局铁律（不可变，所有项目共享）
                                       安全红线 + 伦理约束 + 不可自动化的边界
capabilities.md                     ← 🔑 能力清单（动态生成，AI 知道自己能做什么）
                                       当前可用命令 + 已加载 Skills + 工具状态

.agents/                            ← Antigravity 原生约定
├── workflows/                      ← 工作流定义（控制面）
│   ├── pipeline.md                 ← 主 pipeline 编排器
│   ├── idea-mgmt.md                ← 想法管理
│   ├── project-mgmt.md             ← 项目管理
│   ├── onboard.md                  ← 逆向 Onboard（现有系统接管）
│   └── s0-init.md ~ s8-retro.md   ← 9 个阶段 workflow
└── skills/                         ← 🔑 项目级技能库（最高优先级，可覆盖全局层）
    ├── methodologies/              ← 方法论 = skill
    │   ├── domain/
    │   │   ├── ddd/SKILL.md
    │   │   ├── business-blueprint/SKILL.md
    │   │   └── event-storming/SKILL.md
    │   ├── requirements/
    │   │   ├── invest/SKILL.md
    │   │   └── user-story-mapping/SKILL.md
    │   ├── architecture/
    │   │   ├── c4-model/SKILL.md
    │   │   └── adr/SKILL.md
    │   ├── design/
    │   │   └── solid/SKILL.md
    │   ├── implementation/
    │   │   └── clean-code/SKILL.md
    │   ├── testing/
    │   │   └── test-pyramid/SKILL.md
    │   └── deployment/
    │       └── twelve-factor/SKILL.md
    └── frameworks/                 ← 框架知识 = skill
        ├── odoo17/
        │   ├── SKILL.md              ← 入口：命名规范 + 标准模块映射 + 文件索引
        │   ├── manifest.yaml         ← 版本约束 + 依赖
        │   ├── philosophy.md         ← 🆕 5 大设计原则 + ORM 核心概念
        │   ├── structure.md          ← 🆕 模块结构 + __manifest__ 详解
        │   ├── best-practices.md     ← Model/View/安全/性能/测试最佳实践
        │   ├── pitfalls.md           ← P1-P4 分级陷阱 + 自检清单
        │   └── templates/            ← 代码生成模板（就近原则）
        ├── react18/                ← 未来
        └── fastapi/                ← 未来

~/.aisep/                               ← 🔑 全局级技能库（跨项目共享，中等优先级）
├── skills/
│   ├── methodologies/                ← 用户沉淀的全局方法论
│   │   └── event-storming/
│   └── frameworks/                   ← 用户沉淀的全局框架知识
│       ├── odoo17/                   ← 跨项目共享的 Odoo 知识
│       └── react18/
├── config.yaml                       ← 用户全局偏好
└── templates/                        ← 用户全局制品模板

.aisep/                              ← AISEP 配置 + 状态
├── README.md                       ← 目录说明（渐进披露 L1）
├── config.yaml                     ← 全局配置
├── ideas.yaml                      ← 想法池
├── registry.yaml                   ← 项目注册表（只保留活跃项目）
├── archive/                        ← 🆕 归档存储
│   └── registry-archive.yaml       ← 归档项目注册表（冷热分区）
├── schemas/                        ← 制品 Schema（验证用，9 个定义）
│   ├── _index.yaml                 ← 所有 schema 索引
│   ├── s0-project.schema.yaml      ← 项目定义
│   ├── s0-research.schema.yaml     ← 技术调研
│   ├── s1-domain-model.schema.yaml ← 领域模型
│   ├── s1-capability-map.schema.yaml ← 能力图谱
│   ├── s2-functional.schema.yaml   ← 功能需求
│   ├── s2-slice-plan.schema.yaml   ← Slice 规划
│   ├── s3-architecture.schema.yaml ← 架构设计（最复杂）
│   ├── s4-slice-design.schema.yaml ← Slice 详细设计
│   └── s7-deployment.schema.yaml   ← 部署配置
├── conventions/                    ← 全局工程规范
│   └── _index.yaml
├── templates/artifacts/            ← 制品模板（与框架无关）
├── evolution/                      ← 🔑 自进化引擎数据
│   ├── triggers.yaml               ← L2 触发条件
│   ├── rule-metrics.yaml           ← L3 规则有效率追踪
│   ├── corrections-log.yaml        ← 跨项目修正汇总
│   └── evolution-history.yaml      ← 进化历史审计
├── knowledge/                      ← 🆕 认知知识库（用户学习笔记）
│   ├── index.yaml                  ← 知识条目索引
│   ├── entry-template.yaml         ← 条目格式模板
│   ├── entries/                    ← 知识条目详情
│   └── reviews/                    ← 定期回顾记录
└── docs/                           ← 系统设计文档

projects/                           ← 多项目工作空间（数据面）
├── {project-id}/
│   ├── project.yaml                ← 项目元数据 + pipeline 状态
│   ├── constitution.md             ← 🔑 项目级铁律（继承全局 constitution.md + 项目特有约束）
│   ├── glossary.yaml               ← 统一语言词汇表（跨阶段共享）
│   ├── _map.yaml                   ← 🆕 项目地图（Gate 通过时自动生成，低 token 全局概览）
│   ├── _context_audit.yaml         ← 🆕 上下文审计日志（/tidy 追加，保留最近 10 条）
│   ├── _next_session.yaml          ← 🆕 会话交接清单（/tidy 生成，新对话消费）
│   ├── artifacts/                  ← 项目制品
│   │   ├── global/                 ← S0-S3 全局制品
│   │   │   ├── project.yaml         (S0)
│   │   │   ├── research.yaml        (S0, 可选) 技术选型/竞品调研
│   │   │   ├── domain-model.yaml    (S1)
│   │   │   ├── capability-map.yaml  (S1)
│   │   │   ├── gap-analysis.yaml    (S1, 条件性)
│   │   │   ├── functional.yaml      (S2)
│   │   │   ├── slice-plan.yaml      (S2)
│   │   │   ├── architecture.yaml    (S3)
│   │   │   └── deployment.yaml      (S7)
│   │   ├── slices/                 ← S4-S6 按 Slice 隔离（Greenfield）
│   │   │   ├── slice-1-bom-management/
│   │   │   │   ├── design.yaml      (S4)
│   │   │   │   ├── code/            (S5)
│   │   │   │   └── tests/           (S6)
│   │   │   └── slice-2-production-order/
│   │   │       └── ...
│   │   └── changes/                ← 增量变更单元（Brownfield / Onboard 后演进）
│   │       ├── change-001-add-qc/
│   │       │   ├── proposal.yaml    ← 变更提案 + 影响分析
│   │       │   ├── design.yaml      ← 变更设计（对齐 S4）
│   │       │   └── implementation/  ← 变更实现（对齐 S5-S6）
│   │       └── change-002-.../
│   └── history/                    ← Gate 审批记录
│       ├── gate-log.yaml           ← 自进化 L1 数据源
│       └── {stage}-{timestamp}.yaml
└── {another-project-id}/
    └── ...
```

---

## 三文件入口设计（借鉴 OpenClaw AGENTS/SOUL/TOOLS）

| 文件 | 对应 OpenClaw | 职责 | 加载时机 |
|------|-------------|------|----------|
| `AISEP.md` | `AGENTS.md` | 系统導航、目录索引、当前活跃项目、渐进披露加载指引 | 始终加载 |
| `constitution.md` | `SOUL.md` | 全局铁律（安全红线 + 伦理边界 + 不可自动化边界） | 始终加载 |
| `capabilities.md` | `TOOLS.md` | 当前可用命令 + 已加载 Skills + 工具状态 | 动态生成 |

**全局 vs 项目 constitution**：

```
constitution.md（根目录）           ← 全局铁律（所有项目共享）
  • 不可降级、不可自动修改
  • 示例：“所有规则变更必须经人确认”“禁止删除生产数据”

projects/{id}/constitution.md      ← 项目级铁律（继承全局 + 项目特有）
  • 可添加项目特有约束，不可削弱全局铁律
  • 示例：“本项目严禁裸 SQL”“必须继承 odoo base 而非直接修改”
```

---

## Skills 三层优先级（借鉴 OpenClaw Bundled/Managed/Workspace）

```
╒═════════════════════════════════════════════════════╕
│  Layer 3 （最高优先级）: 项目级 Skills             │
│  .agents/skills/{methodologies,frameworks}/         │
│  可覆盖下层同名 Skill、添加项目特有 Skill           │
├─────────────────────────────────────────────────────┤
│  Layer 2 （中等优先级）: 全局级 Skills             │
│  ~/.aisep/skills/{methodologies,frameworks}/         │
│  跨项目共享、用户沉淀、L2 自进化产出的知识         │
├─────────────────────────────────────────────────────┤
│  Layer 1 （最低优先级）: 内置 Skills              │
│  AISEP 默认方法论（随系统分发）                     │
│  DDD, INVEST, C4, SOLID, test-pyramid 等 基础套件   │
╘═════════════════════════════════════════════════════╛
```

**解析规则（同名 Skill 冲突时）**：
- 项目层 > 全局层 > 内置层（就近原则）
- 合并策略：`checklist`、`artifact_additions` 等列表字段可叠加，`instructions` 等文本字段以高优先级层为准
- 自进化流向：L2 知识沉淀默认写入全局层（`~/.aisep/skills/`），用户可手动下沉到项目层

---

## `/project status --full` 聚合视图

从项目所有制品自动合成只读概览（借鉴 OpenSpec 活文档理念）：

```
/project status --full
│
├─ 读取 project.yaml          → 项目基本信息 + pipeline 状态
├─ 读取 glossary.yaml          → 术语数量统计
├─ 读取 artifacts/global/*.yaml → 每阶段制品摘要
├─ 读取 slices/*/design.yaml    → Slice 完成度
├─ 读取 changes/*/proposal.yaml → 待处理变更
└─ 读取 history/gate-log.yaml   → Gate 通过/修正/拒绝统计
  │
  └→ 输出 project-overview.md（只读快照，不持久化）
```

## 跨阶段共享制品

```yaml
# Glossary — S1 创建，S2-S6 引用，确保全程术语一致
# 位于 projects/{id}/glossary.yaml
shared_artifacts:
  glossary:
    created_at: s1
    referenced_by: [s2, s3, s4, s5, s6]
    enforcement: strict
    content:
      terms:
        - term: "物料清单"
          english: "Bill of Materials"
          abbreviation: "BOM"
          model_name: "bom"
          class_name: "BillOfMaterials"
          definition: "描述产品由哪些原材料和子件组成的层级结构"
          context: "产品定义"
          aliases: ["配方", "产品结构"]
```

---

## 项目注册表 `registry.yaml`（冷热分区）

```yaml
# .aisep/registry.yaml — 只保留活跃项目
aisep_registry:
  active_project: "mfg-erp-001"
  projects:
    - id: "mfg-erp-001"
      name: "制造业 ERP"
      tech_stack: "odoo17"
      status: "s2-requirements"
      created_at: "2026-03-11"

  # 归档项目另存（保持主注册表轻量）
  archive_ref: ".aisep/archive/registry-archive.yaml"
```

```yaml
# .aisep/archive/registry-archive.yaml — 已完成/归档项目
archived_projects:
  - id: "retail-erp-002"
    name: "零售 ERP"
    stage: "s0-init"
    archived_at: "2026-03-15"
    summary: "初始化阶段归档"
    project_dir: "projects/retail-erp-002/"
```

**迁移触发**：`/project archive` 命令将项目从 `registry.yaml` 移至 `registry-archive.yaml`，同时在 `AISEP.md` 的 `context_fence.excluded_dirs` 中加入该项目路径。

---

## 想法池 `ideas.yaml`

```yaml
# .aisep/ideas.yaml
ideas:
  - id: "idea-001"
    title: "制造业 ERP"
    raw_input: "做一个制造业 ERP，需要 BOM 管理、生产计划、质量检验、仓储"
    tags: [erp, manufacturing]
    priority: high
    status: promoted
    promoted_to: "mfg-erp-001"

  - id: "idea-002"
    title: "零售 POS 系统"
    raw_input: "零售门店 POS，支持扫码、会员积分、多门店库存同步"
    tags: [erp, retail, pos]
    priority: medium
    status: draft
```

**Idea 生命周期：`draft → refined → promoted → archived`**

---

## 命令接口

```
# 想法管理
/idea add <描述>              ← 快速记录
/idea list                     ← 列出所有
/idea refine <id>              ← AI 辅助分析
/idea promote <id>             ← 提升为项目（→ S0）
/idea archive <id>             ← 搞置

# 项目管理
/project list                  ← 列出所有项目
/project switch <id>           ← 切换活跃项目
/project status [id]           ← 查看进度（简要）
/project status --full [id]    ← 聚合视图
/project archive <id>          ← 归档项目

# Pipeline 执行
/pipeline                      ← 执行当前项目 pipeline
/s0-init ~ /s7-deployment      ← 直接进入指定阶段
/onboard --source <path>       ← 逆向接管现有模块

# 系统维护
/tidy                          ← 对话窗口收尾整理
/evolve                        ← 触发自进化分析
```

---

## 配置文件设计

### 全局配置 `config.yaml`

```yaml
# .aisep/config.yaml
aisep:
  version: "1.0"
  defaults:
    tech_stack: "odoo17"
    artifact_format: yaml
  
  pipeline:
    stages:
      - id: s0
        name: "项目初始化"
        workflow: ".agents/workflows/s0-init.md"
        gate: manual
      - id: s1
        name: "业务领域分析"
        workflow: ".agents/workflows/s1-domain.md"
        gate: manual
      # ... s2-s7 同结构

  control:
    require_approval_on_gate: true
    allow_stage_skip: false
    allow_stage_rollback: true
```

### 项目配置 `project.yaml`

```yaml
# projects/{id}/project.yaml
project:
  id: "mfg-erp-001"
  name: "制造业 ERP"
  tech_stack: "odoo17"
  
  pipeline_state:
    current_stage: "s1-domain"
    stages:
      s0: { status: "completed", gate_passed: true }
      s1: { status: "in_progress", gate_passed: false }

  gate_overrides:
    s6: auto     # 该项目的 S6 设为自动通过
```

> [!IMPORTANT]
> **后期可切换**：更换技术栈只需创建新框架知识库（如 `skills/frameworks/nextjs/`），S0-S4 的制品**完全复用**，只有 S5-S7 根据框架知识库重新生成。
