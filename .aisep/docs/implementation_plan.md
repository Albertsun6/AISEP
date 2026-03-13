# AISEP — 构建计划（整合版）

一个 Workflow 驱动的、精细可控的软件工程系统。

## 设计哲学

**核心原则：约束下的探索（Constrained Exploration）**

每个阶段定义：输入约束 → 输出 Schema → Quality Gate → 人工决策点。AI 在约束内自由工作，人类控制边界。

---

## 设计文档索引（11 份）

| 文档 | 内容 |
|------|------|
| [architecture.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/architecture.md) | 五面体架构、三文件入口、Skills 三层优先级、目录结构、命令接口 |
| [pipeline-stages.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/pipeline-stages.md) | S0-S7 阶段详细设计（含 research.yaml） |
| [methodology-layer.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/methodology-layer.md) | SKILL.md + Frontmatter Gating + 方法论映射 |
| [templates-conventions-layer.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/templates-conventions-layer.md) | 模板 + 规范层（四层模型） |
| [framework-knowledge-base.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/framework-knowledge-base.md) | 框架知识库设计（Skills 机制） |
| [vertical-slice-evaluation.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/vertical-slice-evaluation.md) | 垂直切片策略评估 |
| [onboard-reverse-engineering.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/onboard-reverse-engineering.md) | 逆向 Onboard + changes/ 增量演进 |
| [self-evolution.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/self-evolution.md) | 四层进化架构 |
| [context-loading-protocol.md](file:///Users/yongqian/Desktop/AISEP250311/.aisep/docs/context-loading-protocol.md) | 上下文加载协议（六大机制，含会话审计与交接） |
| implementation_plan.md（本文件） | 构建计划 |

---

## 构建清单

按**依赖顺序**排列，分为 4 批。每批内部可并行。

### 批次 A：入口文件 + 系统配置（基础设施）

无依赖，优先构建。

| 类型 | 文件 | 说明 |
|------|------|------|
| [NEW] | `AISEP.md` | 系统导航入口 — 目录索引 + 当前活跃项目 + 加载指引 |
| [NEW] | `constitution.md` | 全局铁律 — 安全红线 + 不可自动化边界 |
| [NEW] | `.aisep/config.yaml` | 全局配置 — pipeline 阶段 + 控制策略 + 上下文预算 |
| [NEW] | `.aisep/ideas.yaml` | 想法池 — 初始空模板 |
| [NEW] | `.aisep/registry.yaml` | 项目注册表 — 项目索引 + 活跃项目指针 |

---

### 批次 B：项目脚手架模板 + Schema

依赖：批次 A 的配置结构。

| 类型 | 文件 | 说明 |
|------|------|------|
| [NEW] | `.aisep/templates/project-scaffold/manifest.yaml` | 模板版本 + 变更日志 |
| [NEW] | `.aisep/templates/project-scaffold/project.yaml.tmpl` | 项目元数据模板 |
| [NEW] | `.aisep/templates/project-scaffold/constitution.md.tmpl` | 项目级铁律模板 |
| [NEW] | `.aisep/templates/project-scaffold/glossary.yaml.tmpl` | 术语表模板 |
| [NEW] | `.aisep/templates/project-scaffold/adr/000-template.md` | ADR 模板 |
| [NEW] | `.aisep/templates/project-scaffold/artifacts/` | 空目录骨架（global/ + slices/ + changes/） |
| [NEW] | `.aisep/templates/artifacts/*.tmpl.yaml` (×6) | 制品 Schema 模板（S0-S4 + research） |
| [NEW] | `.aisep/schemas/*.schema.yaml` (×8) | 制品验证 Schema（S0-S7） |

---

### 批次 C：Skills（方法论 + 框架知识）

依赖：批次 A 的目录结构。

| 类型 | 文件 | 说明 |
|------|------|------|
| [NEW] | `.agents/skills/methodologies/domain/ddd/SKILL.md` | DDD 方法论（含 Gating frontmatter） |
| [NEW] | `.agents/skills/methodologies/domain/business-blueprint/SKILL.md` | 业务蓝图方法论 |
| [NEW] | `.agents/skills/methodologies/requirements/invest/SKILL.md` | INVEST 质量检查 |
| [NEW] | `.agents/skills/methodologies/requirements/user-story-mapping/SKILL.md` | 用户故事映射 |
| [NEW] | `.agents/skills/frameworks/odoo17/SKILL.md` | Odoo 17 知识库入口（含 Gating） |
| [NEW] | `.agents/skills/frameworks/odoo17/manifest.yaml` | 版本约束 + 依赖 |
| [NEW] | `.agents/skills/frameworks/odoo17/best-practices.md` | 最佳实践 |
| [NEW] | `.agents/skills/frameworks/odoo17/pitfalls.md` | 已知陷阱 |
| [NEW] | `.agents/skills/frameworks/odoo17/templates/` | 代码生成模板 |
| [NEW] | `.aisep/conventions/naming.yaml` | 命名规范 |
| [NEW] | `.aisep/conventions/coding-standards.yaml` | 编码标准 |

---

### 批次 D：Workflow 定义（流程编排）

依赖：批次 A-C 全部就绪。

| 类型 | 文件 | 说明 |
|------|------|------|
| [NEW] | `.agents/workflows/pipeline.md` | 主编排器 — 读取项目，按序调 S0-S7，检查 gate |
| [NEW] | `.agents/workflows/idea-mgmt.md` | 想法管理 — add/list/refine/promote/archive |
| [NEW] | `.agents/workflows/project-mgmt.md` | 项目管理 — list/switch/status/status --full |
| [NEW] | `.agents/workflows/onboard.md` | 逆向 Onboard workflow |
| [NEW] | `.agents/workflows/s0-init.md` | S0 项目初始化阶段 |
| [NEW] | `.agents/workflows/s1-domain.md` | S1 业务领域分析 |
| [NEW] | `.agents/workflows/s2-requirements.md` | S2 需求规格 + Slice 规划 |
| [NEW] | `.agents/workflows/s3-architecture.md` | S3 架构设计 |
| [NEW] | `.agents/workflows/s4-design.md` | S4 Slice 详细设计（含 context 声明） |
| [NEW] | `.agents/workflows/s5-implementation.md` | S5 代码生成 |
| [NEW] | `.agents/workflows/s6-testing.md` | S6 测试验证 |
| [NEW] | `.agents/workflows/s7-deployment.md` | S7 部署配置 |
| [NEW] | `.agents/workflows/s8-retrospective.md` | S8 复盘进化 |
| [NEW] | `.agents/workflows/tidy.md` | 收尾整理（14 步检查清单） |

> [!NOTE]
> `capabilities.md` 不在构建清单中——它由 Pipeline 运行器动态生成，不是静态文件。

---

## 工作量估算

| 批次 | 文件数 | 预计时间 | 复杂度 |
|------|--------|---------|--------|
| A | 5 | ~10m | low |
| B | ~16 | ~25m | mid |
| C | ~11 | ~25m | mid |
| D | ~12 | ~30m | high（workflow 质量决定整个系统） |
| **总计** | **~44 files** | **~90m** | |

---

## Verification Plan

### 结构验证
- `find .aisep .agents -type f | wc -l` 验证文件数
- `find .aisep .agents -name '*.yaml' -exec python3 -c "import yaml; yaml.safe_load(open('{}'))" \;` 验证 YAML 格式

### 模板验证
- 手动执行 `/idea promote` 流程，验证 `project-scaffold/` 是否正确复制到 `projects/{id}/`
- 检查生成的 `project.yaml` 是否包含 `_meta.template_version`
- 验证 `constitution.md.tmpl` 展开后是否自动包含全局铁律引用

### Workflow 验证
- 通过 `/pipeline` 命令启动 S0，验证 workflow 正确引导对话
- 检查 S0 输出的 `project.yaml` 是否符合 Schema
- 验证 S4 workflow 的 `context` frontmatter 是否正确控制上下文加载

### 用户验证
- 选择一个 ERP 场景进行端到端试运行（S0 → S1 → S2 → Gate）
